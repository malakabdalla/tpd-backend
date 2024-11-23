from flask import jsonify
from .models import Answer, db

def add_hard_words(module_id, exercise_id, hard_words):
    # Ensure both module_id, exercise_id, and hard_words are provided
    if not module_id:
        return jsonify({"error": "module_id is required"}), 400

    if not exercise_id:
        return jsonify({"error": "exercise_id is required"}), 400

    if not hard_words:
        return jsonify({"error": "hard_words is required"}), 400

    # Ensure that hard_words is a list if multiple words are provided
    if isinstance(hard_words, str):
        hard_words = [hard_words]  # If it's a single word, make it a list

    # Fetch the answers that belong to the given module_id and exercise_id
    answers = Answer.query.filter(
        Answer.module_id == module_id,
        Answer.exercise_id == exercise_id
    ).all()

    # If no answers exist for the provided module_id and exercise_id
    if not answers:
        return jsonify({"error": "No answers found for the given module_id and exercise_id"}), 404

    # Update the hard_words column for each answer (you can decide how to assign)
    for answer in answers:
        # Append new hard words to the existing ones, if any
        existing_hard_words = answer.hard_words or ""  # Use empty string if no existing hard words
        # Combine existing and new hard words, ensuring no duplicates
        all_hard_words = set(existing_hard_words.split(", ") + hard_words)  # Use set to remove duplicates
        answer.hard_words = ", ".join(all_hard_words)  # Join all words back into a comma-separated string

    # Commit changes to the database
    db.session.commit()

    # Return a success message
    return jsonify({"message": "Hard words added successfully"}), 200
