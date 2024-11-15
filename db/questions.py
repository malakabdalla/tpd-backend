from flask import Blueprint, jsonify, request
from models import Question, Curriculum, Exercise, Module, db

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/get_questions', methods=['GET'])
def get_questions():
    module_id = request.args.get('module_id')
    exercise_id = request.args.get('exercise_id')
    
    if not module_id or not exercise_id:
        return jsonify({"error": "module_id and exercise_id are required"}), 400
    
    # Query the Question, Exercise, and Curriculum tables
    questions = db.session.query(Question, Exercise, Curriculum).join(
        Exercise, Exercise.exercise_id == Question.exercise_id
    ).join(
        Curriculum, Curriculum.module_id == Exercise.module_id
    ).filter(
        Exercise.module_id == module_id,
        Question.exercise_id == exercise_id
    ).all()

    if not questions:  # Check if no questions are found
        return jsonify([])  # Return empty list

    questions_list = [
        {
            "question_id": q[0].question_id,
            "question_number": q[0].question_number,
            "question_type": q[0].question_type.value,  # Access enum value
            "prompts": q[0].prompts,
            "data": q[0].data,
            "answers": q[0].answers,
            "description": q[1].description,  # Get description from Exercise table
            "phonics": q[2].phonics,  # Get phonics from Curriculum table
            "sight_words": q[2].sight_words,  # Get sight_words from Curriculum table
            "other_topics": q[2].other_topics  # Get other_topics from Curriculum table
        } for q in questions
    ]

    return jsonify(questions_list)
