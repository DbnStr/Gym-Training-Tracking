import psycopg2
from typing import Union, Tuple

db_config = {
    'dbname': 'gym_training_tracking',
    'user': 'muscle_man',
    'password': '12345678',
    'host': 'localhost'
}

def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn


def execute_select_one_query(query: str):
    with get_db_connection().cursor() as cursor:
        cursor.execute(query)
        entry = cursor.fetchone()
        return entry

def execute_select_all_query(query: str):
    with get_db_connection().cursor() as cursor:
        cursor.execute(query)
        entry = cursor.fetchall()
        return entry

def insert(table_name: str, entry: dict):
    column_names = ', '.join([k for k in entry.keys()])
    values = ', '.join('%s' for _ in entry.keys())
    query = 'INSERT INTO {}({}) VALUES ({})'.format(table_name, column_names, values)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, list(entry.values()))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
        return False
    return True

def insert_strengthExercise(entry: dict):
    column_names = ', '.join([k for k in entry.keys()])
    values = ', '.join('%s' for _ in entry.keys())
    query = 'INSERT INTO strength_exercise ({}) VALUES ({}) RETURNING strengthexerciseid'.format(column_names, values)
    conn = get_db_connection()
    try:
        entry
        with conn.cursor() as cursor:
            cursor.execute(query, list(entry.values()))
            entry = cursor.fetchone()
        conn.commit()
        return entry
    except Exception as e:
        conn.rollback()
        print(e)
        return False

def get_all_trainings(customer_id: int):
    return execute_select_all_query('SELECT * FROM training WHERE customerid={}'.format(customer_id))

def user_exists(email, phoneNumber: str):
    user = 'SELECT * FROM Customer WHERE email = \'{}\' OR phonenumber = \'{}\''.format(email, phoneNumber)
    return not execute_select_one_query(user) is None

def get_consumer_by_email(email: str):
    return execute_select_one_query('SELECT * FROM Customer WHERE email = \'{}\''.format(email))

def get_by_unique_int(table: str, by: str, value: int) -> Union[Tuple, None]:
    return execute_select_one_query('SELECT * FROM {} WHERE {}={}'.format(table, by, value))

def get_all_running_exercise(training_id: int):
    return execute_select_all_query('SELECT * FROM running_exercise WHERE trainingid={}'.format(training_id))

def get_last_training(customerId: int):
    return execute_select_one_query('SELECT MAX (trainingId) FROM training WHERE customerid={}'.format(customerId))[0]

def complete_training(trainingId: int, datetime_of_finish: str):
    query = 'UPDATE training SET datetimeoffinish=\'{}\' WHERE trainingid={} RETURNING *'.format(datetime_of_finish, trainingId)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)
        return False
    return True
