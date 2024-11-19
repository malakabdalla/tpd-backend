from flask import Blueprint, request, jsonify
from .word import get_word
from .sentence import get_sentence
from .words_with_scores import transcribe_word_scores
from .text_to_speech import synthesize_speech_with_specific_voice
from app.config import logger
import base64


speech_blueprint = Blueprint('speech', __name__)


@speech_blueprint.route('/speak_text', methods=['POST'])
def speak_text():
    data = request.get_json()
    text = data['message']
    audio_content = synthesize_speech_with_specific_voice(text)
    audio_base64 = base64.b64encode(audio_content).decode('utf-8')
    return jsonify({"audio": audio_base64})

@speech_blueprint.route('/get_sentence', methods=['POST'])
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

@speech_blueprint.route('/get_word_scores', methods=['POST'])
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

@speech_blueprint.route('/get_word', methods=['POST'])
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
