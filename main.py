from flask_socketio import SocketIO, emit
from google.cloud import speech
import queue
import threading
import base64
from datetime import datetime
import logging
from engineio.async_drivers import threading as async_threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from speech import synthesize_speech_with_specific_voice
from ai_functions import ai_answer_question, word_helper
from functools import partial
from timeout_decorator import timeout


logging.basicConfig(level=logging.CRITICAL)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    logger=False,
    engineio_logger=False,
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=1e8,
    always_connect=True,
    http_compression=False
)



class AudioStreamHandler:
    def __init__(self, socket_id, sample_rate=16000):
        self.socket_id = socket_id
        self.sample_rate = sample_rate
        self.buffer = queue.Queue()
        self.closed = False
        self.is_recording = False
        self.audio_levels = []  
        self.min_audio_chunks = 3  # Minimum number of chunks to calculate average
        self.timeout_duration = 1
        self.timeout_thread = None
        try:
            self.client = speech.SpeechClient()
        except Exception as e:
            logger.error(f"Failed to initialize Speech client: {e}")
            raise


    def timeout_action(self):
        """Function to call when timeout occurs."""
        logger.isEnabledFor(logging.DEBUG)
        logger.debug(f"Timeout occurred for client {self.socket_id}")
        self.close()
        self.emit_timeout()

    def start_timeout(self):
        """Start a timeout thread that will call timeout_action."""
        if self.timeout_thread is not None:
            self.timeout_thread.cancel()
        self.timeout_thread = threading.Timer(self.timeout_duration, self.timeout_action)
        self.timeout_thread.start()
        
    def add_chunk(self, chunk):
        logger.isEnabledFor(logging.DEBUG)
        """Add an audio chunk to the buffer and update audio levels"""
        if not self.closed:
            try:
                self.buffer.put(chunk, timeout=5)
                
            except queue.Full:
                logger.warning(f"Buffer full for client {self.socket_id}")
                self.emit_error("Processing buffer full - please try again")
            
    def close(self):
        """Close the stream and cleanup."""
        if not self.closed:
            self.closed = True
            self.is_recording = False
            self.buffer.put(None)

    def generator(self):
        """Generate audio chunks from the buffer."""
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
        logger.isEnabledFor(logging.DEBUG)
        """Emit transcription using Socket.IO."""
        try:
            socketio.emit('transcription', {'transcript': transcript}, room=self.socket_id)
        except Exception as e:
            logger.error(f"Failed to emit transcription: {e}")

    def emit_error(self, error_message):
        """Emit error using Socket.IO."""
        try:
            socketio.emit('error', {'message': error_message}, room=self.socket_id)
        except Exception as e:
            logger.error(f"Failed to emit error: {e}")

    def emit_timeout(self):
        """Emit Timeout"""
        try:
            socketio.emit('timeout', {'message': 'timeout'}, room=self.socket_id)
        except Exception as e:
            logger.error(f"Failed to emit error: {e}")

# Dictionary to store active streams for each client
active_streams = {}

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

        # MODIFICATION: Expanded MIME type support
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,  # Keep as primary
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        # Alternative encoding (commented out, but available)
        # config = speech.RecognitionConfig(
        #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #     sample_rate_hertz=16000,
        #     language_code="en-US",
        #     enable_automatic_punctuation=True,
        # )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True
        )

        def process_audio_stream(handler):
            """Process audio stream and emit transcriptions."""
            try:
                audio_generator = handler.generator()
                requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
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
                        continue

                    result = response.results[0]
                    if not result.alternatives:
                        continue

                    transcript = result.alternatives[0].transcript

                    # MODIFICATION: More robust transcription handling
                    if result.is_final or (result.stability and result.stability > 0.8):
                        logger.debug(f"Final Transcript: {transcript}")
                        handler.emit_transcription(transcript)

            except Exception as e:
                logger.error(f"Error in process_audio_stream: {str(e)}")
                handler.emit_error(f"Transcription error: {str(e)}")
                handler.close()

        # Run synchronously - uncomment thread version if needed
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
            
            # MODIFICATION: More robust base64 decoding
            try:
                audio_data = base64.b64decode(data['audio'])
            except (KeyError, TypeError) as decode_error:
                logger.error(f"Base64 decoding error: {str(decode_error)}")
                return

            stream.add_chunk(audio_data)
    except Exception as e:
        logger.error(f"Error in handle_audio_chunk: {str(e)}")
        socketio.emit("error", {"message": str(e)}, room=request.sid)

@socketio.on("end_audio_stream")
def end_audio_stream():
    """Handle ending of audio stream."""
    try:
        if request.sid in active_streams:
            stream = active_streams[request.sid]
            stream.close()
            del active_streams[request.sid]
            logger.info(f"Audio stream ended for client {request.sid}")
    except Exception as e:
        logger.error(f"Error in end_audio_stream: {str(e)}")

@app.route('/speak_text', methods=['POST'])
def speak_text():
    data = request.get_json()
    text = data['message']
    audio_content = synthesize_speech_with_specific_voice(text)
    audio_base64 = base64.b64encode(audio_content).decode('utf-8')
    return jsonify({"audio": audio_base64})

# request_lock = threading.Lock()

# @timeout(30, use_signals=False)
@app.route('/answer_question', methods=['POST'])
def answer_question():
    # if not request_lock.acquire(blocking=False):
    #     return jsonify({'error': 'Request in progress'}), 429
    try:
        data = request.get_json()
        user_message = data['question']
        chat = data['chat']
        response = ai_answer_question(user_message, chat)
        # print('\n\n:: ', response, '\n\n')

        # Extract the text content from the response
        text_content = response.content[0].text

        # Use regular expressions to extract response and continue values
        response_match = re.search(r'<response>(.*?)</response>', text_content, re.DOTALL)
        continue_match = re.search(r'<continue>(.*?)</continue>', text_content, re.DOTALL)

        if response_match and continue_match:
            response_text = response_match.group(1).strip()
            continue_value = continue_match.group(1).strip().lower() == 'true'

            ret_val = {'message': response_text, 'continue': continue_value}
            # print(ret_val['continue'])
            # print(ret_val)
        #     return ret_val
        # else:
        #     return {'error': 'Failed to parse response'}
        response_text = response_match.group(1).strip()
        continue_value = continue_match.group(1).strip().lower() == 'true'


        # Generate the audio content
        audio_content = synthesize_speech_with_specific_voice(response_text)

        # Encode audio content in Base64 for JSON compatibility
        audio_base64 = base64.b64encode(audio_content).decode('utf-8')

        # Create a JSON response with audio and additional text fields
        response_data = {
            "audio": audio_base64,
            "message": response_text,
            "continue": continue_value
        }

        return jsonify(response_data)
    finally:
        logger.info(f"Answer Question API called with question: {user_message}")
    #     request_lock.release()

@app.route('/word_helper', methods=['POST'])
def word_helper_api():
    data = request.get_json()
    word = data['word']
    logger.info(f"Word Helper API called with word: {word}")
    response = word_helper(word)
    logger.info(f"Word Helper API response: {response}")
    text_content = response.content[0].text
    description_match = re.search(r'<description>(.*?)</description>', text_content, re.DOTALL)
    example_sentence_match = re.search(r'<example_sentence>(.*?)</example_sentence>', text_content, re.DOTALL)
    similar_sounds_match = re.search(r'<similar_sounds>(.*?)</similar_sounds>', text_content, re.DOTALL)
    description_text = description_match.group(1).strip()
    example_text = example_sentence_match.group(1).strip()
    similar_text = similar_sounds_match.group(1).strip()
    response_data = {
        "description": description_text,
        "example_sentence": example_text,
        "similar_sounds": similar_text
    }
    
    return jsonify(response_data)
# def run_http_server():
#     # Run the Flask app for HTTP on port 5000
#     app.run(host='0.0.0.0', port=8001)

# def run_socket_server():
#     # Run the Socket.IO server on port 5000
#     socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
    # Start HTTP server in a separate thread
    # http_thread = threading.Thread(target=run_http_server)
    # http_thread.start()

    # # Run Socket.IO server in main thread
    # run_socket_server()
