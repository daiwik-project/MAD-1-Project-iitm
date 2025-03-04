# Controllers/Auth/user.py
from models.model import User, db


def previous_username(id):
    user = User.query.filter_by(username=id).first()
    return user.username if user else None

def previous_email(id):
    user = User.query.filter_by(email=id).first()
    return user.email if user else None


def create_user(uuid, username, email, password):
    user = User(uuid=uuid, username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

def verify_user(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return True
    return False

def find_user_id(username):
    user = User.query.filter_by(username=username).first()
    return user.uuid if user else None