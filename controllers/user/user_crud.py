from models.model import Chapter, Quiz, Subject, UserQuizAttempt, Question, UserAnswer, db
from datetime import datetime

def get_sub():
    subjects = Subject.query.with_entities(Subject.uuid, Subject.name).distinct().all()
    print(subjects)
    return subjects

def get_subject_chapter_course_details(user_id):
    subjects = Subject.query.all()
    result = []
    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        chapter_details = []
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            quiz_details = []
            for quiz in quizzes:
                attempt_count = 0
                if user_id:
                    attempt_count = UserQuizAttempt.query.with_entities(UserQuizAttempt.attempt_number).filter_by(
                        user_uuid=user_id,
                        quiz_uuid=quiz.uuid
                    ).first()
                    ac = 0
                    if attempt_count:
                        for i in attempt_count:
                            if i > ac:  
                                ac = i
                    else:
                        ac = 0
                                
                quiz_details.append({
                    'quiz_uuid': quiz.uuid,
                    'quiz_name': quiz.title,
                    'quiz_description': quiz.description,
                    'quiz_max_marks': quiz.max_score,
                    'quiz_correct_score': quiz.correct_score,
                    'quiz_wrong_score': quiz.wrong_score,
                    'quiz_date': quiz.scheduled_date,
                    'quiz_duaration': quiz.duration_minutes,
                    'total_questions': quiz.total_questions,
                    'attempt_count': ac
                })
            
            chapter_details.append({
                'chapter_uuid': chapter.uuid,
                'chapter_name': chapter.name,
                'chapter_description': chapter.description,
                'quiz_count': len(quizzes),
                'quizzes': quiz_details
            })
        
        result.append({
            'subject_uuid': subject.uuid,
            'subject_name': subject.name,
            'subject_description': subject.description,
            'chapter_count': len(chapters),
            'chapters': chapter_details
        })   
    return result


def get_ques_for_quiz(quiz_id):
    subject = Question.query.filter_by(quiz_uuid=quiz_id).all()
    return subject

def get_quiz_time(quiz_id):
    time = Quiz.query.with_entities(Quiz.duration_minutes).filter_by(uuid=quiz_id).first()
    return time[0]

def ques_need_to_attempt(quiz_id):
    t_ques = Quiz.query.with_entities(Quiz.total_questions).filter_by(uuid=quiz_id).first()
    return t_ques[0]

def get_ques_and_cor_answ(quiz_id):
    questions = Question.query.filter_by(quiz_uuid=quiz_id).all()
    
    return {q.uuid: q.correct_option for q in questions}

def send_corr(quiz_id):
    corr = Quiz.query.with_entities(Quiz.correct_score).filter_by(uuid=quiz_id).first()
    return corr.correct_score

def send_wrong(quiz_id):
    corr = Quiz.query.with_entities(Quiz.wrong_score).filter_by(uuid=quiz_id).first()
    return corr.wrong_score

def add_score(user_id, quiz_id, score):
    attempt = UserQuizAttempt.query.filter_by(user_uuid=user_id, quiz_uuid=quiz_id).first()
    
    if attempt:
        attempt.score = score
        attempt.attempt_number += 1  
        
        db.session.commit()
        return True
    else:
        new_attempt = UserQuizAttempt(
            user_uuid=user_id, 
            quiz_uuid=quiz_id, 
            score=score, 
            attempt_number=1
        )
        
        db.session.add(new_attempt)
        db.session.commit()
        return True


def add_answer(user_id, quiz_id, a, b,  cor):
    prev_attemp = UserAnswer.query.filter_by(user_uuid=user_id, quiz_uuid=quiz_id, question_uuid=a).first()
    if prev_attemp:
        prev_attemp.attempt_no += 1 
        db.session.commit()
        return True
    else:
        new = UserAnswer(
            user_uuid=user_id, 
            quiz_uuid=quiz_id,
            question_uuid=a,
            selected_option=b,
            is_correct=cor,     
            attempt_no=1
        )
        db.session.add(new)
        db.session.commit()
        return True

def user_ans(user_id, quiz_id):
    user_answers = {}
    answers = UserAnswer.query.filter_by(user_uuid=user_id, quiz_uuid=quiz_id).all()
    for answer in answers:
        user_answers[answer.question_uuid] = answer
    return user_answers

def user_attempt(user_id, quiz_id):
    attempt = UserQuizAttempt.query.filter_by(
        user_uuid=user_id,
        quiz_uuid=quiz_id
    ).first()
    return attempt.score if attempt else None
################################## solution ######################

def get_user_quiz_answers(quiz_id, user_id):
    """Get all answers for a specific quiz attempt by a user."""
    answers = UserAnswer.query.filter_by(
        user_uuid=user_id,
        quiz_uuid=quiz_id
    ).all()
    return {answer.question_uuid: answer for answer in answers}

def get_user_quiz_score(quiz_id, user_id):
    """Get the score for a specific quiz attempt by a user."""
    attempt = UserQuizAttempt.query.filter_by(
        user_uuid=user_id,
        quiz_uuid=quiz_id
    ).first()
    return attempt.score if attempt else None

################################################################
def add_answer(user_id, quiz_id, question_id, selected_option, is_correct):
    """Add or update a user's answer for a question."""
    prev_attempt = UserAnswer.query.filter_by(
        user_uuid=user_id, 
        quiz_uuid=quiz_id, 
        question_uuid=question_id
    ).first()
    if prev_attempt:
        prev_attempt.selected_option = selected_option
        prev_attempt.is_correct = is_correct
        prev_attempt.attempt_no += 1
        prev_attempt.updated_at = datetime.utcnow()
    else:
        new_answer = UserAnswer(
            user_uuid=user_id,
            quiz_uuid=quiz_id,
            question_uuid=question_id,
            selected_option=selected_option,
            is_correct=is_correct,
            attempt_no=1
        )
        db.session.add(new_answer)
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error saving answer: {e}")
        return False

