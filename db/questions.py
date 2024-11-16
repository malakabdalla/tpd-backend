from flask import Blueprint, jsonify, request
from db.models import Question, Exercise, Module, db

api_blueprint_get = Blueprint('get_questions', __name__)

@api_blueprint_get.route('/get_questions', methods=['GET'])
def get_questions():
    module_number = request.args.get('module_number')
    exercise_number = request.args.get('exercise_number')
    
    if not module_number or not exercise_number:
        return jsonify({"error": "module_number and exercise_number are required"}), 400

    # Retrieve the module_id based on module_number
    module = db.session.query(Module).filter(Module.module_number == module_number).first()
    if not module:
        return jsonify({"error": f"Module with number {module_number} not found"}), 404

    # Retrieve the exercise_id based on exercise_number and module_id
    exercise = db.session.query(Exercise).filter(
        Exercise.exercise_number == exercise_number,
        Exercise.module_id == module.module_id
    ).first()
    
    if not exercise:
        return jsonify({"error": f"Exercise with number {exercise_number} not found in module {module_number}"}), 404
    
    # Now query the Question, Exercise, and Module tables
    questions = db.session.query(Question, Exercise, Module).join(
        Exercise, Exercise.exercise_id == Question.exercise_id
    ).join(
        Module, Module.module_id == Exercise.module_id
    ).filter(
        Exercise.module_id == module.module_id,
        Question.exercise_id == exercise.exercise_id
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
            "phonics": q[2].phonics,  # Get phonics from Module table
            "sight_words": q[2].sight_words,  # Get sight_words from Module table
            "other_topics": q[2].other_topics  # Get other_topics from Module table
        } for q in questions
    ]

    return jsonify(questions_list)
