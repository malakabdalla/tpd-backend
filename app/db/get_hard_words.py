from flask import jsonify
from .models import  Module, Answer, db

def get_hard_words(module_id):
    # Ensure module_id is provided
    if not module_id:
        return jsonify({"error": "module_id is required"}), 400

    # Query to get answers with related module data
    words = db.session.query(Answer).join(
        Module, Module.module_id == Answer.module_id
    ).filter(Answer.module_id == module_id).all()

    # If no hard words are found
    if not words:
        return jsonify([])  # Return an empty list if no hard words are found

    # Creating a list of hard words from the Answer model
    word_list = [
        {"hard_words": answer.hard_words} for answer in words
    ]

    # Return the results in a structured response
    return jsonify({"hard_words": word_list})
