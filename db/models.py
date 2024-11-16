from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    ethnicity = db.Column(db.String(50))
    first_language = db.Column(db.String(50))
    interests = db.Column(db.Text)
    personal_goals = db.Column(db.Text)
    milestone_completed = db.Column(db.Integer)
    exercise_completed = db.Column(db.Integer)
    question_completed = db.Column(db.Integer)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    answers = db.relationship('Answer', back_populates='user')

class Module(db.Model):
    __tablename__ = 'module'

    module_id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    exercises = db.relationship('Exercise', back_populates='module')

class Exercise(db.Model):
    __tablename__ = 'exercise'

    exercise_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    exercise_number = db.Column(db.Integer, nullable=False)
    exercise_name = db.Column(db.String, nullable=False)
    description = db.Column(db.JSONB)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    module = db.relationship('Module', back_populates='exercises')
    questions = db.relationship('Question', back_populates='exercise')
    answers = db.relationship('Answer', back_populates='exercise')

class Question(db.Model):
    __tablename__ = 'question'

    question_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question_type = db.Column(db.Enum('repeat_word', 'repeat_sentence', 'repeat_paragraph', name='question_type'), nullable=False)
    prompts = db.Column(db.JSONB)
    data = db.Column(db.JSONB)
    answers = db.Column(db.JSONB)  # You may want to adjust the data type for this column
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    exercise = db.relationship('Exercise', back_populates='questions')
    answers_rel = db.relationship('Answer', back_populates='question')

class Answer(db.Model):
    __tablename__ = 'answer'

    answer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    answer_text = db.Column(db.String, nullable=False)
    audio_path = db.Column(db.String, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='answers')
    question = db.relationship('Question', back_populates='answers_rel')
    exercise = db.relationship('Exercise', back_populates='answers')
    module = db.relationship('Module', back_populates='answers')

# Additional setup to ensure the `back_populates` work as expected
Module.answers = db.relationship('Answer', back_populates='module')
