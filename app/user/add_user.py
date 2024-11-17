import bcrypt
import psycopg2

def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password

def add_user(data):
    # Connect to the database
    connection = psycopg2.connect(
        dbname="tpd",
        user="tpd",
        password="tpd",
        host="samuelmoore.cc",
        port="5432"
    )
    cursor = connection.cursor()

    # Hash the password
    password_hash = hash_password(data['plain_text_password'])

    # SQL query to insert the new user
    insert_query = """
    INSERT INTO users (first_name, last_name, age, gender, ethnicity, first_language, interests, personal_goals, milestone_completed, exercise_completed, question_completed, password_hash)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        data['first_name'], 
        data['last_name'], 
        data['age'], 
        data['gender'], 
        data['ethnicity'], 
        data['first_language'], 
        data['interests'], 
        data['personal_goals'], 
        data['milestone_completed'], 
        data['exercise_completed'], 
        data['question_completed'], 
        password_hash
    ))

    # Commit and close connection
    connection.commit()
    cursor.close()
    connection.close()
