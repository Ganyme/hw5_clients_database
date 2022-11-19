import psycopg2

class Clients:
    def delete_db(cur):
        cur.execute('''
                DROP TABLE phones CASCADE;
                DROP TABLE clients CASCADE;
                ''')
    def create_db(cur):
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            email VARCHAR(40) UNIQUE NOT NULL
        ); 
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone VARCHAR(15),
            client_id INTEGER REFERENCES clients(client_id)
        );
        ''')
    def add_client(cur, first_name, last_name, email):
        cur.execute('''
        INSERT INTO clients(first_name, last_name, email)
        VALUES (%s, %s, %s);
        ''', (first_name, last_name, email))
    def add_phone(cur, client_id, phone):
        cur.execute('''
        INSERT INTO phones(phone, client_id)
        VALUES (%s, %s);
        ''', (phone, client_id))

    def change_client(cur, client_id, first_name=None, last_name=None, email=None):
        if first_name != None:
            cur.execute('''
            UPDATE clients SET first_name = %s WHERE client_id= %s;
            ''', (first_name, client_id))
        if last_name != None:
            cur.execute('''
            UPDATE clients SET last_name = %s WHERE client_id= %s;
            ''', (last_name, client_id))
        if email != None:
            cur.execute('''
            UPDATE clients SET email = %s WHERE client_id= %s;
            ''', (email, client_id))

    def delete_phone(cur, client_id):
        cur.execute('''
               DELETE FROM phones
               WHERE client_id = %s;
               ''', client_id)

    def delete_client(cur, client_id):
        cur.execute('''
                   DELETE FROM phones 
                   WHERE client_id = %s;
                   ''', client_id)
        cur.execute('''
                   DELETE FROM clients 
                   WHERE client_id = %s;
                   ''', client_id)

    def find_client(cur, first_name=None, last_name=None, email=None):
        cur.execute('''
        SELECT * FROM clients c
        FULL JOIN phones p ON c.client_id = p.client_id
        WHERE first_name = %s OR last_name = %s OR email = %s;
        ''', (first_name, last_name, email))
        print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="clients", user="postgres", password="***") as conn:
        with conn.cursor() as cur:
            Clients.delete_db(cur)
            Clients.create_db(cur)
            Clients.add_client(cur, 'Ivan', 'Ivanov', 'ivanov@gmail.com')
            Clients.add_client(cur, 'Peter', 'Petrov', 'petrov@gmail.com')
            Clients.add_client(cur, 'Violetta', 'Violetova', 'vi@gmail.com')
            Clients.add_phone(cur, 1, '(999)999-99-99')
            Clients.add_phone(cur, 2, '(999)999-99-88')
            Clients.add_phone(cur, 3, '(999)999-99-77')
            Clients.add_phone(cur, 3, '(999)999-99-66')
            Clients.add_phone(cur, 3, '(999)999-99-55')
            Clients.change_client(cur, 1, 'Oscar', 'Osetrov')
            Clients.delete_phone(cur, '2')
            Clients.delete_client(cur, '3')
            Clients.find_client(cur, 'Oscar', 'Osetrov')
            cur.close()
        conn.close()


