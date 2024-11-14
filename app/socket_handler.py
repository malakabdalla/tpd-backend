import queue
import threading
import logging
from flask_socketio import SocketIO, emit

logger = logging.getLogger(__name__)

class AudioStreamHandler:
    def __init__(self, socket_id, sample_rate=16000):
        self.socket_id = socket_id
        self.sample_rate = sample_rate
        self.buffer = queue.Queue()
        self.closed = False
        self.is_recording = False
        self.audio_levels = []
        self.min_audio_chunks = 3
        self.timeout_duration = 1
        self.timeout_thread = None
        try:
            self.client = SpeechClient()
        except Exception as e:
            logger.error(f"Failed to initialize Speech client: {e}")
            raise

    def timeout_action(self):
        logger.debug(f"Timeout occurred for client {self.socket_id}")
        self.close()
        self.emit_timeout()

    def start_timeout(self):
        if self.timeout_thread is not None:
            self.timeout_thread.cancel()
        self.timeout_thread = threading.Timer(self.timeout_duration, self.timeout_action)
        self.timeout_thread.start()
        
    def add_chunk(self, chunk):
        if not self.closed:
            try:
                self.buffer.put(chunk, timeout=5)
            except queue.Full:
                logger.warning(f"Buffer full for client {self.socket_id}")
                self.emit_error("Processing buffer full - please try again")
            
    def close(self):
        if not self.closed:
            self.closed = True
            self.is_recording = False
            self.buffer.put(None)

    def generator(self):
        while not self.closed:
            try:
                chunk = self.buffer.get(timeout=30)
                if chunk is None:
                    return
                yield chunk
            except queue.Empty:
                self.close()
                return

    def emit_transcription(self, transcript):
        try:
            socketio.emit('transcription', {'transcript': transcript}, room=self.socket_id)
        except Exception as e:
            logger.error(f"Failed to emit transcription: {e}")

    def emit_error(self, error_message):
        try:
            socketio.emit('error', {'message': error_message}, room=self.socket_id)
        except Exception as e:
            logger.error(f"Failed to emit error: {e}")

    def emit_timeout(self):
        try:
            socketio.emit('timeout', {'message': 'timeout'}, room=self.socket_id)
        except Exception as e:
            logger.error(f"Failed to emit error: {e}")

@socketio.on("connect")
def handle_connect():
    """Handle new client connections."""
    logger.debug(f"Client connected: {request.sid}")
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
    logger.isEnabledFor(logging.DEBUG)
    """Initialize a new audio stream for transcription."""
    try:
        # Clean up any existing stream for this client
        if request.sid in active_streams:
            active_streams[request.sid].close()
            del active_streams[request.sid]

        # Create new stream handler for this client
        stream_handler = AudioStreamHandler(request.sid)
        active_streams[request.sid] = stream_handler

        phrase_set = cloud_speech.PhraseSet(
            phrases=[{"value": "by", "boost": 200}, {"value": "ran", "boost": 200}]
        )
        adaptation = cloud_speech.SpeechAdaptation(
            phrase_sets=[
                cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                    inline_phrase_set=phrase_set
                )
            ]
        )
        # Configure speech recognition
        config = cloud_speech.RecognitionConfig(
            # auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            adaptation=adaptation,
            encoding=cloud_speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=16000,
            language_code="en-GB",
            enable_automatic_punctuation=True,
            model="short",
        )
        # config = speech.RecognitionConfig(
        #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #     sample_rate_hertz=16000,
        #     language_code="en-GB",
        #     enable_automatic_punctuation=True,
        # )

        streaming_config = cloud_speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True
        )

        def process_audio_stream(handler):
            """Process audio stream and emit transcriptions."""
            try:
                audio_generator = handler.generator()
                requests = (cloud_speech.StreamingRecognizeRequest(audio_content=chunk)
                          for chunk in audio_generator)
                
                responses = handler.client.streaming_recognize(
                    streaming_config,
                    requests
                )

                for response in responses:
                    if handler.closed:
                        logger.info(f"Stream closed for client {handler.socket_id}")
                        break

                    handler.start_timeout()

                    if not response.results:
                        logger.isEnabledFor(logging.DEBUG)
                        continue

                    result = response.results[0]
                    if not result.alternatives:
                        continue

                    transcript = result.alternatives[0].transcript

                    if result.is_final or result.stability > 0.8:
                        logger.debug(f"result is_final Transcript: {transcript}")
                        handler.emit_transcription(transcript)

            except Exception as e:
                logger.error(f"Error in process_audio_stream: {str(e)}")
                handler.emit_error(f"Transcription error: {str(e)}")
                handler.close()


        # Start processing in a separate thread
        # threading.Thread(
        #     target=process_audio_stream,
        #     args=(stream_handler,),
        #     daemon=True
        # ).start()
        process_audio_stream(stream_handler)
        
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
    logger.isEnabledFor(logging.DEBUG)
    try:
        if request.sid in active_streams:
            logger.debug(f"Stopping audio stream for client {request.sid}")
            stream = active_streams[request.sid]
            stream.close()
            del active_streams[request.sid]
            socketio.emit('stream_stopped', {'status': 'success'}, room=request.sid)
    except Exception as e:
        logger.error(f"Error in stop_audio_stream: {str(e)}")
        socketio.emit("error", {"message": str(e)}, room=request.sid)


