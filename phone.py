import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS customers(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(50)
            );""")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES customers(client_id),
            phone VARCHAR(12)
            );""")

def add_client(conn, client_id, first_name, last_name, email, phone):
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO customers(client_id, first_name, last_name, email) VALUES(%s, %s, %s, %s);
            """, (client_id, first_name, last_name, email))
        cur.execute("""INSERT INTO phones(client_id, phone) VALUES(%s, %s);
            """, (client_id, phone))

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
            """, (client_id, phone))

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
            """, (client_id, phone))

def change_client_first_name(conn, first_name, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE customers SET first_name=%s WHERE client_id=%s;
            """, (first_name, client_id))

def change_client_last_email(conn, last_name, email, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE customers SET last_name=%s, email=%s WHERE client_id=%s;
            """, (last_name, email, client_id))

def change_client_all(conn, first_name, last_name, email, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE customers SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s;
            """, (first_name, last_name, email, client_id))

def find_client(conn, first_name, last_name, email, phone):
    with conn.cursor() as cur:
        cur.execute("""
             SELECT * FROM customers, phones
             WHERE first_name LIKE %s AND last_name LIKE %s
             AND email LIKE %s AND phone LIKE %s
             AND customers.client_id=phones.client_id;
             """, (first_name, last_name, email, phone))
        print(cur.fetchall())

def delete_phone(conn, phone, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones WHERE phone=%s AND client_id=%s;
            """, (phone, client_id))

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            DELETE FROM customers WHERE client_id=%s;
            """, (client_id,))

with (psycopg2.connect(database="PHONBASE", user="postgres", password="Ak200213!") as conn):

    create_db(conn)

    add_client(conn, 1, 'first_name_1', 'last_name_1', '@mail_1', '+7922xxxxxxx')
    add_client(conn, 2, 'first_name_2', 'last_name_2', '@mail_2', '+7982xxxxxxx')

    add_phone(conn, 1, '+7952xxxxxxx')
    add_phone(conn, 2, '+7902xxxxxxx')

    # Не нашел как проще сделать UPDATE для выборочных полей.
    change_client_first_name(conn, 'Andy', 1)
    change_client_last_email(conn, 'last_name', 'email', 1)
    change_client_all(conn, 'Andrew','Kovalev', 'mail@mail.ru', 1)

    # Не нашел других решений.
    # Выбор по полям, используя шаблон %. Например: по букве v поля last_name
    find_client(conn, '%%', '%v%', '%%', '%%')

    # delete_phone(conn, '+7952xxxxxxx', 1)
    # delete_client(conn, 1)
    # delete_client(conn, 2)

conn.close()