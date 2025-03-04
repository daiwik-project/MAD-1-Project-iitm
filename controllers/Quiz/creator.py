from models.model import Quiz, Question, db
from datetime import datetime

def verify_prev_quiz(name, chapter_id):
    quiz = Quiz.query.filter_by(title=name, chapter_uuid=chapter_id).first()
    if quiz:
        return False
    return None

def cre_quiz(uuid, title, description, max_marks, correct_marks, negative_marks, chapter_id, scheduled_date, max_time, total_questions):
    scheduled_datetime = datetime.strptime(scheduled_date, '%Y-%m-%d')
    max_marks_int = int(max_marks)
    correct_marks_float = float(correct_marks)
    negative_marks_float = float(negative_marks)
    max_time_int = int(max_time)
    total_questions_int = int(total_questions)
    
    new_quiz = Quiz(
        uuid=uuid,
        title=title,
        description=description,
        max_score=max_marks_int,
        correct_score=correct_marks_float,
        wrong_score=negative_marks_float,
        chapter_uuid=chapter_id,
        scheduled_date=scheduled_datetime,
        duration_minutes=max_time_int,
        total_questions=total_questions_int
    )
    
    db.session.add(new_quiz)
    db.session.commit()
    return True

def cre_ques(uuid, quiz_id, question, option1, option2, option3, option4, correct_option,):
    new_question = Question(
        uuid=uuid,
        quiz_uuid=quiz_id,
        question_statement=question,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        correct_option=correct_option
    )
    
    db.session.add(new_question)
    db.session.commit()
    return True