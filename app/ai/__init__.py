from flask import Blueprint, request, jsonify
from .ai_helper import repeat_word
from .word_helper import get_word_help
from .anthropic_calls import AnthropicCalls
import os
from dotenv import load_dotenv
import logging

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

LLM_calls = AnthropicCalls(api_key=ANTHROPIC_API_KEY, stream=True)

logger = logging.getLogger(__name__)
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