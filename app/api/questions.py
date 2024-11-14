from flask import Blueprint, jsonify, request
from app.models.question import Question
from app.models.exercise import Exercise  # Assuming you have an Exercise model defined
from app.models.module import Module  # Assuming you have a Module model defined
from app.models import db  # Ensure db is imported

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/get_questions', methods=['GET'])
def get_questions():
    module_id = request.args.get('module_id')
    exercise_id = request.args.get('exercise_id')
    
    if not module_id or not exercise_id:
        return jsonify({"error": "module_id and exercise_id are required"}), 400
    
    # Assuming relationships are properly defined, otherwise query separately
    questions = Question.query.join(Exercise).filter(
        Exercise.module_id == module_id,
        Question.exercise_id == exercise_id
    ).all()

    if not questions:  # Check if no questions are found
           return jsonify([])  # Return empty list

    questions_list = [
        {
            "question_id": q.question_id,
            "question_number": q.question_number,
            "question_type": q.question_type.value,  # Access enum value
            "prompts": q.prompts,
            "data": q.data,
            "answers": q.answers
        } for q in questions
    ]
    return jsonify(questions_list)
