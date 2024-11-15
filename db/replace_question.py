from flask import Blueprint, request, jsonify
from db.models import db, Question, Exercise, QuestionType, Module

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/replace_question', methods=['PUT'])
def replace_question():
    try:
        # Get data from the request
        data = request.get_json()
        
        # Ensure that the necessary fields are provided
        if not all(key in data for key in ('module_number', 'exercise_number', 'question_id', 'question_type', 'prompts', 'data', 'answers')):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Find the exercise by module_number and exercise_number
        exercise = Exercise.query.join(Module).filter(
            Exercise.exercise_number == data['exercise_number'],
            Module.module_number == data['module_number']
        ).first()
        
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404
        
        # Find the question to replace using question_id
        question = Question.query.filter_by(question_id=data['question_id'], exercise_id=exercise.exercise_id).first()
        
        if not question:
            return jsonify({"error": "Question not found"}), 404
        
        # Update the question's details
        question.question_type = QuestionType[data['question_type']]  # Enum conversion
        question.prompts = data['prompts']
        question.data = data['data']
        question.answers = data['answers']
        
        # Commit the changes to the database
        db.session.commit()
        
        return jsonify({
            "message": "Question updated successfully",
            "question_id": question.question_id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
