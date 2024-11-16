from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, ENUM
import enum, bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

db = SQLAlchemy()

class QuestionType(enum.Enum):
    repeat_word = "repeat_word"
    repeat_sentence = "repeat_sentence"
    repeat_paragraph = "repeat_paragraph"

class Module(db.Model):
    __tablename__ = 'module'
    
    module_id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, nullable=False, unique=True)
    phonics = db.Column(JSON)  # Assuming phonics data is JSON
    sight_words = db.Column(JSON)  # Assuming sight_words data is JSON
    other_topics = db.Column(JSON)  # Assuming other_topics data is JSON
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship
    exercises = db.relationship('Exercise', backref='module', lazy=True)  # One module has many exercises

# Exercise Table
class Exercise(db.Model):
    __tablename__ = 'exercise'
    
    exercise_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    exercise_number = db.Column(db.Integer, nullable=False)
    exercise_name = db.Column(db.String, nullable=False)
    description = db.Column(JSON)  # Assuming description is a JSON object
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship
    questions = db.relationship('Question', backref='exercise', lazy=True)  # One exercise has many questions

# Question Table
class Question(db.Model):
    __tablename__ = 'question'
    
    question_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question_type = db.Column(Enum(QuestionType), nullable=False)  # Using Enum for question types
    prompts = db.Column(JSON)  # Assuming prompts is a JSON object
    data = db.Column(JSON)  # Assuming data is a JSON object
    answers = db.Column(JSON)  # Assuming answers is a JSON object
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship
    answers = db.relationship('Answer', backref='question', lazy=True)  # One question can have many answers

# Answer Table
class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    answer_text = db.Column(db.String, nullable=False)  # The user's answer text
    audio_path = db.Column(db.String, nullable=True)  # Path to the audio file, can be NULL if not provided
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())

    # Relationships
    user = db.relationship('User', back_populates='answers')
    question = db.relationship('Question', back_populates='answers')
    exercise = db.relationship('Exercise', back_populates='answers')
    module = db.relationship('Module', back_populates='answers')
    
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

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    