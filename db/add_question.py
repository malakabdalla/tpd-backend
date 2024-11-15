from flask import Blueprint, request, jsonify
from db.models import db, Question, Exercise, QuestionType

api_blueprint = Blueprint('questions', __name__)

@api_blueprint.route('/add_question', methods=['POST'])
def add_question():
    try:
        # Get data from the request
        data = request.get_json()
        
        # Ensure that the necessary fields are provided
        if not all(key in data for key in ('module_number', 'exercise_number', 'question_type', 'prompts', 'data', 'answers')):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Find the exercise by module_number and exercise_number
        exercise = Exercise.query.join(Module).filter(
            Exercise.exercise_number == data['exercise_number'],
            Module.module_number == data['module_number']
        ).first()
        
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404
        
        # Find the next available question number for the exercise
        last_question = Question.query.filter_by(exercise_id=exercise.exercise_id).order_by(Question.question_number.desc()).first()
        next_question_number = last_question.question_number + 1 if last_question else 1
        
        # Create a new Question instance
        question = Question(
            exercise_id=exercise.exercise_id,
            question_number=next_question_number,
            question_type=QuestionType[data['question_type']],  # Enum conversion
            prompts=data['prompts'],
            data=data['data'],
            answers=data['answers']
        )
        
        # Add the question to the session and commit
        db.session.add(question)
        db.session.commit()
        
        return jsonify({
            "message": "Question added successfully",
            "question_id": question.question_id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
