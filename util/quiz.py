from models.model import  Subject, Chapter

def verify_subject(name):
    sub = Subject.query.filter_by(name=name).first()
    if sub:
        return False
    return None

def verify_chapter(name):
    ch = Chapter.query.filter_by(name=name).first()
    if ch:
        return False
    return None 

