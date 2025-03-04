# controllers\admin\create.py
from models.model import  Subject, Chapter, db

def cre_subject(id, name, description):
    new_subject = Subject(uuid=id, name=name, description=description)
    db.session.add(new_subject)
    db.session.commit()
    return True

def cre_chapter(id, name, description, subject_id):
    new_chapter = Chapter(uuid=id, name=name, description=description, subject_uuid=subject_id)
    db.session.add(new_chapter)
    db.session.commit()
    return True