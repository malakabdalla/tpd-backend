from flask import Blueprint, request, jsonify
from .add_question import add_question
from .questions import get_questions
from .replace_question import replace_question
from .exercise_by_id import get_questions_by_exercise_id
from .homepage import get_homepage_data
from app.config import logger

db_blueprint = Blueprint('db', __name__)

@db_blueprint.route('/get_homepage_data', methods=['GET'])
def get_homepage_data_route():
    return get_homepage_data()

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

@db_blueprint.route('/get_exercise_by_id', methods=['GET'])
def get_question_by_exercise_id_route():
    exercise_id = request.args.get('exercise_id')
    logger.debug(f"exercise_id: {exercise_id}")
    return get_questions_by_exercise_id(exercise_id)

@db_blueprint.route('/add_hard_words', methods=['POST'])
def add_hard_words():
    data = request.get_json()
    module_id = data.get('module_id')
    exercise_id = data.get('exercise_id')
    hard_words = data.get('hard_words')
    return add_hard_words(module_id, exercise_id, hard_words)

@db_blueprint.route('/get_hard_words', methods=['GET'])
def get_hard_words():
    module_id = request.args.get('module_id')
    return get_hard_words(module_id)