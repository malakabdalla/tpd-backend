from flask import Blueprint, request, jsonify
from .word_helper import get_word_help
from .evaluate.eval_repeat_words import eval_repeat_words
from .chatbot.chat_complete_sentence import chat_complete_sentence
from .chatbot.chat_repeat_sentence import chat_repeat_sentence
from .chatbot.chat import chatbot
import re
from app.config import logger
from .generator.gen_complete_sentence import GameFillGap

ai_blueprint = Blueprint('ai', __name__)

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
    result = eval_repeat_words(data, chat)
    print(result)
    logger.info(result)
    evaluation_match = re.search(r'<evaluation>(.*?)</evaluation>', result, re.DOTALL)
    add_words_match = re.search(r'<add_words>(.*?)</add_words>', result, re.DOTALL)

    # Extracting the string value or setting it to None if no match
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

# @ai_blueprint.route('/helper_complete_sentence', methods=['POST'])
# def helper_complete_sentence():
#     data = {'exercise_details': 
#             {'exercise_name': 'Fill in the missing words',
#              'Description': """In this exercise, you will be asked to complete sentences 
#              by filling in the missing words. The sentences are simple and relate to 
#              everyday activities. Your task is to think about the context of the sentence 
#              and choose the most appropriate word to complete it."""}, 


    # data = {'exercise_data': 
    #         {'exercise_name': 'Reading long vowel sounds',
    #          'Description': """Remember that vowel sounds can be long or short. The 
    #          long vowel sounds are ā, ē, ō, ĩ and ũ', "the short ones are a, e, i, o, 
    #          and u. In this activity you'll be reading words containing long vowel 
    #          sounds. There are seven words for each long vowel sound and all the letter 
    #          combinations you've learnt so far for each sound will feature here. Read each 
    #          word as it appears on the screen"""},
    #          'questions': [{'Question Number': 1, 'Question Type': 'repeat_words', 'Prompts': ['ai, ay'], 'Data': ['pay', 'train', 'wait', 'ray', 'gay', 'chain', 'tail'] }],
    #          'User interactions': {'pay': 5, 'train': 5, 'wait': 1, 'ray': 1, 'gay': 1, 'chain': 1, 'tail': 1},
    #         'sight_words': """so work love their one over sure two knew because only woman done does other"""}
