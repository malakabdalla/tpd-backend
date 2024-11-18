from flask import Blueprint, request, jsonify
from .ai_helper import repeat_word
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
    data = request.get_json()
    return repeat_word(data)