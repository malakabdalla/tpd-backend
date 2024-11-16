from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from datetime import datetime
import bcrypt
import enum

db = SQLAlchemy()

# Enum for Question Types
class QuestionType(enum.Enum):
    repeat_word = "repeat_word"
    repeat_sentence = "repeat_sentence"
    repeat_paragraph = "repeat_paragraph"

# Module Table
class Module(db.Model):
    __tablename__ = 'module'

    module_id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, nullable=False, unique=True)
    phonics = db.Column(JSONB)  # JSONB field for phonics
    sight_words = db.Column(JSONB)  # JSONB field for sight words
    other_topics = db.Column(JSONB)  # JSONB field for other topics
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship with Exercise
    exercises = db.relationship('Exercise', backref='module', lazy=True)

# Exercise Table
class Exercise(db.Model):
    __tablename__ = 'exercise'

    exercise_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    exercise_number = db.Column(db.Integer, nullable=False)
    exercise_name = db.Column(db.String, nullable=False)
    description = db.Column(JSONB)  # JSONB field for description
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship with Question
    questions = db.relationship('Question', backref='exercise', lazy=True)

# Question Table
class Question(db.Model):
    __tablename__ = 'question'

    question_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question_type = db.Column(ENUM(QuestionType), nullable=False)  # ENUM type for question types
    prompts = db.Column(JSONB)  # JSONB field for prompts
    data = db.Column(JSONB)  # JSONB field for data
    answers = db.Column(JSONB)  # JSONB field for answers (this can store predefined answers, etc.)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship with Answer
    answers_rel = db.relationship('Answer', backref='question', lazy=True)

# Answer Table
class Answer(db.Model):
    __tablename__ = 'answers'

    answer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    answer_text = db.Column(db.String, nullable=False)  # User's answer text
    audio_path = db.Column(db.String, nullable=True)  # Path to audio file (nullable)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship with User
    user = db.relationship('User', back_populates='answers')
    question = db.relationship('Question', back_populates='answers_rel')
    exercise = db.relationship('Exercise', back_populates='answers')
    module = db.relationship('Module', back_populates='answers')

# User Table
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False, default=18)
    milestone_completed = db.Column(db.Integer, nullable=False, default=0)
    exercise_completed = db.Column(db.Integer, nullable=False, default=0)
    question_completed = db.Column(db.Integer, nullable=False, default=0)
    gender = db.Column(db.String(50), nullable=False, default='Not specified')
    ethnicity = db.Column(db.String(100), nullable=False, default='Not specified')
    first_language = db.Column(db.String(100), nullable=False, default='Not specified')
    interests = db.Column(db.String(255), nullable=False, default='Not specified')
    personal_goals = db.Column(db.String(255), nullable=False, default='Not specified')
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    password_hash = db.Column(db.String(255), nullable=False)

    # Password hashing and checking
    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    # Relationship with Answers
    answers = db.relationship('Answer', back_populates='user')

