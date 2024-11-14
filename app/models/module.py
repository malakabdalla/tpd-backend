from app.models import db 

class Module(db.Model):
    __tablename__ = 'module'
    module_id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, nullable=False)
    exercises = db.relationship('Exercise', backref='module', lazy=True)