from models.model import Chapter, User, Quiz, Subject, UserQuizAttempt, db
from datetime import datetime


def user_search_result(param, query, user_id):
    result = {}

    if param == "date":
        try:
            date_obj = datetime.strptime(query, '%d/%m/%Y')
        except ValueError:
            try:
                date_obj = datetime.strptime(query, '%d-%m-%Y')
            except ValueError:
                return {}  

        search_date = date_obj.date()
        quizzes = Quiz.query.filter(db.func.date(Quiz.scheduled_date) == search_date).all()

        if quizzes:
            quiz_titles = []
            chapter_names = []
            subject_names = []
            dates = []
            user_scores = []

            for quiz in quizzes:
                quiz_titles.append(quiz.title)

                chapter = Chapter.query.get(quiz.chapter_uuid)
                if chapter:
                    chapter_names.append(chapter.name)
                    subject = Subject.query.get(chapter.subject_uuid)
                    if subject:
                        subject_names.append(subject.name)
                    else:
                        subject_names.append(None)
                else:
                    chapter_names.append(None)
                    subject_names.append(None)

                dates.append(quiz.scheduled_date.strftime('%d/%m/%Y'))

                attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid, user_uuid=user_id).all()
                scores_for_quiz = []
                for attempt in attempts:
                    scores_for_quiz.append(attempt.score)

                user_scores.append(scores_for_quiz if scores_for_quiz else [])

            result["Date"] = dates
            result["Quiz title"] = quiz_titles
            result["Chapter name"] = chapter_names
            result["Subject name"] = subject_names
            result["Your score"] = user_scores

    elif param == "quiz_title":
        quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{query}%")).all()

        if quizzes:
            quiz_titles = []
            chapter_names = []
            subject_names = []
            dates = []
            user_scores = []

            for quiz in quizzes:
                quiz_titles.append(quiz.title)

                chapter = Chapter.query.get(quiz.chapter_uuid)
                if chapter:
                    chapter_names.append(chapter.name)
                    subject = Subject.query.get(chapter.subject_uuid)
                    if subject:
                        subject_names.append(subject.name)
                    else:
                        subject_names.append(None)
                else:
                    chapter_names.append(None)
                    subject_names.append(None)

                dates.append(quiz.scheduled_date.strftime('%d/%m/%Y'))

                attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid, user_uuid=user_id).all()
                scores_for_quiz = []
                for attempt in attempts:
                    scores_for_quiz.append(attempt.score)

                user_scores.append(scores_for_quiz if scores_for_quiz else [])

            result["Quiz title"] = quiz_titles
            result["Chapter name"] = chapter_names
            result["Subject name"] = subject_names
            result["Date"] = dates
            result["Your score"] = user_scores

    elif param == "chapter_name":
        chapters = Chapter.query.filter(Chapter.name.ilike(f"%{query}%")).all()

        if chapters:
            chapter_names = []
            subject_names = []
            quiz_titles = []
            dates = []
            user_scores = []

            for chapter in chapters:
                chapter_names.append(chapter.name)

                subject = Subject.query.get(chapter.subject_uuid)
                if subject:
                    subject_names.append(subject.name)
                else:
                    subject_names.append(None)

                quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
                for quiz in quizzes:
                    quiz_titles.append(quiz.title)
                    dates.append(quiz.scheduled_date.strftime('%d/%m/%Y'))

                    attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid, user_uuid=user_id).all()
                    scores_for_quiz = []
                    for attempt in attempts:
                        scores_for_quiz.append(attempt.score)

                    user_scores.append(scores_for_quiz if scores_for_quiz else [])

            result["Chapter name"] = chapter_names
            result["Subject name"] = subject_names
            result["Quiz title"] = quiz_titles
            result["Date"] = dates
            result["Your score"] = user_scores

    elif param == "subject_name":
        subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()

        if subjects:
            subject_names = []
            chapter_names = []
            quiz_titles = []
            dates = []
            user_scores = []

            for subject in subjects:
                subject_names.append(subject.name)

                chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
                for chapter in chapters:
                    chapter_names.append(chapter.name)

                    quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
                    for quiz in quizzes:
                        quiz_titles.append(quiz.title)
                        dates.append(quiz.scheduled_date.strftime('%d/%m/%Y'))

                        attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid, user_uuid=user_id).all()
                        scores_for_quiz = []
                        for attempt in attempts:
                            scores_for_quiz.append(attempt.score)

                        user_scores.append(scores_for_quiz if scores_for_quiz else [])

            result["Subject name"] = subject_names
            result["Chapter name"] = chapter_names
            result["Quiz title"] = quiz_titles
            result["Date"] = dates
            result["Your score"] = user_scores

    elif param == "score":
        try:
            score = query 
        except ValueError:
            return {}

        attempts = UserQuizAttempt.query.filter_by(score=score, user_uuid=user_id).all()

        if attempts:
            user_scores = []
            quiz_titles = []
            subject_names = []
            chapter_names = []
            dates = []

            for attempt in attempts:
                user_scores.append(attempt.score)

                quiz = Quiz.query.get(attempt.quiz_uuid)
                if quiz:
                    quiz_titles.append(quiz.title)
                    dates.append(quiz.scheduled_date.strftime('%d/%m/%Y'))

                    chapter = Chapter.query.get(quiz.chapter_uuid)
                    if chapter:
                        chapter_names.append(chapter.name)

                        subject = Subject.query.get(chapter.subject_uuid)
                        if subject:
                            subject_names.append(subject.name)
                        else:
                            subject_names.append(None)
                    else:
                        chapter_names.append(None)
                        subject_names.append(None)

            result["Your score"] = user_scores
            result["Quiz title"] = quiz_titles
            result["Subject name"] = subject_names
            result["Chapter name"] = chapter_names
            result["Date"] = dates

    return result




def admin_search_result(param, query):
    result = {}

    if param == "date":
        try:
            date_obj = datetime.strptime(query, '%d/%m/%Y')
        except ValueError:
            try:
                date_obj = datetime.strptime(query, '%d-%m-%Y')
            except ValueError:
                return {}  

        search_date = date_obj.date()
        quizzes = Quiz.query.filter(db.func.date(Quiz.scheduled_date) == search_date).all()

        if quizzes:
            quiz_titles = [quiz.title for quiz in quizzes]
            chapter_names = []
            subject_names = []
            dates = [quiz.scheduled_date.strftime('%d/%m/%Y') for quiz in quizzes]
            user_counts = []

            for quiz in quizzes:
                chapter = Chapter.query.get(quiz.chapter_uuid)
                chapter_names.append(chapter.name if chapter else None)
                subject = Subject.query.get(chapter.subject_uuid) if chapter else None
                subject_names.append(subject.name if subject else None)

                attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid).all()
                user_ids = set()  
                for attempt in attempts:
                    user_ids.add(attempt.user_uuid)
                user_counts.append(len(user_ids))

            result["Date"] = dates
            result["Quiz Title"] = quiz_titles
            result["Chapter name"] = chapter_names
            result["Subject name"] = subject_names
            result["Users Attempted"] = user_counts  


    
    elif param == "quiz_title":
        quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{query}%")).all()

        if quizzes:
            quiz_titles = [quiz.title for quiz in quizzes]
            chapter_names = []
            subject_names = []
            dates = [quiz.scheduled_date.strftime('%d/%m/%Y') for quiz in quizzes]
            user_counts = []

            for quiz in quizzes:
                chapter = Chapter.query.get(quiz.chapter_uuid)
                chapter_names.append(chapter.name if chapter else None)
                subject = Subject.query.get(chapter.subject_uuid) if chapter else None
                subject_names.append(subject.name if subject else None)

                attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid).all()
                user_ids = set()
                for attempt in attempts:
                    user_ids.add(attempt.user_uuid)
                user_counts.append(len(user_ids))

            result["Quiz Title"] = quiz_titles
            result["Chapter name"] = chapter_names
            result["Subject name"] = subject_names
            result["Date"] = dates
            result["Users Attempted"] = user_counts

    
    elif param == "chapter_name":
        chapters = Chapter.query.filter(Chapter.name.ilike(f"%{query}%")).all()

        if chapters:
            chapter_names = [chapter.name for chapter in chapters]
            subject_names = []
            quiz_titles = []
            dates = []
            user_counts = []

            for chapter in chapters:
                subject = Subject.query.get(chapter.subject_uuid)
                subject_names.append(subject.name if subject else None)

                quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
                for quiz in quizzes:
                    quiz_titles.append(quiz.title)
                    dates.append(quiz.scheduled_date.strftime('%d/%m/%Y'))

                    attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid).all()
                    user_ids = set()
                    for attempt in attempts:
                        user_ids.add(attempt.user_uuid)
                    user_counts.append(len(user_ids))

            result["Chapter name"] = chapter_names
            result["Subject name"] = subject_names
            result["Quiz Title"] = quiz_titles
            result["Date"] = dates
            result["Users Attempted"] = user_counts

    
    elif param == "subject_name":
        subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()

        if subjects:
            subject_names = [subject.name for subject in subjects]
            chapter_names = []
            quiz_titles = []
            dates = []
            user_counts = []

            for subject in subjects:
                chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
                for chapter in chapters:
                    chapter_names.append(chapter.name)
                    quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
                    for quiz in quizzes:
                        quiz_titles.append(quiz.title)
                        dates.append(quiz.scheduled_date.strftime('%d/%m/%Y'))

                        attempts = UserQuizAttempt.query.filter_by(quiz_uuid=quiz.uuid).all()
                        user_ids = set()
                        for attempt in attempts:
                            user_ids.add(attempt.user_uuid)
                        user_counts.append(len(user_ids))

            result["Subject name"] = subject_names
            result["Chapter name"] = chapter_names
            result["Quiz Title"] = quiz_titles
            result["Date"] = dates
            result["Users Attempted"] = user_counts

    
    elif param == "user_id":
        user = User.query.filter(User.uuid.ilike(f"%{query}%")).first()  
        if user:
            attempts = UserQuizAttempt.query.filter_by(user_uuid=user.uuid).all()
            if attempts:
                user_ids = [user.uuid]  
                usernames = [user.username]
                quiz_titles = []
                scores = []
                dates = []

                for attempt in attempts:
                    quiz = Quiz.query.get(attempt.quiz_uuid)
                    if quiz:
                        quiz_titles.append(quiz.title)
                        scores.append(attempt.score)
                        dates.append(quiz.scheduled_date.strftime('%d/%m/%Y') if quiz.scheduled_date else "N/A")


                result["User ID"] = user_ids
                result["Username"] = usernames
                result["Quiz Title"] = quiz_titles
                result["Date"] = dates
                result["Score"] = scores
    print(result)
    return result
