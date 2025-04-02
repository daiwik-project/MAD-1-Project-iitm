from controllers.Auth.user import block_User, block_checker, create_user, find_user_id, get_user_info, previous_email, previous_username, unblock_User, verify_user
from controllers.Quiz.creator import cre_ques, cre_quiz, verify_prev_quiz
from controllers.Quiz.read import find_t_questions, get_title, get_total_cre, view_inside_chap, view_inside_quiz
from controllers.Quiz.update import update_ques, update_quiz_info
from controllers.admin.read import admin_dashboard_view, get_chap, get_subj_des
from controllers.admin.update import update_chap_info, update_sub_info
from controllers.delete.delete import del_chapter, del_ques, del_quiz, del_sub
from controllers.user.user_crud import add_answer, add_score, get_ques_and_cor_answ, get_ques_for_quiz, get_quiz_time, get_sub, get_subject_chapter_course_details, get_user_quiz_answers, get_user_quiz_score, ques_need_to_attempt, send_corr, send_wrong, user_ans, user_attempt
from flask import Flask, render_template, request, redirect, url_for, flash  # type: ignore
from database import db
from util.profile import update_user_profile_info, user_info
from util.quiz import verify_chapter, verify_subject
from util.search import admin_search_result, user_search_result
from util.summary import get_admin_summary, get_user_summary
from util.util import update_user_quiz_info
from util.uuid import generate_uuid
from controllers.admin.create import cre_chapter, cre_subject

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Influencersync'

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')



# Admin Routes
@app.route('/admin_dashboard')
def admin_dashboard():
    info = admin_dashboard_view()
    return render_template('admin_dashboard.html', subjects_info=info )

@app.route('/admin_dashboard/user_control', methods=['GET', 'POST'])
def user_control():
    if request.method == 'POST':
        a_query = request.form['query']
        user_info = get_user_info(a_query)
        if user_info:
            return render_template('admin_user_ctrl.html', user_info=user_info)
    return render_template('admin_user_ctrl.html')

@app.route('/admin_dashboard/user_control/block/<username>', methods=['GET'])
def block_user(username):
    block_User(username)
    return redirect(url_for('user_control'))

@app.route('/admin_dashboard/user_control/unblock/<username>', methods=['GET'])
def unblock_user(username):
    unblock_User(username)
    return redirect(url_for('user_control'))

############################# View Routes ################################
# View Subject
@app.route('/admin_dashboard/view/<subject_id>/<subject_name>')
def view_subject(subject_id, subject_name):
    des = get_subj_des(subject_id) 
    chap = get_chap(subject_id)
    return render_template('view_subject.html', subject_id=subject_id, subject_name=subject_name, subject_description=des, chapter=chap)

@app.route('/admin_dashboard/view/<subject_id>/<subject_name>/<chapter_id>/<chapter_name>')
def view_chapter(subject_id, subject_name, chapter_id, chapter_name):
    quiz_info = view_inside_chap(chapter_id)
    return render_template('view_chapter.html', 
                           subject_id=subject_id, 
                           subject_name=subject_name, 
                           chapter_id=chapter_id, 
                           chapter_name=chapter_name, 
                           quizzes=quiz_info)

@app.route('/admin_dashboard/view/<quiz_id>')
def view_question(quiz_id):
    ques_info = view_inside_quiz(quiz_id)
    quiz_title = get_title(quiz_id)
    t_ques = get_total_cre(quiz_id)
    return render_template('vie_question.html',
                         ques=ques_info,
                         quiz_id=quiz_id,
                         total_questions=t_ques)



########################## Create Routes #####################################
# Create Subject
@app.route('/admin_dashboard/create/subject', methods=['GET', 'POST'])
def create_subject():
    if request.method == 'POST':
        name = request.form['subject_name']
        description = request.form['subject_description']
        if name and description:
            verify_subject(name)
            if verify_subject(name)==None:
                id = generate_uuid()
                cre_subject(id, name, description)
                flash('Subject created successfully', category='success')
                return redirect(url_for('create_chapter', subject_name=name, subject_id=id ))
            else:
                flash('Subject already exists', category='danger')
        else:
            flash('Please provide subject name and description', category='warning')
    return render_template('create_subject.html')

# Create Chapter
@app.route('/admin_dashboard/<subject_id>/<subject_name>/create/chapter', methods=['GET', 'POST'])
def create_chapter(subject_name, subject_id):
    if request.method == 'POST':
        name = request.form['chapter_name']
        description = request.form['chapter_description']
        if name and description:
            verify_chapter(name)
            if verify_chapter(name)==None:
                uuid = generate_uuid()
                cre_chapter(uuid, name, description, subject_id)
                flash('Chapter created successfully', category='success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Chapter created successfully', category='Danger')
        else:
            flash('Please provide chapter name and description', category='warning')
    return render_template('create_chapter.html',  subject_name=subject_name, subject_id=subject_id)

# Create Quiz
@app.route('/admin_dashboard/<subject_id>/<subject_name>/<chapter_id>/<chapter_name>/create/quiz', methods=['GET', 'POST'])
def create_quiz(subject_id, subject_name, chapter_id, chapter_name):
    if request.method == 'POST':
        try:
            title = request.form['quizTitle']
            description = request.form['quizDescription']
            max_marks = request.form['quizMaxMarks']
            correct_marks = request.form['quizcorrectscore']
            negative_marks = request.form['quizwrongscore']
            scheduled_date = request.form['quizScheduledDate']
            max_time = request.form['quizMaxTime']
            total_questions = request.form['quiztotalquestion']
            if title and description:
                if verify_prev_quiz(title, chapter_id) is None:
                    uuid = generate_uuid()
                    cre_quiz(
                        uuid, title, description, max_marks, 
                        correct_marks, negative_marks, chapter_id,
                        scheduled_date, max_time, total_questions
                    )
                    flash('Quiz created successfully!', 'success')
                    return redirect(url_for('view_chapter', 
                                          subject_id=subject_id,
                                          subject_name=subject_name,
                                          chapter_id=chapter_id,
                                          chapter_name=chapter_name))
                else:
                    flash('Quiz with this title already exists', 'danger')
            else:
                flash('Please provide quiz title and description', 'warning')
        except:
            print("problem here")
    return render_template('view_chapter.html',
                         subject_id=subject_id,
                         subject_name=subject_name,
                         chapter_id=chapter_id,
                         chapter_name=chapter_name)

@app.route('/admin_dashboard/<subject_id>/<subject_name>/<chapter_id>/<chapter_name>/<quiz_id>/<quiz_title>/create/questions', methods=['GET', 'POST'])
def create_question(subject_id, subject_name, chapter_id, chapter_name, quiz_id, quiz_title):
    t_questions = find_t_questions(quiz_id)
    if request.method == 'POST':
        data = request.form.to_dict()
        for i in range(1, t_questions+1):
            question = request.form[f'question_{i}']
            option1 = request.form[f'q{i}_option1']
            option2 = request.form[f'q{i}_option2']
            option3 = request.form[f'q{i}_option3']
            option4 = request.form[f'q{i}_option4']
            correct_option = request.form[f'q{i}_correct']
            uuid = generate_uuid()
            cre_ques(uuid, quiz_id, question, option1, option2, option3, option4, correct_option,)
        flash('Question created successfully', 'success')
        return redirect(url_for('view_chapter', 
                                subject_id=subject_id, 
                                subject_name=subject_name, 
                                chapter_id=chapter_id, 
                                chapter_name=chapter_name))
    return render_template('create_question.html', subject_id=subject_id, 
                           subject_name=subject_name, 
                           chapter_id=chapter_id, 
                           chapter_name=chapter_name, 
                           quiz_id=quiz_id, 
                           quiz_title=quiz_title, 
                           total_questions=t_questions)

##################################### EDIT ROUTES ################################
@app.route('/admin_dashboard/<quiz_id>/edit/<ques_id>', methods=['POST'])
def update_question(ques_id, quiz_id):
    up_ques = request.form['question']
    option_1 = request.form['option1']
    option_2 = request.form['option2']
    option_3 = request.form['option3']
    option_4 = request.form['option4']
    is_correct = request.form['is_correct']
    update_ques(ques_id, up_ques, option_1, option_2, option_3, option_4, is_correct)
    return redirect(url_for('view_question', quiz_id=quiz_id))

@app.route('/admin_dashboard/<subject_id>/<subject_name>/<chapter_id>/<chapter_name>/edit/<quiz_id>', methods=['POST'])
def update_quiz_det(subject_id, subject_name, chapter_id,chapter_name, quiz_id):
    title = request.form['quizTitle']
    description = request.form['quizDescription']
    max_marks = int(request.form['quizsMaxMarks'])
    correct_marks = float(request.form['quizcorrectscore'])
    negative_marks = float(request.form['quizwrongscore'])
    scheduled_date = request.form['quizScheduledDate']
    max_time = int(request.form['quizMaxTime'])
    total_questions = int(request.form['quiztotalquestion'])
    update_quiz_info(quiz_id, title, description, max_marks, correct_marks, negative_marks, scheduled_date, max_time, total_questions)
    return redirect(url_for('view_chapter', subject_id=subject_id, subject_name=subject_name, chapter_id=chapter_id,chapter_name=chapter_name))

@app.route('/admin_dashboard/<subject_id>/<subject_name>/edit/<chapter_id>', methods=['POST'])
def update_chap_det(subject_id, subject_name,  chapter_id):
    title = request.form['chapter_name']
    description = request.form['chapter_des']
    update_chap_info(chapter_id, title, description)
    return redirect(url_for('view_subject', subject_id=subject_id, subject_name=subject_name))

@app.route('/admin_dashboard/<subject_id>/edit', methods=['POST'])
def update_subject_det(subject_id):
    title = request.form['sub_name']
    description = request.form['sub_des']
    update_sub_info(subject_id, title, description)
    return redirect(url_for('admin_dashboard'))

############################# DELETE ROUTES ###################################
@app.route('/admin_dashboard/<quiz_id>/edit/<ques_id>', methods=['GET'])
def delete_question(ques_id, quiz_id):
    del_ques(ques_id)
    return redirect(url_for('view_question', quiz_id=quiz_id))


@app.route('/admin_dashboard/<subject_id>/<subject_name>/<chapter_id>/<chapter_name>/del/<quiz_id>', methods=['GET'])
def delete_quiz(subject_id, subject_name, chapter_id,chapter_name, quiz_id):
    del_quiz(quiz_id)
    return redirect(url_for('view_chapter', subject_id=subject_id, subject_name=subject_name, chapter_id=chapter_id,chapter_name=chapter_name))


@app.route('/admin_dashboard/<subject_id>/<subject_name>/del/<chapter_id>', methods=['GET'])
def delete_chap(subject_id, subject_name,  chapter_id):
    del_chapter(chapter_id)
    return redirect(url_for('view_subject', subject_id=subject_id, subject_name=subject_name))

@app.route('/admin_dashboard/<subject_id>/del', methods=['GET'])
def del_subject(subject_id):
    del_sub(subject_id)
    return redirect(url_for('admin_dashboard'))



##################################### User Routes ################################
# User Auth Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match', category='warning')
        elif previous_username(username) is not None or previous_email(email) is not None:
            flash('Username already exists', category='danger')
        else:
            uuid = generate_uuid()
            create_user(uuid, username, email, password)
            flash('Registration successful', category='success')
            return redirect(url_for('login'))
    return render_template('user_register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if (username and password):
            verify_status = verify_user(username, password)
            active_status = block_checker(username)
            if verify_status and active_status:
                id = find_user_id(username)
                flash('Login successful', category='success')
                return redirect(url_for('user_dashboard',id=id))
            else:
                flash('Invalid credentials or blocked by admin', category='danger')
                return redirect(url_for('login'))
        return "You have not typed correct user id and passwordor or you are not present in our database"
    return render_template('user_login.html')

# User Dashboard
@app.route('/user_dashboard/<id>')
def user_dashboard(id):
    subject_data = get_subject_chapter_course_details(id)
    return render_template('user_dashboard.html', subjects=subject_data, user_id=id)

#user Profile Page 
@app.route('/user_dashboard/profile/<id>', methods=['GET', 'POST'])
def user_profile(id):
    user_prof = user_info(id)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        update_user_profile_info(email, password, id)
        return redirect(url_for('user_profile', id=id))

    return render_template('user_profile.html', 
                           user=user_prof,
                           user_id=id)

################################## Attempt Quiz ########################################
@app.route('/user_dashboard/<user_id>/<subject_id>/<subject_name>/<chapter_id>/<chapter_name>/<quiz_id>/attempt/<attempt>/<attempt_no>', methods=['GET', 'POST'])
def attempt_quiz(user_id, subject_id, subject_name, chapter_id, chapter_name, quiz_id, attempt, attempt_no):
    corr = send_corr(quiz_id)
    wrong = send_wrong(quiz_id)
    score = 0.0
    ques = get_ques_for_quiz(quiz_id)  
    time = get_quiz_time(quiz_id)
    Ques = get_ques_and_cor_answ(quiz_id) 
    total_ques = ques_need_to_attempt(quiz_id)  

    if request.method == 'POST':
        data = request.form.to_dict()  
        attempted_scores = []

        for a, b in data.items():
            for c, d in Ques.items():
                if a == c: 
                    if b == d: 
                        attempted_scores.append(corr)
                    elif b!=d: 
                        attempted_scores.append(-wrong)  
                    else:
                        continue
                else:
                    continue

        attempted_scores.sort(reverse=True)
        best_scores = attempted_scores[:total_ques]  
        score = sum(best_scores)
        add_score(user_id, quiz_id, score)

        for question_id, selected_option in data.items():
            correct_answer = Ques.get(question_id)
            if correct_answer:
                is_correct = 1 if selected_option == correct_answer else 0
                add_answer(user_id, quiz_id, question_id, selected_option, is_correct)

        max_score = total_ques * corr
        return redirect(url_for('solution', user_id=user_id, 
                                subject_id=subject_id, 
                                subject_name=subject_name,
                                chapter_id=chapter_id, 
                                chapter_name=chapter_name, 
                                quiz_id=quiz_id,
                                attempt=attempt, 
                                attempt_no=attempt_no,
                                max_score=max_score,))

    return render_template('attempt_quiz.html', user_id=user_id, 
                           subject_id=subject_id, 
                           subject_name=subject_name, 
                           chapter_id=chapter_id, 
                           chapter_name=chapter_name, 
                           quiz_id=quiz_id, 
                           attempt_no=attempt_no, 
                           ques=ques,
                           time=time,
                           total_ques=total_ques)


################################## SOLUTION PAGE ##################################################
@app.route('/user_dashboard/<user_id>/<subject_id>/<subject_name>/<chapter_id>/<chapter_name>/<quiz_id>/attempt/<attempt>/<attempt_no>/<max_score>/solution', methods=['GET', 'POST'])
def solution(user_id, subject_id, subject_name, chapter_id, chapter_name, quiz_id, attempt, attempt_no, max_score):
    if attempt:
        questions = get_ques_for_quiz(quiz_id)
        user_answers = get_user_quiz_answers(quiz_id, user_id)
        user_score = get_user_quiz_score(quiz_id, user_id)
        max_scores = float(max_score)
        maxi_score = int(max_scores)
        return render_template('solution.html', 
                            user_id=user_id, 
                            subject_id=subject_id, 
                            subject_name=subject_name, 
                            chapter_id=chapter_id, 
                            chapter_name=chapter_name, 
                            quiz_id=quiz_id, 
                            attempt_no=attempt_no, 
                            questions=questions,
                            user_answers=user_answers,
                            user_score=user_score,
                            max_scores=maxi_score)
    return "YOU HAVE NOT APPTEMPTED THE QUIZ"


@app.route('/user_dashboard/<user_id>/<subject_id>/<subject_name>/<chapter_id>/<chapter_name>/<quiz_id>/attempt/<attempt>/<attempt_no>/solution', methods=['GET', 'POST'])
def quiz_solution(user_id, subject_id, subject_name, chapter_id, chapter_name, quiz_id, attempt, attempt_no):
    questions = get_ques_for_quiz(quiz_id)
    user_answers = user_ans(user_id, quiz_id)  
    user_score = user_attempt(user_id, quiz_id)
    return render_template('solution.html',
                         user_id=user_id,
                         questions=questions,
                         user_answers=user_answers, 
                         user_score=user_score)


########################## Summary Page ##################################
# Admin Summary Page
@app.route('/admin_dashboard/summary')
def admin_summary():
    subject_summary = get_admin_summary()

    quizzes_per_subject = subject_summary['quizzes_per_subject']
    top_trending_quizzes = subject_summary['quiz_max_attempts']
    subject_wise_quiz_attempts = subject_summary['subject_wise_quiz_attempts']
    subject_wise_top_score= subject_summary['subject_wise_top_score']
    student_data = subject_summary["student_highest_attempts"] 
    return render_template('admin_summary.html', 
                           quizzes_per_subject=quizzes_per_subject, 
                           top_trending_quizzes=top_trending_quizzes,
                           subject_wise_quiz_attempts=subject_wise_quiz_attempts,
                           subject_wise_top_score=subject_wise_top_score,
                           student_data=student_data)

#user Summary
@app.route('/user_dashboard/<user_id>/summary')
def user_summary(user_id):
    update_user_quiz_info(user_id)
    a = get_user_summary(user_id)
    average_score_per_subject = a['average_score_per_subject']
    best_score_in_each_subject = a['best_score_in_each_subject']
    highest_score_quiz_wise = a['highest_score_quiz_wise']
    month_wise_quiz_attempts = a['month_wise_quiz_attempts']
    number_of_attempts_per_quiz = a['number_of_attempts_per_quiz']
    quizzes_attempted_per_chapter = a['quizzes_attempted_per_chapter']
    subject_wise_quiz_attempts = a['subject_wise_quiz_attempts']
    total_quiz_attempts = a['total_quiz_attempts']
    return render_template('user_summary.html',
                           average_score_per_subject=average_score_per_subject,
                           best_score_in_each_subject=best_score_in_each_subject,
                           highest_score_quiz_wise=highest_score_quiz_wise,
                           month_wise_quiz_attempts=month_wise_quiz_attempts,
                           number_of_attempts_per_quiz=number_of_attempts_per_quiz,
                           quizzes_attempted_per_chapter=quizzes_attempted_per_chapter,
                           subject_wise_quiz_attempts=subject_wise_quiz_attempts,
                           total_quiz_attempts=total_quiz_attempts,
                           user_id = user_id)


############################### SEARCH PAGE ##########################
# User Search
@app.route('/user_dashboard/<user_id>/search', methods=['GET', 'POST'])
def user_search(user_id):
    placeholder = "Enter your query..."  
    
    if request.method == 'POST':
        selected_parameter = request.form.get('parameter')
        u_query = request.form['query'].lower()

        if selected_parameter == "date":
            placeholder = "Date can only be in any of these formats: dd/mm/yyyy or dd-mm-yyyy"
        elif selected_parameter == "quiz_title":
            placeholder = "Enter the quiz title"
        elif selected_parameter == "chapter_name":
            placeholder = "Enter the chapter name"
        elif selected_parameter == "subject_name":
            placeholder = "Enter the subject name"
        elif selected_parameter == "score":
            placeholder = "Enter the score"
        
        
        if selected_parameter and u_query:
            search_dict = user_search_result(selected_parameter, u_query, user_id)
            return render_template('user_search.html', user_id=user_id,
                                   placeholder=placeholder,
                                   selected_parameter=selected_parameter,
                                   search_dict=search_dict)
        
        return render_template('user_search.html', user_id=user_id, 
                               placeholder=placeholder, 
                               selected_parameter=selected_parameter,)

    return render_template('user_search.html', user_id=user_id, placeholder=placeholder, selected_parameter=None)


# admin Search
@app.route('/admin_dashboard/search', methods=['GET', 'POST'])
def admin_search():
    placeholder = "Enter your query..." 
    
    if request.method == 'POST':
        selected_parameter = request.form.get('parameter')
        a_query = request.form['query'].lower()

        if selected_parameter == "date":
            placeholder = "Date can only be in any of these formats: dd/mm/yyyy or dd-mm-yyyy"
        elif selected_parameter == "quiz_title":
            placeholder = "Enter the quiz title"
        elif selected_parameter == "chapter_name":
            placeholder = "Enter the chapter name"
        elif selected_parameter == "subject_name":
            placeholder = "Enter the subject name"
        elif selected_parameter == "user_id":
            placeholder = "Enter the User ID"
        
        
        if selected_parameter and a_query:
            search_dict = admin_search_result(selected_parameter, a_query)
            iter_len = len(search_dict['Quiz Title'])
            return render_template('admin_search.html', 
                                   placeholder=placeholder,
                                   selected_parameter=selected_parameter,
                                   search_dict=search_dict,
                                   iter_len=iter_len)
        
        return render_template('admin_search.html', 
                               placeholder=placeholder, 
                               selected_parameter=selected_parameter,)

    return render_template('admin_search.html', placeholder=placeholder, selected_parameter=None)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)




