#model/model.py
from datetime import datetime
from database import db

class User(db.Model):
    uuid = db.Column(db.String(12), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Subject(db.Model):
    uuid = db.Column(db.String(12), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chapters = db.relationship('Chapter', backref='subject')

class Chapter(db.Model):
    uuid = db.Column(db.String(12), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_uuid = db.Column(db.String(12), db.ForeignKey('subject.uuid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quiz(db.Model):
    uuid = db.Column(db.String(12), unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    max_score = db.Column(db.Integer, nullable=False)
    correct_score = db.Column(db.Float, nullable=False) 
    wrong_score = db.Column(db.Float, nullable=False) 
    chapter_uuid = db.Column(db.String(12), db.ForeignKey('chapter.uuid'), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_questions = db.Column(db.Integer, nullable=False)


class Question(db.Model):
    uuid = db.Column(db.String(12), unique=True, nullable=False, primary_key=True)
    quiz_uuid = db.Column(db.String(12), db.ForeignKey('quiz.uuid'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String, nullable=False)
    option2 = db.Column(db.String, nullable=False)
    option3 = db.Column(db.String, nullable=False)
    option4 = db.Column(db.String, nullable=False)
    correct_option = db.Column(db.CHAR, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserQuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(12), db.ForeignKey('user.uuid'), nullable=False)
    quiz_uuid = db.Column(db.String(12), db.ForeignKey('quiz.uuid'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False)
    attempt_number = db.Column(db.Integer, nullable=False)


class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(12), db.ForeignKey('user.uuid'), nullable=False)
    attempt_no = db.Column(db.Integer, db.ForeignKey('user_quiz_attempt.attempt_number'), nullable=False)
    quiz_uuid = db.Column(db.String(12), db.ForeignKey('quiz.uuid'), nullable=False) 
    question_uuid = db.Column(db.String(12), db.ForeignKey('question.uuid'), nullable=False)
    selected_option = db.Column(db.CHAR, nullable=False)
    is_correct = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
