import sqlite3
import logging


db = sqlite3.connect('database/db.sqlite3', check_same_thread=False, isolation_level='EXCLUSIVE')


def create_table_users() -> None:
    """
    Создание таблицы
    :return: None
    """
    logging.info("table_users")
    with db:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT,
            age INTEGER,
            honor INTEGER,
            data_registration TEXT
        )""")
        db.commit()


def check_user(tg_id: int) -> bool:
    logging.info(f'check_user')
    with db:
        sql = db.cursor()
        sql.execute('SELECT tg_id FROM users')
        list_user = [row[0] for row in sql.fetchall()]
        if int(tg_id) in list_user:
            return True
        else:
            return False


def add_user(tg_id: int, username: str) -> None:
    logging.info(f'add_user')
    with db:
        sql = db.cursor()
        if not check_user(tg_id=tg_id):
            sql.execute(f'INSERT INTO users (tg_id, username, name, age, honor, data_registration)'
                        f' VALUES ("{tg_id}", "{username}", "name", 0, 0, "01-01-0001")')
            db.commit()


def get_user(tg_id: int) -> tuple:
    """
    ПОЛЬЗОВАТЕЛЬ - имя пользователя по его id
    :param tg_id:
    :return:
    """
    logging.info(f'get_user')
    with db:
        sql = db.cursor()
        return sql.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,)).fetchone()


def set_user_name(tg_id: int, name: str) -> None:
    """
    Устанавливаем имя пользователю
    :param tg_id:
    :param name:
    :return:
    """
    logging.info("set_user_name")
    with db:
        cursor = db.cursor()
        if check_user(tg_id=tg_id):
            cursor.execute("UPDATE users SET name = ? WHERE tg_id = ?", (name, tg_id))
            db.commit()


def set_user_age(tg_id: int, age: int, data_registration: str) -> None:
    """
    Устанавливаем имя пользователю
    :param tg_id:
    :param age:
    :param data_registration:
    :return:
    """
    logging.info("set_user_name")
    with db:
        cursor = db.cursor()
        if check_user(tg_id=tg_id):
            cursor.execute("UPDATE users SET age = ?, data_registration = ? WHERE tg_id = ?",
                           (age, data_registration, tg_id))
            db.commit()

