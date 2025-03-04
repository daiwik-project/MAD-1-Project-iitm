from models.model import User, db


def user_info(id):
    a = User.query.filter_by(uuid=id).first()
    return a

def update_user_profile_info(email, password, id):
    person = User.query.filter_by(uuid=id).first()
    if person:
        person.email = email
        person.password = password
        db.session.commit()
        return True
    return False
