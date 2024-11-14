from app.models import db 

class Exercise(db.Model):
    __tablename__ = 'exercise'
    exercise_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    exercise_number = db.Column(db.Integer, nullable=False)
    exercise_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.JSON)  # You can store structured data here

    questions = db.relationship('Question', backref='exercise', lazy=True)