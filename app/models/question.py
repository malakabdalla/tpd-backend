from sqlalchemy.dialects.postgresql import ENUM
from flask_sqlalchemy import SQLAlchemy
import enum
from app.models import db 


# Define Python Enum matching your PostgreSQL ENUM
class QuestionType(enum.Enum):
    REPEAT_WORD = 'repeat_word'
    REPEAT_SENTENCE = 'repeat_sentence'
    REPEAT_PARAGRAPH = 'repeat_paragraph'

class Question(db.Model):
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    
    # This column maps to the PostgreSQL ENUM type
    question_type = db.Column(
        ENUM(QuestionType, name='question_type', create_type=False), 
        nullable=False
    )
    prompts = db.Column(db.JSON)  
    data = db.Column(db.JSON)     
    answers = db.Column(db.JSON)
