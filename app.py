from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from database import load_courses_from_db, add_rating_to_db, remove_rating_from_db, load_carousel_courses_from_db, load_best_courses_from_db, load_explore_courses_from_db, load_compulsory_courses_from_db, load_favorite_courses_from_db, add_interests_to_db, add_login_to_db, check_credentials, update_interests, add_views_to_db, put_rating_to_db, add_test_to_db, get_test_from_db, load_best_courses_with_favorite_from_db
from flask import request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)


filters = {
    'Degree': ['Bachelor', 'Master', 'Pre-master'],
    'Block': [1, 2, 3, 4]
}

@app.route("/")
def landing():
    return render_template('welcome.html')

app.secret_key = 'session_key'

@app.route("/inlogpage", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_number = request.form['student_number']
        password = request.form['password']

        if check_credentials(student_number, password):
            session['student_number'] = student_number
            session['password'] = password
            return render_template('state_interests.html')
        else:
            return render_template('inlogpage.html')
    return render_template('inlogpage.html')

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        student_number = request.form['student_number']
        password = request.form['password']
        level = request.form['level']
        education = request.form['education']
          
        add_login_to_db(student_number, password, level, education)
        
        return redirect('/inlogpage')
        
    return render_template('signin.html')

@app.route("/state_interests.html")
def state_interests():
    return render_template('state_interests.html')

@app.route("/state_interests/stated.html", methods=['POST'])
def stated_interests():
    data = request.form
    student_number = session.get('student_number')  
    password = session.get('password') 

    if student_number and password:
        update_interests(student_number, password, data)

    previous_page = request.referrer
    return redirect(f'/home/{student_number}')

@app.route("/test", methods=['GET', 'POST'])
def test():
    favorite_value = get_test_from_db()
    data = request.form

    if request.method == 'POST' and 'favorite' in data:
        add_test_to_db(data)

    return render_template('test.html', favorite=favorite_value)



@app.route("/home/<student_number>", methods=['GET', 'POST'])
def home(student_number):
    # Access the student_number from the URL and the session
    student_number = student_number or session.get('student_number', default_value)

    # Rest of your code
    carousel_courses = load_carousel_courses_from_db()
    num_carousel_courses = len(carousel_courses)
    best_courses = load_best_courses_with_favorite_from_db(student_number)
    explore_courses = load_explore_courses_from_db()
    compulsory_courses = load_compulsory_courses_from_db()

    for course in best_courses:
      print(course['course_code'])

    data = request.form  # Moved the data assignment here

    favorite_value = None
    if request.method == 'POST' and 'favorite' in data:
        add_test_to_db(data, student_number)
        selected_course_code = data.get("course_code")
        favorite_value = data.get("favorite")
        print(selected_course_code, favorite_value)


    return render_template('home.html', student_number=student_number, carousel_courses=carousel_courses, num_carousel_courses=num_carousel_courses, best_courses=best_courses, explore_courses=explore_courses, compulsory_courses=compulsory_courses, favorite=favorite_value)






@app.route("/home/<student_number>/<course_code>/rating", methods=['POST'])
def sumbit_favorite(student_number, course_code):
    data = request.form
    student_number = student_number or session.get('student_number', default_value)
    carousel_courses = load_carousel_courses_from_db()
    num_carousel_courses = len(carousel_courses)
    # Fetch best courses along with user ratings
    best_courses = load_best_courses_from_db(student_number)
    explore_courses = load_explore_courses_from_db()
    compulsory_courses = load_compulsory_courses_from_db()
    # Put the new rating into the database
    put_rating_to_db(student_number, course_code, data)
    # Fetch the user's ratings again after the update
    best_courses = load_best_courses_from_db(student_number)

    return render_template('home.html', student_number=student_number, carousel_courses=carousel_courses, num_carousel_courses=num_carousel_courses, best_courses=best_courses, explore_courses=explore_courses, compulsory_courses=compulsory_courses)




      
@app.route("/courses")
def hello_world():
    courses = load_courses_from_db()
    return render_template('courses.html', courses=courses, filters=filters)


@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

@app.route("/api/courses")
def list_courses():
  courses = load_courses_from_db()
  return jsonify(courses)




@app.route("/course/<student_number>/<course_code>")
def show_course(student_number, course_code):
    # Load the course data
    courses = load_courses_from_db()
    course = [course for course in courses if course.get('course_code') == course_code]

    if not course:
        return "Not Found", 404

    print(student_number)
    print(course_code)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_views_to_db(student_number, course_code, timestamp)

    return render_template('coursepage.html', course=course[0])











if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)