from flask import Blueprint, request, jsonify
from .chatbot.repeat_words import repeat_words
from .word_helper import get_word_help
from .evaluate.repeat_words import evaluate_repeat_words_exercise
from .chatbot.complete_sentence import complete_sentence
from .chatbot.repeat_sentence import repeat_sentence
import re

ai_blueprint = Blueprint('ai', __name__)

@ai_blueprint.route('/new_chat', methods=['GET'])
def new_chat():
    global chat
    chat = []
    return jsonify(chat)

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
def helper_repeat_words():
    data = request.get_json()
    chat.append({"role": "user", "content": data['user_request']})  # Store as a dictionary
    
    if data['exercise_details']['question_type'] == 'repeat_sentence':
        response = re.search(r'<answer>(.*?)</answer>', repeat_sentence(data, chat, data['user_request']), re.DOTALL)
        return_val = {'response': response.group(1).strip()}
    elif data['exercise_details']['question_type'] == 'complete_sentence':
        response = re.search(r'<answer>(.*?)</answer>', complete_sentence(data, chat, data['user_request']), re.DOTALL)
        return_val = {'response': response.group(1).strip()}
    elif data['exercise_details']['question_type'] == 'repeat_words':
        response = re.search(r'<answer>(.*?)</answer>', repeat_words(data, chat, data['user_request']), re.DOTALL)
        return_val = {'response': response.group(1).strip()}
    
    chat.append({"role": "assistant", "content": return_val['response']})  # Store as a dictionary
    print(return_val)
    return return_val

e_chat = []
@ai_blueprint.route('/evaluate_repeat_words', methods=['POST'])
def evaluate_repeat_words():
    if len(e_chat) == 0:
        e_chat.append({"role": "user", "content": "evaluate the exercise"})
        e_chat.append({'role': 'assistant', 'content': """
                       <evaluation><summary>Great effort! I noticed you practiced the words "pay" and "train" more thoroughly than others. This shows good attention to getting the pronunciation just right. While you read through the remaining words smoothly, I'd be happy to provide some additional practice with similar 'ay' and 'ai' words if you'd like to strengthen those patterns even further. Would you like to try a few more similar words?</summary></evaluation>
                       """})
        e_chat.append({"role": "user", "content": "okay"})
    data = {'exercise_data': 
            {'exercise_name': 'Reading long vowel sounds',
             'Description': """Remember that vowel sounds can be long or short. The 
             long vowel sounds are ā, ē, ō, ĩ and ũ', "the short ones are a, e, i, o, 
             and u. In this activity you'll be reading words containing long vowel 
             sounds. There are seven words for each long vowel sound and all the letter 
             combinations you've learnt so far for each sound will feature here. Read each 
             word as it appears on the screen"""},
             'questions': [{'Question Number': 1, 'Question Type': 'repeat_words', 'Prompts': ['ai, ay'], 'Data': ['pay', 'train', 'wait', 'ray', 'gay', 'chain', 'tail'] }],
             'User interactions': {'pay': 5, 'train': 5, 'wait': 1, 'ray': 1, 'gay': 1, 'chain': 1, 'tail': 1},
            'sight_words': """so work love their one over sure two knew because only woman done does other"""}
    result = evaluate_repeat_words_exercise(data, e_chat)
    print(result)
    return result

# @ai_blueprint.route('/helper_complete_sentence', methods=['POST'])
# def helper_complete_sentence():
#     data = {'exercise_details': 
#             {'exercise_name': 'Fill in the missing words',
#              'Description': """In this exercise, you will be asked to complete sentences 
#              by filling in the missing words. The sentences are simple and relate to 
#              everyday activities. Your task is to think about the context of the sentence 
#              and choose the most appropriate word to complete it."""}, 
