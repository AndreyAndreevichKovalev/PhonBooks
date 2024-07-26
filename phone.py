""" Создание базы данных
    CREATE DATABASE BASE;
"""
import  psycopg2


def create_db(conn):
    """Функция, создающая структуру БД (таблицы)"""
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS customers(
        client_id INTEGER UNIQUE PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(50)
        );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES customers(client_id),
        phone VARCHAR(12)
        );""")

def add_client(conn, client_id, first_name, last_name, email, phone):
    """Функция, позволяющая добавить нового клиента"""
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO customers(client_id, first_name, last_name, email) VALUES(%s, %s, %s, %s);
        """, (client_id, first_name, last_name, email))
    cur.execute("""
        INSERT INTO phones(client_id, phone) VALUES(%s, %s);
        """, (client_id, phone))

def add_phone(conn, client_id, phone):
    """Функция, позволяющая добавить телефон для существующего клиента"""
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO phones(client_id, phone) VALUES(%s, %s);
        """, (client_id, phone))

def change_client(conn, first_name, last_name, email, client_id):
    """Функция, позволяющая изменить данные о клиенте"""
    cur = conn.cursor()
    cur.execute("""
        UPDATE customers SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s;
        """, (first_name, last_name, email, client_id))

def delete_phone(conn, phone, client_id):
    """Функция, позволяющая удалить телефон для существующего клиента"""
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM phones WHERE phone=%s AND client_id=%s;
        """, (phone, client_id))


def delete_client(conn, client_id):
    """Функция, позволяющая удалить существующего клиента"""
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM customers WHERE client_id=%s;
        """, (client_id,))

def find_first_name_client(conn, first_name, last_name, email, phone):
    """Функция, позволяющая найти клиента по его данным: имени"""
    cur = conn.cursor()
    cur.execute("""
        SELECT first_name, last_name, email, phone FROM customers, phones
        WHERE first_name=%s AND customers.client_id = phones.client_id;
        """, (first_name,))
    
def find_last_name_client(conn, first_name, last_name, email, phone):
    """Функция, позволяющая найти клиента по его данным: фамилии"""
    cur = conn.cursor()
    cur.execute("""
        SELECT first_name, last_name, email, phone FROM customers, phones
        WHERE last_name=%s AND customers.client_id = phones.client_id;
        """, (last_name,))

def find_email_client(conn, first_name, last_name, email, phone):
    """Функция, позволяющая найти клиента по его данным: почте"""
    cur = conn.cursor()
    cur.execute("""
        SELECT first_name, last_name, email, phone FROM customers, phones
        WHERE email = %s AND customers.client_id = phones.client_id;
        """, (email,))

def find_phone_client(conn, first_name, last_name, email, phone):
    """Функция, позволяющая найти клиента по его данным: телефону"""
    cur = conn.cursor()
    cur.execute("""
        SELECT first_name, last_name, email, phone FROM customers, phones
        WHERE phone=%s AND customers.client_id = phones.client_id;
        """, (phone,))
