from flask import Blueprint, jsonify, request
from db.models import Question, Curriculum, Exercise, Module, db

api_blueprint_get = Blueprint('get_questions', __name__)

@api_blueprint_get.route('/get_questions', methods=['GET'])
def get_questions():
    # Get parameters from query string
    module_id = request.args.get('module_id')
    exercise_id = request.args.get('exercise_id')
    
    # Validate that both module_id and exercise_id are provided
    if not module_id or not exercise_id:
        return jsonify({"error": "module_id and exercise_id are required"}), 400
    
    # Query the Question, Exercise, and Module tables
    questions = db.session.query(Question, Exercise, Module).join(
        Exercise, Exercise.exercise_id == Question.exercise_id
    ).join(
        Module, Module.module_id == Exercise.module_id
    ).filter(
        Exercise.module_id == module_id,
        Question.exercise_id == exercise_id
    ).all()

    # If no questions are found, return an empty list
    if not questions:
        return jsonify([])

    # Prepare the list of questions with the required fields
    questions_list = [
        {
            "question_id": q[0].question_id,
            "question_number": q[0].question_number,
            "question_type": q[0].question_type.value,  # Access the enum value for question_type
            "prompts": q[0].prompts,
            "data": q[0].data,
            "answers": q[0].answers,
            "description": q[1].description,  # Get description from Exercise table
            "phonics": q[2].phonics,  # Get phonics from Module table
            "sight_words": q[2].sight_words,  # Get sight_words from Module table
            "other_topics": q[2].other_topics  # Get other_topics from Module table
        } for q in questions
    ]

    # Return the formatted list of questions as JSON
    return jsonify(questions_list)
