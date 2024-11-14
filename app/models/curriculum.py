from app.models import db
# Example model for curriculum

class Curriculum(db.Model):
    __tablename__ = 'curriculum'
    
    curriculum_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'))
    phonics = db.Column(db.JSON)
    sight_words = db.Column(db.JSON)
    other_topics = db.Column(db.JSON)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
