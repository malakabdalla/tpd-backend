from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, ENUM
import enum, bcrypt

db = SQLAlchemy()

class QuestionType(enum.Enum):
    repeat_word = "repeat_word"
    repeat_sentence = "repeat_sentence"
    repeat_paragraph = "repeat_paragraph"

class Module(db.Model):
    __tablename__ = 'module'
    module_id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Exercise(db.Model):
    __tablename__ = 'exercise'
    exercise_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    exercise_number = db.Column(db.Integer, nullable=False)
    exercise_name = db.Column(db.String, nullable=False)
    description = db.Column(JSONB)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    module = db.relationship('Module', backref=db.backref('exercises', lazy=True))

class Question(db.Model):
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question_type = db.Column(ENUM(QuestionType), nullable=False)
    prompts = db.Column(JSONB)
    data = db.Column(JSONB)
    answers = db.Column(JSONB)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    exercise = db.relationship('Exercise', backref=db.backref('questions', lazy=True))

class Curriculum(db.Model):
    __tablename__ = 'curriculum'
    curriculum_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'))
    phonics = db.Column(db.JSON)
    sight_words = db.Column(db.JSON)
    other_topics = db.Column(db.JSON)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    module = db.relationship('Module', backref=db.backref('curricula', lazy=True))

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