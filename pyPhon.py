""" Создание базы данных
    CREATE DATABASE PHONBASE;
"""
import psycopg2


with (psycopg2.connect(database="PHONBASE", user="postgres", password="Ak200213!") as conn):
    with conn.cursor() as cur:
        def create_db(conn):
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
            conn.commit()
        # create_db(conn)

        def add_client(conn, client_id, first_name, last_name, email, phone):
            cur.execute("""
                INSERT INTO customers(client_id, first_name, last_name, email) VALUES(%s, %s, %s, %s);
                """, (client_id, first_name, last_name, email))
            conn.commit()
            cur.execute("""
                INSERT INTO phones(client_id, phone) VALUES(%s, %s);
                """, (client_id, phone))
            conn.commit()
        # add_client(conn, 1, 'first_name_1', 'last_name_1', '@mail_1', '+7922xxxxxxx')
        # add_client(conn, 2, 'first_name_2', 'last_name_2', '@mail_2', '+7982xxxxxxx')

        def add_phone(conn, client_id, phone):
            cur.execute("""
                INSERT INTO phones(client_id, phone) VALUES(%s, %s);
                """, (client_id, phone))
            conn.commit()
        # add_phone(conn, 1, '+7952xxxxxxx')
        # add_phone(conn, 2, '+7902xxxxxxx')

        def change_client_all(conn, first_name, last_name, email, client_id):
            cur.execute("""
                UPDATE customers SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s;
                """, (first_name, last_name, email, client_id))
            conn.commit()
        # change_client_all(conn, 'Andrew','Kovalev', 'mail@mail.ru', 1)

        def find_client(conn, first_name, last_name, email, phone):
            cur.execute("""
                SELECT * FROM customers, phones
                WHERE (first_name=%s OR last_name=%s OR email=%s OR phone=%s) AND customers.client_id = phones.client_id;
                """, (first_name, last_name, email, phone))
            print(cur.fetchall())
        # find_client(conn, '%%', '%%', '%%', '+7952xxxxxxx')

        def delete_phone(conn, phone, client_id):
            cur.execute("""
                DELETE FROM phones WHERE phone=%s AND client_id=%s;
                """, (phone, client_id))
            conn.commit()
        # delete_phone(conn, '+7982xxxxxxx', 2)

        def delete_client(conn, client_id):
            cur.execute("""
                DELETE FROM phones WHERE client_id=%s;
                """, (client_id,))
            conn.commit()
            cur.execute("""
                DELETE FROM customers WHERE client_id=%s;
                """, (client_id,))
            conn.commit()
        # delete_client(conn, 1)

        # conn.close()
