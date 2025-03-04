from datetime import datetime
from models.model import Quiz, Question, db

def update_ques(ques_id, up_ques, option_1, option_2, option_3, option_4, is_correct):
    i = Question.query.filter_by(uuid=ques_id).first()
    if i:
        i.question_statement = up_ques
        i.option1=option_1
        i.option2=option_2
        i.option3=option_3
        i.option4=option_4
        i.correct_option=is_correct
        db.session.commit()
        return True
    return False

def update_quiz_info(quiz_id, title, description, max_marks, correct_marks, negative_marks, scheduled_date, max_time, total_questions):
    quiz = Quiz.query.filter_by(uuid=quiz_id).first()
    if quiz:
        scheduled_date = datetime.strptime(scheduled_date, '%Y-%m-%d')

        quiz.title = title
        quiz.description = description
        quiz.max_score =max_marks
        quiz.correct_score =correct_marks
        quiz.wrong_score = negative_marks
        quiz.scheduled_date = scheduled_date
        quiz.duration_minutes = max_time
        quiz.total_questions = total_questions
        db.session.commit()
        return True
    return False
