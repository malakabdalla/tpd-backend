from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class QuestionType(enum.Enum):
    repeat_words = 'repeat_words'
    repeat_sentence = 'repeat_sentence'
    complete_sentence = 'complete_sentence'
    repeat_paragraph = 'repeat_paragraph'
    complete_spelling = 'complete_spelling'
    find_word = 'find_word'

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
    

# Dummy data for users
users = [
    User(
        first_name="Alice",
        last_name="Smith",
        age=25,
        gender="Female",
        ethnicity="Caucasian",
        first_language="English",
        interests="Reading, Hiking, Yoga",
        personal_goals="Become proficient in Python programming.",
        milestone_completed=3,
        exercise_completed=12,
        question_completed=40,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    User(
        first_name="Bob",
        last_name="Johnson",
        age=30,
        gender="Male",
        ethnicity="African American",
        first_language="English",
        interests="Gaming, Basketball, Coding",
        personal_goals="Improve problem-solving skills.",
        milestone_completed=5,
        exercise_completed=20,
        question_completed=60,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    User(
        first_name="Carlos",
        last_name="Martinez",
        age=28,
        gender="Male",
        ethnicity="Hispanic",
        first_language="Spanish",
        interests="Soccer, Cooking, Technology",
        personal_goals="Learn cloud computing.",
        milestone_completed=2,
        exercise_completed=10,
        question_completed=25,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    User(
        first_name="Diana",
        last_name="Lee",
        age=23,
        gender="Female",
        ethnicity="Asian",
        first_language="Korean",
        interests="Painting, Running, Reading",
        personal_goals="Master data analysis techniques.",
        milestone_completed=4,
        exercise_completed=18,
        question_completed=50,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    User(
        first_name="Emily",
        last_name="Williams",
        age=35,
        gender="Female",
        ethnicity="Mixed",
        first_language="English",
        interests="Traveling, Music, Gardening",
        personal_goals="Develop leadership skills.",
        milestone_completed=6,
        exercise_completed=25,
        question_completed=70,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    User(
        first_name="Frank",
        last_name="O'Connor",
        age=40,
        gender="Male",
        ethnicity="Caucasian",
        first_language="English",
        interests="Writing, Philosophy, Chess",
        personal_goals="Publish a book.",
        milestone_completed=7,
        exercise_completed=30,
        question_completed=80,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    User(
        first_name="sam",
        last_name="david",
        age=30,
        gender="Male",
        ethnicity="Arab",
        first_language="Arabic",
        interests="Writing, Reading, WATCHING VIDEOS",
        personal_goals="Make an Ai App.",
        milestone_completed=7,
        exercise_completed=30,
        question_completed=90,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    User(
        first_name="Katherine",
        last_name="Oldcorner",
        age=40,
        gender="Female",
        ethnicity="Afghan",
        first_language="Afghany",
        interests="Writing, Philosophy, Chess",
        personal_goals="a happy family.",
        milestone_completed=7,
        exercise_completed=30,
        question_completed=80,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ),
    User(
        first_name="Joseph",
        last_name="Nugyen",
        age=23,
        gender="Male",
        ethnicity="vitnamese",
        first_language="English"    ,
        interests="computing, pottery, playing video games",
        personal_goals="be a streamer.",
        milestone_completed=7,
        exercise_completed=30,
        question_completed=80,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
]

# Add to database session
for user in users:
    db.session.add(user)

# Commit to save the users
db.session.commit()

class Module(db.Model):
    __tablename__ = 'module'

    module_id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    phonics = db.Column(JSONB, nullable=True, default=list)  # JSONB array
    sight_words = db.Column(JSONB, nullable=True, default=list)  # JSONB array
    other_topics = db.Column(JSONB, nullable=True, default=list)  # JSONB array

    exercises = db.relationship('Exercise', back_populates='module')

class Exercise(db.Model):
    __tablename__ = 'exercise'

    exercise_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    exercise_number = db.Column(db.Integer, nullable=False)
    exercise_name = db.Column(db.String, nullable=False)
    description = db.Column(JSONB) 
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
    question_type = db.Column(db.Enum('repeat_words', 'repeat_sentence', 'complete_sentence', 'repeat_paragraph', 'complete_spelling', 'find_word', name='question_type'), nullable=False)
    prompts = db.Column(JSONB) 
    data = db.Column(JSONB) 
    answers = db.Column(JSONB)
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
    hard_words = db.Column(db.Text)
                           
    user = db.relationship('User', back_populates='answers')
    question = db.relationship('Question', back_populates='answers_rel')
    exercise = db.relationship('Exercise', back_populates='answers')
    module = db.relationship('Module', back_populates='answers')

    

# Additional setup to ensure the `back_populates` work as expected
Module.answers = db.relationship('Answer', back_populates='module')
