from models.model import  UserQuizAttempt, Quiz, db

def update_user_quiz_info(user_id):
    quiz = []
    quiz_id = Quiz.query.with_entities(Quiz.uuid).all()
    for i in quiz_id:
        quiz.append(i[0])
    
    user_quiz_ids = []
    user_quiz = UserQuizAttempt.query.with_entities(UserQuizAttempt.quiz_uuid).all()
    for i in user_quiz:
        user_quiz_ids.append(i[0])

    for user_quiz_id in user_quiz_ids:
        if user_quiz_id not in quiz:
            user_attempt = UserQuizAttempt.query.filter_by(quiz_uuid=user_quiz_id).first()
            if user_attempt:
                db.session.delete(user_attempt)
    
    db.session.commit()
    return 0
