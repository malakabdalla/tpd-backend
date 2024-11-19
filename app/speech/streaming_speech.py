from flask import Blueprint
from flask_socketio import SocketIO, emit
from main import socketio
import queue, threading, base64


# socketio = SocketIO(
#     app,
#     cors_allowed_origins="*",  # More permissive for testing
#     async_mode='threading',
#     logger=True,
#     engineio_logger=True,
#     ping_timeout=60,
#     ping_interval=25,
#     max_http_buffer_size=1e8,
#     always_connect=True,
#     http_compression=False  # Disable compression for testing
# )

# Create a Blueprint for socket functionality
socket_bp = Blueprint('socket_bp', __name__)

# Placeholder for SocketIO reference

# Initialize the SocketIO reference within the module


# Define a socket event handler
@socketio.on('message', namespace='/my_namespace')
def handle_message(data):
    print(f"Received message: {data}")
    emit('response', {'message': 'Message received!'}, namespace='/my_namespace')

active_streams = {}

class AudioStreamHandler:
    def __init__(self, socket_id, sample_rate=16000):
        self.socket_id = socket_id
        self.sample_rate = sample_rate
        self.buffer = queue.Queue()
        self.closed = False
        try:
            self.client = SpeechClient()
        except Exception as e:
            logger.error(f"Failed to initialize Speech V2 client: {e}")
            raise
        
    def add_chunk(self, chunk):
        """Add an audio chunk to the buffer."""
        if not self.closed:
            try:
                self.buffer.put(chunk, timeout=5)  # 5 second timeout
            except queue.Full:
                logger.warning(f"Buffer full for client {self.socket_id}")
                self.emit_error("Processing buffer full - please try again")
            
    def close(self):
        """Close the stream and cleanup."""
        if not self.closed:
            self.closed = True
            self.buffer.put(None)  # Sentinel to stop the generator
            logger.info(f"Closed stream for client {self.socket_id}")

    def generator(self):
        """Generate audio chunks from the buffer."""
        while not self.closed:
            try:
                chunk = self.buffer.get(timeout=30)  # 30 second timeout
                if chunk is None:
                    return
                yield chunk
            except queue.Empty:
                logger.warning(f"No audio received for 30 seconds from {self.socket_id}")
                self.emit_error("No audio received for 30 seconds - closing connection")
                self.close()
                return

    def emit_transcription(self, transcript, is_final=False):
        """Emit transcription using Socket.IO."""
        try:
            socketio.emit('transcription', {
                'transcript': transcript, 
                'is_final': is_final
            }, room=self.socket_id)
        except Exception as e:
            logger.error(f"Failed to emit transcription: {e}")

    def emit_error(self, error_message):
        """Emit error using Socket.IO."""
        try:
            socketio.emit('error', {'message': error_message}, room=self.socket_id)
        except Exception as e:
            logger.error(f"Failed to emit error: {e}")

@socketio.on("connect")
def handle_connect():
    """Handle new client connections."""
    logger.info(f"Client connected: {request.sid}")
    socketio.emit('connection_status', {'status': 'connected'}, room=request.sid)

@socketio.on("disconnect")
def handle_disconnect():
    """Clean up when a client disconnects."""
    if request.sid in active_streams:
        try:
            stream = active_streams[request.sid]
            stream.close()
            del active_streams[request.sid]
            logger.info(f"Cleaned up resources for client: {request.sid}")
        except Exception as e:
            logger.error(f"Error during disconnect cleanup: {e}")
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on("start_audio_stream")
def start_audio_stream():
    """Initialize a new audio stream for transcription."""
    try:
        # Clean up any existing stream for this client
        if request.sid in active_streams:
            active_streams[request.sid].close()
            del active_streams[request.sid]

        # Create new stream handler for this client
        stream_handler = AudioStreamHandler(request.sid)
        active_streams[request.sid] = stream_handler

        # Configure Speech V2 recognition
        recognition_config = cloud_speech_types.RecognitionConfig(
            auto_decoding_config=cloud_speech_types.AutoDetectDecodingConfig(),
            language_codes=["en-GB"],
            model="long",
        )
        streaming_config = cloud_speech_types.StreamingRecognitionConfig(
            config=recognition_config
        )
        config_request = cloud_speech_types.StreamingRecognizeRequest(
            recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
            streaming_config=streaming_config,
        )

        def process_audio_stream(handler):
            """Process audio stream and emit transcriptions."""
            try:
                audio_generator = handler.generator()
                audio_requests = (
                    cloud_speech_types.StreamingRecognizeRequest(audio=chunk)
                    for chunk in audio_generator
                )
                streaming_features= cloud_speech_types.StreamingRecognitionFeatures(interim_results=True)

                recognition_config = cloud_speech_types.RecognitionConfig(
                    auto_decoding_config=cloud_speech_types.AutoDetectDecodingConfig(),
                    language_codes=["en-GB"],
                    model="long",
                )
                streaming_config = cloud_speech_types.StreamingRecognitionConfig(
                    config=recognition_config,
                    streaming_features=streaming_features
                )
                config_request = cloud_speech_types.StreamingRecognizeRequest(
                    recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
                    streaming_config=streaming_config,
                )

                def requests_generator():
                    yield config_request
                    yield from audio_requests

                responses = handler.client.streaming_recognize(
                    requests=requests_generator()
                )

                for response in responses:
                    if handler.closed:
                        break

                    if not response.results:
                        continue

                    result = response.results[0]
                    if not result.alternatives:
                        continue

                    transcript = result.alternatives[0].transcript

                    # Emit transcription based on stability or finality
                    handler.emit_transcription(
                        transcript, 
                        is_final=result.is_final
                    )

            except Exception as e:
                logger.error(f"Error in process_audio_stream V2: {str(e)}")
                handler.emit_error(f"Transcription error: {str(e)}")
                handler.close()

        # Start processing in a separate thread
        threading.Thread(
            target=process_audio_stream,
            args=(stream_handler,),
            daemon=True
        ).start()
        
        socketio.emit('stream_started', {'status': 'success'}, room=request.sid)
        
    except Exception as e:
        logger.error(f"Error in start_audio_stream: {str(e)}")
        socketio.emit("error", {"message": str(e)}, room=request.sid)

@socketio.on("audio_chunk")
def handle_audio_chunk(data):
    """Handle incoming audio chunks from the client."""
    try:
        if request.sid in active_streams:
            stream = active_streams[request.sid]
            audio_data = base64.b64decode(data['audio'])
            stream.add_chunk(audio_data)
    except Exception as e:
        logger.error(f"Error in handle_audio_chunk: {str(e)}")
        socketio.emit("error", {"message": str(e)}, room=request.sid)

@socketio.on("stop_audio_stream")
def stop_audio_stream():
    """Stop the audio stream and clean up resources."""
    try:
        if request.sid in active_streams:
            stream = active_streams[request.sid]
            stream.close()
            del active_streams[request.sid]
            socketio.emit('stream_stopped', {'status': 'success'}, room=request.sid)
    except Exception as e:
        logger.error(f"Error in stop_audio_stream: {str(e)}")
        socketio.emit("error", {"message": str(e)}, room=request.sid)
