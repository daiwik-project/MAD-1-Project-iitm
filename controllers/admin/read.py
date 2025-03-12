# controllers\admin\create.py
from models.model import  Subject, Chapter, db

def admin_dashboard_view():
    subjects_info = Subject.query.with_entities(Subject.name, Subject.description, Subject.uuid).all()
    chapters_info = Chapter.query.with_entities(Chapter.name, Chapter.subject_uuid).all()
    result = []
    for subject in subjects_info:
        subject_data = [subject.uuid, subject.name, subject.description, []] 
        for chapter in chapters_info:
            if chapter.subject_uuid == subject.uuid:
                subject_data[3].append(chapter.name)  
        result.append(subject_data)
    return result


def get_subj_des(subj_id):
    subject = Subject.query.filter_by(uuid=subj_id).first()
    return subject.description if subject else None

def get_chap(subject_id):
    chapters  = Chapter.query.filter_by(subject_uuid=subject_id).all()
    if chapters:
        return [[chapter.uuid, chapter.name, chapter.description] for chapter in chapters]  
    return None 