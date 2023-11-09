from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import os
from algorithm import get_recommendations

# Rest of your code remains the same

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }
)

def load_courses_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM r_courses"))
    courses = []
    columns = result.keys()
    for row in result:
      result_dict = {column: value for column, value in zip(columns, row)}
      courses.append(result_dict)
    return courses


def load_carousel_courses_from_db(student_number):
  with engine.connect() as conn:
      query = text("""
          SELECT c.*, rf.rating 
          FROM r_courses c
          LEFT JOIN r_favorites4 rf
          ON c.course_code = rf.course_code AND rf.student_number = :student_number
      """)

      result = conn.execute(query, {"student_number": student_number})

      carousel_courses = []
      columns = result.keys()
      for row in result:
          result_dict = {column: value for column, value in zip(columns, row)}
          carousel_courses.append(result_dict)

      return carousel_courses


def load_best_courses_with_favorite_from_db(student_number):
  with engine.connect() as conn:
      query = text("""
          SELECT c.*, rf.rating 
          FROM r_courses c
          LEFT JOIN r_favorites4 rf
          ON c.course_code = rf.course_code AND rf.student_number = :student_number
      """)
    
      result = conn.execute(query, {"student_number": student_number})

      best_courses = []
      columns = result.keys()
      for row in result:
          result_dict = {column: value for column, value in zip(columns, row)}
          best_courses.append(result_dict)

      return best_courses






def add_test_to_db(request, student_number, course_code, favorite_value):
  with engine.connect() as conn:
      # Check if the record already exists
      existing_record = conn.execute(
          text("SELECT * FROM r_favorites4 WHERE course_code = :course_code AND student_number = :student_number"),
          {"course_code": course_code, "student_number": student_number}
      ).fetchone()

      # Fetch the 'id' from 'course_info' based on the 'course_code'
      course_info_id = conn.execute(
          text("SELECT id FROM r_courses WHERE course_code = :course_code"),
          {"course_code": course_code}
      ).fetchone()

      if course_info_id:
          course_info_id = course_info_id[0]
      else:
          # Handle the case where 'course_code' doesn't exist in 'course_info'
          # You can raise an exception, return an error, or handle it as needed
          # For now, I'm assuming you want to set it to NULL
          course_info_id = None

      print(f"Retrieved id for course_code={course_code}: id={course_info_id}")

      if existing_record:
          # Update the existing record
          query = text("UPDATE r_favorites4 SET rating = :rating, id = :id WHERE course_code = :course_code AND student_number = :student_number")
      else:
          # Insert a new record
          query = text("INSERT INTO r_favorites4 (course_code, student_number, rating, id) VALUES (:course_code, :student_number, :rating, :id)")

      conn.execute(query, {"course_code": course_code, "student_number": student_number, "rating": favorite_value, "id": course_info_id})



def load_favorite_courses_from_db(student_number):
    with engine.connect() as conn:
      query = text(""" 
          SELECT rf.*, c.course_code, c.course_name, c.content
          FROM r_courses c
          LEFT JOIN r_favorites4 rf
          ON c.course_code = rf.course_code AND rf.student_number =:student_number
          WHERE rf.rating = 'on' 
      """)
      
      result = conn.execute(query, {"student_number": student_number})
      
      favorite_courses = []
      columns = result.keys()
      for row in result:
          result_dict = {column: value for column, value in zip(columns, row)}
          favorite_courses.append(result_dict)
      return favorite_courses


def add_login_to_db(student_number, password, level, education):
  with engine.connect() as conn:
      conn.execute(
          text("INSERT INTO r_users (student_number, password, level, education) VALUES (:student_number, :password, :level, :education)"),
          {"student_number": student_number, "password": password, "level": level, "education": education}
      )

def check_credentials(student_number, password):
  with engine.connect() as conn:
      result = conn.execute(
          text("SELECT * FROM r_users WHERE student_number = :student_number AND password = :password"),
          {"student_number": student_number, "password": password}
      )
      return result.fetchone() is not None

def add_interests_to_db(data):
  with engine.connect() as conn:
      query = text("INSERT INTO r_users (manamgement, data, law, businesses, psychology, economics, statistics, finance, philosophy, sociology, entrepreneurship, marketing, accounting, econometrics, media, ethics, programming, health, society, technology, communication, history, culture, language, Bachelor, Master) "
                   "VALUES (:manamgement, :data, :law, :businesses, :psychology, :economics, :statistics, :finance, :philosophy, :sociology, :entrepreneurship, :marketing, :accounting, :econometrics, :media, :ethics, :programming, :health, :society, :technology, :communication, :history, :culture, :language,  :Bachelor, :Master)")

      # Construct the parameter dictionary
      params = {
            'management': data.get('management'),
            'data':data.get('data'),
            'law': data.get('law'),
            'businesses': data.get('businesses'),
            'psychology': data.get('psychology'),
            'economics': data.get('economics'),
            'statistics': data.get('statistics'),
            'finance': data.get('finance'),
            'philosophy': data.get('philosophy'),
            'sociology': data.get('sociology'),
            'entrepreneurship': data.get('entrepreneurship'),
            'marketing': data.get('marketing'),
            'accounting': data.get('accounting'),
            'econometrics': data.get('econometrics'),
            'media': data.get('media'),
            'ethics': data.get('ethics'),
            'programming': data.get('programming'),
            'health': data.get('health'),
            'society': data.get('society'),
            'technology': data.get('technology'),
            'communication': data.get('communication'),
            'history': data.get('history'),
            'culture': data.get('culture'),
            'language': data.get('language'),
            'Bachelor': data.get('Bachelor'),
            'Master': data.get('Master'),
        }
      

      conn.execute(query, params)


def update_interests(student_number, password, data):
  with engine.connect() as conn:
      query = text(
          "UPDATE r_users SET "
          "management = :management, "
          "data = :data, "
          "law = :law, "
          "businesses = :businesses, "
          "psychology = :psychology, "
          "economics = :economics, "
          "statistics = :statistics, "
          "finance = :finance, "
          "philosophy = :philosophy, "
          "sociology = :sociology, "
          "entrepreneurship = :entrepreneurship, "
          "marketing = :marketing, "
          "accounting = :accounting, "
          "econometrics = :econometrics, "
          "media = :media, "
          "ethics = :ethics, "
          "programming = :programming, "
          "health = :health, "
          "society = :society, "
          "technology = :technology, "
          "communication = :communication, "
          "history = :history, "
          "culture = :culture, "
          "language = :language, "
          "Bachelor = :Bachelor, "
          "Master = :Master "
              "WHERE student_number = :student_number AND password = :password"
          )
# Add student_number and password to the parameter dictionary
      params = {
          'management': data.get('management'),
          'data':data.get('data'),
          'law': data.get('law'),
          'businesses': data.get('businesses'),
          'psychology': data.get('psychology'),
          'economics': data.get('economics'),
          'statistics': data.get('statistics'),
          'finance': data.get('finance'),
          'philosophy': data.get('philosophy'),
          'sociology': data.get('sociology'),
          'entrepreneurship': data.get('entrepreneurship'),
          'marketing': data.get('marketing'),
          'accounting': data.get('accounting'),
          'econometrics': data.get('econometrics'),
          'media': data.get('media'),
          'ethics': data.get('ethics'),
          'programming': data.get('programming'),
          'health': data.get('health'),
          'society': data.get('society'),
          'technology': data.get('technology'),
          'communication': data.get('communication'),
          'history': data.get('history'),
          'culture': data.get('culture'),
          'language': data.get('language'),
          'Bachelor': data.get('Bachelor'),
          'Master': data.get('Master'),
          'student_number': student_number,
          'password': password
      }

      conn.execute(query, params)
    
def add_views_to_db(student_number, course_code, timestamp, id):
  with engine.connect() as conn:
      # Retrieve the 'id' value from the "r_courses" table based on the 'course_code'
      course_info_id = conn.execute(
          text("SELECT id FROM r_courses WHERE course_code = :course_code"),
          {"course_code": course_code}
      ).fetchone()

      if course_info_id:
          course_info_id = course_info_id[0]
      else:
          course_info_id = None

      # Check if a record with the same 'id' and 'student_number' combination already exists in "r_views"
      existing_record = conn.execute(
          text("SELECT id FROM r_views WHERE student_number = :student_number AND id = :id"),
          {"student_number": student_number, "id": course_info_id}
      ).fetchone()

      if not existing_record:
          # If no matching record exists, proceed with the insert
          query = text("INSERT INTO r_views (course_code, student_number, timestamp, id) VALUES (:course_code, :student_number, :timestamp, :id)")
          conn.execute(query, {"course_code": course_code, "student_number": student_number, "timestamp": timestamp, "id": course_info_id})

     



      
     





def get_ratings_from_database(student_number):
  with engine.connect() as conn:
      query = text("SELECT course_code, rating FROM r_favorites4 WHERE student_number = :student_number")
      result = conn.execute(query, {"student_number": student_number})

      # Create a dictionary to store the ratings for each course
      ratings = {row.course_code: row.rating for row in result}
  return ratings




def get_recommendations_with_ratings(student_number):
  recommendations = get_recommendations(student_number)  # Retrieve recommended courses as before
  rated_courses = get_ratings_from_database(student_number)  # Retrieve the ratings from the database
  
  for recommendation_set in recommendations:
      for recommendation in recommendation_set['recommended_courses']:
          course_code = recommendation['course_code']  # Access 'course_code' within the nested structure
          # Check if there is a rating for the current course in the rated_courses list
          if course_code in rated_courses:
              recommendation['liked'] = rated_courses[course_code]
              #print(f"Course {course_code} is marked as {rated_courses[course_code]}")
          else:
              # If no rating found, assume 'off'
              recommendation['liked'] = 'off'
              
  
  return recommendations


















