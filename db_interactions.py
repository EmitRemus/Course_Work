import base64

import mysql.connector


class db_config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'ManTikor12'
    MYSQL_DB = 'pass_save_db'


def get_db_connection():
    connection = mysql.connector.connect(
        host=db_config.MYSQL_HOST,
        user=db_config.MYSQL_USER,
        password=db_config.MYSQL_PASSWORD,
        database=db_config.MYSQL_DB
    )
    return connection


SQL_SELECT_USER_BY_EMAIL = "SELECT * FROM users WHERE mail = %s".strip()
SQL_INSERT_USER = "INSERT INTO users (mail, name) VALUES (%s, %s)".strip()
SQL_SELECT_USER_ID_BY_EMAIL = "SELECT id FROM users WHERE mail = %s".strip()
SQL_SELECT_PASSWORDS_BY_USER_ID = "SELECT * FROM passwords WHERE user_id = %s".strip()
SQL_INSERT_PASSWORD = """
INSERT INTO passwords (user_id, password, used_for, salt, iv_password, iv_used_for) VALUES (%s, %s, %s, %s, %s, %s)""".strip()
SQL_UPDATE_PASSWORD = """
UPDATE passwords SET password = %s, used_for = %s, salt = %s, iv_password = %s, iv_used_for = %s WHERE password_id = %s""".strip()
SQL_DELETE_PASSWORD_BY_ID = "DELETE FROM passwords WHERE password_id = %s".strip()
SQL_SELECT_PASSWORD_BY_ID = "SELECT * FROM passwords WHERE password_id = %s".strip()


def get_user_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(SQL_SELECT_USER_BY_EMAIL, (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user


def insert_user(email, name):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(SQL_INSERT_USER, (email, name))
    connection.commit()
    cursor.close()
    connection.close()


def get_user_id(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(SQL_SELECT_USER_ID_BY_EMAIL, (email,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user['id']


def get_encrypted_passwords(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(SQL_SELECT_PASSWORDS_BY_USER_ID, (user_id,))
    passwords = cursor.fetchall()
    cursor.close()
    connection.close()
    return passwords


def insert_password(user_id, encrypted_password, encrypted_description, salt, iv_password, iv_description):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        SQL_INSERT_PASSWORD,
        (user_id, encrypted_password, encrypted_description, base64.b64encode(salt).decode('utf-8'), iv_password,
         iv_description)
    )
    connection.commit()
    cursor.close()
    connection.close()


def update_password(id, encrypted_password, encrypted_description, salt, iv_password, iv_description):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        SQL_UPDATE_PASSWORD,
        (encrypted_password, encrypted_description, base64.b64encode(salt).decode('utf-8'), iv_password, iv_description,
         id)
    )
    connection.commit()
    cursor.close()
    connection.close()


def delete_password_by_id(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(SQL_DELETE_PASSWORD_BY_ID, (id,))
    connection.commit()
    cursor.close()
    connection.close()


def get_password_by_id(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(SQL_SELECT_PASSWORD_BY_ID, (id,))
    password_entry = cursor.fetchone()
    cursor.close()
    connection.close()
    return password_entry
