from flask import Blueprint, request, jsonify
from speech.speech import synthesize_speech_with_specific_voice  # example import, replace as necessary
from ai.ai_functions import ai_answer_question, word_helper
from speech.word import get_word
from speech.sentence import get_sentence
from speech.words_with_scores import transcribe_word_scores
import logging

logger = logging.getLogger(__name__)

# Create a Blueprint for API endpoints
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/get_sentence', methods=['POST'])
def get_sentence_endpoint():
    audio_file = request.files['audio']
    phrase = request.form['phrase']
    logger.debug(f"get_word request: {phrase}")
    audio_content = audio_file.read()
    response = get_sentence(audio_content, phrase)
    logger.debug(f"get_word response: {response}")
    ret_val = []
    for result in response.results:
        for word_info in result.alternatives[0].words:
            ret_val.append({
                "word": word_info.word,
                "confidence": word_info.confidence
            })
    return ret_val

@api_blueprint.route('/get_word_scores', methods=['POST'])
def get_word_scores():
    audio_file = request.files['audio']
    audio_content = audio_file.read()
    result = transcribe_word_scores(audio_content)
    ret_val = []
    for result in result.results:
        for word_info in result.alternatives[0].words:
            ret_val.append({
                "word": word_info.word,
                "confidence": word_info.confidence
            })
    logger.debug(f"get_word_scores response: {result}")
    logger.debug(f"return value: {ret_val}")
    return ret_val

@api_blueprint.route('/get_word', methods=['POST'])
def get_word_endpoint():
    audio_file = request.files['audio']
    phrase = request.form['phrase']
    logger.debug(f"get_word request: {phrase}")
    audio_content = audio_file.read()
    response = get_word(audio_content, phrase)
    logger.debug(f"get_word response: {response}")
    logger.debug(f"get_word results: {response.results[0].alternatives[0].transcript}")
    result = response.results[0].alternatives[0].transcript
    return jsonify(result)

@api_blueprint.route('/answer_question', methods=['POST'])
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

@api_blueprint.route('/word_helper', methods=['POST'])
def word_helper_api():
    logger.isEnabledFor(logging.DEBUG)
    logger.debug("Word Helper API called")
    data = request.get_json()
    print(data)
    logger.debug(f"Data: {data}")
    word = data.get('word')
    if not word:
        return jsonify({'data': data}), 400
    logger.debug(f"Word Helper API called with word: {word}")
    response = word_helper(word)
    logger.debug(f"Word Helper API response: {response}")
    if type(response) == str:
        text_content = response
    else:
        text_content = response.content[0].text or response
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
    # result = {'message': 'success'}
    # Ensure the function returns a valid response
    # return jsonify(result)
# def run_http_server():
#     # Run the Flask app for HTTP on port 5000
#     app.run(host='0.0.0.0', port=8001)

# def run_socket_server():
#     # Run the Socket.IO server on port 5000
#     socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

@api_blueprint.route('/speak_text', methods=['POST'])
def speak_text():
    data = request.get_json()
    text = data['message']
    audio_content = synthesize_speech_with_specific_voice(text)
    audio_base64 = base64.b64encode(audio_content).decode('utf-8')
    return jsonify({"audio": audio_base64})