from models.model import Question,Quiz,Chapter,Subject, db

def del_ques(ques_id):
    question_to_delete = Question.query.filter_by(uuid=ques_id).first()
    db.session.delete(question_to_delete)
    db.session.commit()
    return True


def del_quiz(quiz_id):
    questions = Question.query.filter_by(quiz_uuid=quiz_id).all()
    for question in questions:
        db.session.delete(question)
    
    quiz = Quiz.query.filter_by(uuid=quiz_id).first()
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
        return True
    return False

def del_chapter(chapter_id):
        quizzes = Quiz.query.filter_by(chapter_uuid=chapter_id).all()
        
        for quiz in quizzes:
            questions = Question.query.filter_by(quiz_uuid=quiz.uuid).all()
            for question in questions:
                db.session.delete(question)  
            db.session.delete(quiz)
        chapter = Chapter.query.filter_by(uuid=chapter_id).first()
        if chapter:
            db.session.delete(chapter)
            db.session.commit()  
            return True
        return False

def del_sub(subject_id):
        chapters = Chapter.query.filter_by(subject_uuid=subject_id).all()
        
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            
            for quiz in quizzes:
                questions = Question.query.filter_by(quiz_uuid=quiz.uuid).all()
                for question in questions:
                    db.session.delete(question)
                db.session.delete(quiz)
            db.session.delete(chapter)
        subject = Subject.query.filter_by(uuid=subject_id).first()
        if subject:
            db.session.delete(subject)
            db.session.commit()  
            return True 
        return False

