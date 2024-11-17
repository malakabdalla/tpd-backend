from flask import Blueprint, request, jsonify
from .add_question import add_question
from .questions import get_questions
from .replace_question import replace_question

db_blueprint = Blueprint('db', __name__)

@db_blueprint.route('/add_question', methods=['POST'])
def add_question_route():
    data = request.get_json()
    return add_question(data)

@db_blueprint.route('/get_questions', methods=['GET'])
def get_questions_route():
    return get_questions()

@db_blueprint.route('/replace_question', methods=['POST'])
def replace_question_route():
    data = request.get_json()
    return replace_question(data)