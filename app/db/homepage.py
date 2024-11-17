from flask import jsonify
from .models import Module, Exercise, db

def get_homepage_data():
    # Query all modules from the database
    modules = db.session.query(Module).all()

    if not modules:  # Check if no modules are found
        return jsonify([])  # Return an empty list

    # Prepare the result as a list of module objects with their exercises
    result = []
    for module in modules:
        # Query exercises for each module
        exercises = db.session.query(Exercise).filter(Exercise.module_id == module.module_id).all()

        # Prepare the list of exercises for this module
        exercises_list = [
            {
                "exercise_id": exercise.exercise_id,
                "exercise_number": exercise.exercise_number,
                "exercise_name": exercise.exercise_name,
                # "description": exercise.description
            }
            for exercise in exercises
        ]

        # Create module object with its exercises
        module_data = {
            "module_id": module.module_id,
            "module_number": module.module_number,
            # "phonics": module.phonics,
            # "sight_words": module.sight_words,
            # "other_topics": module.other_topics,
            "exercises": exercises_list  # List of exercises
        }

        # Append module data to the result list
        result.append(module_data)

    return jsonify(result)
