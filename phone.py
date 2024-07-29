import psycopg2


with (psycopg2.connect(database="PHONBASE", user="postgres", password="Ak200213!") as conn):

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
    # create_db(conn)

    def add_client(conn, client_id, first_name, last_name, email, phone):
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO customers(client_id, first_name, last_name, email) VALUES(%s, %s, %s, %s);
                """, (client_id, first_name, last_name, email))
            cur.execute("""INSERT INTO phones(client_id, phone) VALUES(%s, %s);
                """, (client_id, phone))
    # add_client(conn, 1, 'first_name_1', 'last_name_1', '@mail_1', '+7922xxxxxxx')
    # add_client(conn, 2, 'first_name_2', 'last_name_2', '@mail_2', '+7982xxxxxxx')

    def add_phone(conn, client_id, phone):
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s);
                """, (client_id, phone))
    # add_phone(conn, 1, '+7952xxxxxxx')
    # add_phone(conn, 2, '+7902xxxxxxx')

    def change_client(conn, first_name, last_name, email, client_id):
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE customers SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s;
                """, (first_name, last_name, email, client_id))
    # change_client(conn, 'Andrew','Kovalev', 'mail@mail.ru', 1)

    def find_client(conn, first_name, last_name, email, phone):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM customers, phones
                WHERE first_name LIKE %s AND last_name LIKE %s
                AND email LIKE %s AND phone LIKE %s;
                """, (first_name, last_name, email, phone))
            print(cur.fetchall())
    # find_client(conn, 'A%', '%%', '%ru', '%22%')

    def delete_phone(conn, phone, client_id):
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM phones WHERE phone=%s AND client_id=%s;
                """, (phone, client_id))
    # delete_phone(conn, '+7982xxxxxxx', 2)

    def delete_client(conn, client_id):
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM phones WHERE client_id=%s;
                """, (client_id,))
            cur.execute("""
                DELETE FROM customers WHERE client_id=%s;
                """, (client_id,))
    # delete_client(conn, 1)
    # delete_client(conn, 2)

conn.close()