from models.model import  Subject, Chapter, db

def update_chap_info(chapter_id, title, description):
    chap = Chapter.query.filter_by(uuid=chapter_id).first()
    if chap:
        chap.name = title
        chap.description = description
        db.session.commit()
        return True
    return False

def update_sub_info(subject_id, title, description):
    sub = Subject.query.filter_by(uuid=subject_id).first()
    if sub:
        sub.name = title
        sub.description = description
        db.session.commit()
        return True
    return False
