from flask import Blueprint, request, jsonify
from .ai_helper.repeat_word import repeat_word
from .word_helper import get_word_help
from .anthropic_calls import AnthropicCalls

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

@ai_blueprint.route('/helper_repeat_word', methods=['POST'])
def helper_repeat_word():
    data = {'exercise_details': 
            {'exercise_name': 'Reading long vowel sounds',
             'data' : ['week', ' speak', ' happy', 'keen', 'sorry', 'cheat', 'tree'],
             'Description': """Remember that vowel sounds can be long or short. The 
             long vowel sounds are ā, ē, ō, ĩ and ũ', "the short ones are a, e, i, o, 
             and u. In this activity you'll be reading words containing long vowel 
             sounds. There are seven words for each long vowel sound and all the letter 
             combinations you've learnt so far for each sound will feature here. Read each 
             word as it appears on the screen"""}, 
            'sight_words': """so work love their one over sure two knew because only woman done does other""", 
            'user_request': 'Why have you grouped all of these words together?'}
    return jsonify(repeat_word(data))