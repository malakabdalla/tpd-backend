from flask import Blueprint, request, jsonify
from .chatbot.repeat_words import repeat_words
from .word_helper import get_word_help
from .anthropic_calls import AnthropicCalls
from .evaluate.repeat_words import evaluate_repeat_words_exercise
from .chatbot.complete_sentence import complete_sentence
import re

ai_blueprint = Blueprint('ai', __name__)

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
    return_val = None
    data = request.get_json()
    if data['exercise_details']['question_type'] == 'complete_sentence':
        response = re.search(r'<answer>(.*?)</answer>', complete_sentence(data), re.DOTALL)
        print(response)
        return_val = {'response': response.group(1).strip()}
    if data['exercise_details']['question_type'] == 'repeat_words':
        response = re.search(r'<answer>(.*?)</answer>', repeat_words(data), re.DOTALL)
        return_val = {'response': response.group(1).strip()}
    print(return_val)
    return return_val

@ai_blueprint.route('/evaluate_repeat_words', methods=['POST'])
def evaluate_repeat_words():
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
    return jsonify(evaluate_repeat_words_exercise(data))

# @ai_blueprint.route('/helper_complete_sentence', methods=['POST'])
# def helper_complete_sentence():
#     data = {'exercise_details': 
#             {'exercise_name': 'Fill in the missing words',
#              'Description': """In this exercise, you will be asked to complete sentences 
#              by filling in the missing words. The sentences are simple and relate to 
#              everyday activities. Your task is to think about the context of the sentence 
#              and choose the most appropriate word to complete it."""}, 
