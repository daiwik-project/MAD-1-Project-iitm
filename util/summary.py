from models.model import Chapter, Quiz, Subject, UserQuizAttempt, Question, User, db
from datetime import datetime


def get_admin_summary():
    """Get summary of all subjects and their quiz counts"""
    subjects = Subject.query.all()
    summary = {
        "total_subjects": len(subjects),
        "subjects_list": [],
        "quizzes_per_subject": {},
        "quiz_max_attempts":{},
        "subject_wise_quiz_attempts":{},
        "subject_wise_top_score":{},
        "student_highest_attempts": {}
    }
    
    for subject in subjects:
        summary["subjects_list"].append(subject.name)
        
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        
        quiz_count = 0
        
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            quiz_count += len(quizzes)
        
        summary["quizzes_per_subject"][subject.name] = quiz_count


    quizzes = Quiz.query.all() 

    for quiz in quizzes:
        quiz_attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid).all()
        max_attempts = 0
        for attempt in quiz_attempts:
            if attempt.attempt_number > max_attempts:
                max_attempts = attempt.attempt_number
        summary["quiz_max_attempts"][quiz.title] = max_attempts

    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        quiz_attempts = 0
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            for quiz in quizzes:
                attempts = UserQuizAttempt.query.with_entities(UserQuizAttempt.attempt_number).filter_by(quiz_uuid=quiz.uuid).all()
                quiz_attempts += attempts[0][0] if attempts else 0
        summary["subject_wise_quiz_attempts"][subject.name] = quiz_attempts

    for subject in subjects:
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        top_score = 0  
        
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            for quiz in quizzes:
                attempts = UserQuizAttempt.query.with_entities(UserQuizAttempt.score).filter_by(quiz_uuid=quiz.uuid).all()
                
                if attempts:  
                    for attempt in attempts:
                        score = attempt[0]
                        if score > top_score:  
                            top_score = score
                        else:
                            top_score = 0  
        summary["subject_wise_top_score"][subject.name] = top_score
    
    attempt_counts = {}  
    
    user_quiz_attempts = UserQuizAttempt.query.all()
    for attempt in user_quiz_attempts:
        if attempt.user_uuid in attempt_counts:
            attempt_counts[attempt.user_uuid] += 1
        else:
            attempt_counts[attempt.user_uuid] = 1
    student_des = list(attempt_counts.items())
    for al in range(len(student_des)):
        for bl in range(al + 1, len(student_des)):
            if student_des[al][1] < student_des[bl][1]:
                student_des[al], student_des[bl] = student_des[bl], student_des[al]
    
    sorted_dict = dict(student_des)
    final_dict = {}
    for key, value in sorted_dict.items():
        User_data = User.query.filter_by(uuid=key).first()
        final_dict[User_data.username] = value
    summary["student_highest_attempts"] = final_dict
    return summary



def get_user_summary(user_uuid):
    """Retrieves summary data for a specific user."""

    user = User.query.filter_by(uuid=user_uuid).first()
    if not user:
        return None

    summary = {
        "total_quiz_attempts": 0,
        "subject_wise_quiz_attempts": {},
        "highest_score_quiz_wise": {},
        "month_wise_quiz_attempts": {},
        "average_score_per_subject": {},
        "quizzes_attempted_per_chapter": {},
        "best_score_in_each_subject": {},
        "number_of_attempts_per_quiz": {},
    }

    
    summary["total_quiz_attempts"] = UserQuizAttempt.query.filter_by(user_uuid=user_uuid).count()

    subjects = Subject.query.all()
    for subject in subjects:
        attempt_count = 0
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            for quiz in quizzes:
                attempts = UserQuizAttempt.query.filter_by(user_uuid=user_uuid, quiz_uuid=quiz.uuid).count()
                attempt_count += attempts  # Add the count directly
        summary["subject_wise_quiz_attempts"][subject.name] = attempt_count

    quizzes = Quiz.query.all()
    for quiz in quizzes:
        user_score = (UserQuizAttempt.query
                    .with_entities(UserQuizAttempt.score)
                    .filter_by(user_uuid=user_uuid, quiz_uuid=quiz.uuid)  # Corrected line
                    .all())
        if user_score:
            max_poss_score = quiz.max_score
            percentage = (user_score[0][0] *100) / max_poss_score
            summary["highest_score_quiz_wise"][quiz.title] = percentage

    all_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_uuid).all()
    month_counts = {}
    for attempt in all_attempts:
        if attempt.timestamp: 
           month_str = attempt.timestamp.strftime("%Y-%m")  
           if month_str in month_counts:
               month_counts[month_str] += 1
           else:
               month_counts[month_str] = 1
    summary["month_wise_quiz_attempts"] = month_counts


    subjects = Subject.query.all()
    for subject in subjects:
        total_possible_score = 0
        total_achieved_score = 0
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            for quiz in quizzes:
                attempts = UserQuizAttempt.query.filter_by(user_uuid=user_uuid, quiz_uuid=quiz.uuid).all()
                if attempts:
                    total_possible_score += quiz.max_score  
                    for attempt in attempts:
                        if attempt.score is not None:
                            total_achieved_score += attempt.score
        if (total_possible_score> 0):
            avg_score_percentage = (total_achieved_score / total_possible_score) * 100
            summary["average_score_per_subject"][subject.name] = avg_score_percentage


    subjects = Subject.query.all()
    for subject in subjects:
        best_score_subject = 0  
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        for chapter in chapters:
            quizzes_attempted_count = 0
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            for quiz in quizzes:
                user_attempts_quiz = UserQuizAttempt.query.filter_by(user_uuid=user_uuid, quiz_uuid=quiz.uuid).all()
                if user_attempts_quiz:
                    quizzes_attempted_count += 1  
                    for attempt in user_attempts_quiz:
                        if attempt.score is not None: 
                           score_percentage = (attempt.score * 100) / quiz.max_score
                           best_score_subject = max(best_score_subject, score_percentage)  

            summary["quizzes_attempted_per_chapter"][chapter.name] = quizzes_attempted_count  

        summary["best_score_in_each_subject"][subject.name] = best_score_subject  

    user_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_uuid).all()
    attempts_per_quiz = {}
    for attempt in user_attempts:
        quiz = Quiz.query.get(attempt.quiz_uuid)  
        if quiz:
            attempts_per_quiz[quiz.title] = attempt.attempt_number 

    summary["number_of_attempts_per_quiz"] = attempts_per_quiz

    return summary
