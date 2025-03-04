from models.model import Quiz, Question, db

def view_inside_chap(chapter_id):
    quiz_details = Quiz.query.filter_by(chapter_uuid=chapter_id).all()   
    for quiz in quiz_details:
        quiz.created_questions_count = Question.query.filter_by(quiz_uuid=quiz.uuid).count()
    return quiz_details

def find_t_questions(quiz_id):
    quiz = Quiz.query.filter_by(uuid=quiz_id).first()
    if not quiz:
        return None
    created_questions = Question.query.filter_by(quiz_uuid=quiz_id).count()
    remaining_questions = quiz.total_questions - created_questions
    return remaining_questions if remaining_questions > 0 else None

def view_inside_quiz(quiz_id):
    ques_details = Question.query.filter_by(quiz_uuid=quiz_id).all()
    return ques_details

def get_title(quiz_id):
    tile = Quiz.query.with_entities(Quiz.title).filter_by(uuid=quiz_id).first()
    b = None
    for i in tile:
        b = i
        return b
    return b

def get_total_cre(quiz_id):
    created_questions = Question.query.filter_by(quiz_uuid=quiz_id).count()
    return created_questions
