from flask import Blueprint, jsonify, request
from .models import Question, Exercise, Module, db

def get_questions_by_exercise_id(exercise_id):

    if not exercise_id:
        return jsonify({"error": "exercise_id is required"}), 400

    # Query to get questions along with related Exercise and Module data
    questions = db.session.query(Question, Exercise, Module).join(
        Exercise, Exercise.exercise_id == Question.exercise_id
    ).join(
        Module, Module.module_id == Exercise.module_id
    ).filter(
        Question.exercise_id == exercise_id
    ).all()

    if not questions:
        return jsonify([])  # Return an empty list if no questions are found

    # Extracting data from the first matched Exercise and Module
    result = {
        "description": questions[0][1].description,  # From Exercise
        "phonics": questions[0][2].phonics,          # From Module
        "sight_words": questions[0][2].sight_words,  # From Module
        "other_topics": questions[0][2].other_topics # From Module
    }

    # Creating a list of questions with relevant fields from the Question model
    questions_list = [
        {
            "question_id": q[0].question_id,
            "question_number": q[0].question_number,
            "question_type": q[0].question_type,
            "prompts": q[0].prompts,
            "data": q[0].data,
            "answers": q[0].answers,
        } for q in questions
    ]

    # Combine extracted data with the list of questions
    result["questions"] = questions_list

    return jsonify(result)
