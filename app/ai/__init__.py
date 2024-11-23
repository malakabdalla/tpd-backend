from flask import Blueprint, request, jsonify
from .word_helper import get_word_help
from .evaluate.eval_repeat_words import eval_repeat_words
from .chatbot.chat_complete_sentence import chat_complete_sentence
from .chatbot.chat_repeat_sentence import chat_repeat_sentence
from .chatbot.chat import chatbot
import re
from app.config import logger
from .generator.gen_complete_sentence import GameFillGap
from .generator.basic_comprehention import GameComprehension

ai_blueprint = Blueprint('ai', __name__)

@ai_blueprint.route('/final', methods=['POST'])
def final():
    data = request.json
    response = GameComprehension(data['hard_words'])
    return jsonify(response)

@ai_blueprint.route('/generate', methods=['POST'])
def generate():
    data = request.json
    response = GameFillGap()
    return jsonify(response)

@ai_blueprint.route('/new_chat', methods=['GET'])
def new_chat():
    print("New chat")

@ai_blueprint.route('/ai_helper', methods=['POST'])
def ai_helper():
    data = request.json
    print(data)
    return jsonify(data)

@ai_blueprint.route('/word_helper', methods=['POST'])
def word_helper_api():
    data = request.get_json()
    return get_word_help(data)

@ai_blueprint.route('/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.get_json()
    chat = data.get('chat', [])
    try:
        response = chatbot(data, chat, data['user_request'])  # Ensure chatbot returns valid data
        if response:
            return_val = {'response': response, 'chat': chat}
        else:
            return_val = {'response': "No valid answer found", 'chat': chat}
    except Exception as e:
        print("Error during chatbot processing:", e)
        return_val = {'response': "Nope, there was an error", 'chat': chat}

    return return_val

@ai_blueprint.route('/evaluate', methods=['POST'])
def evaluate_repeat_words():
    data = request.get_json()
    chat = data.get('chat', [])
    print(chat)
    result = eval_repeat_words(data, chat)
    print(result)
    logger.info(result)
    evaluation_match = re.search(r'<evaluation>(.*?)</evaluation>', result, re.DOTALL)
    add_words_match = re.search(r'<add_words>(.*?)</add_words>', result, re.DOTALL)

    evaluation = evaluation_match.group(1).strip() if evaluation_match else None
    add_words = (
        [word.strip() for word in add_words_match.group(1).split(',')]
        if add_words_match
        else None
    ) 
    logger.info(data)
    response = {
        "response": evaluation,
        "includes_questions": bool(add_words),
        "question": {
            "data": add_words if add_words else [],
            "answer_list": add_words if add_words else [],
            "question_type": data.get("exercise_details", {}).get("questions", [{}])[0].get("question_type", None),  # Access question_type safely from the first question
            "prompts": data.get("exercise_details", {}).get("questions", [{}])[0].get("prompts", []),  
            "quesition_id": "ai_generated"
        }
    }
    return response