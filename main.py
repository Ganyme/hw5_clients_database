import psycopg2

class Clients:
    def create_db(conn):
        with conn.cursor() as cur:
            cur.execute('''
            DROP TABLE phones CASCADE;
            DROP TABLE clients CASCADE;
            ''')
            cur.execute('''
            CREATE TABLE IF NOT EXISTS clients(
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(20) NOT NULL,
                surname VARCHAR(30) NOT NULL,
                email VARCHAR(40) UNIQUE NOT NULL
            ); 
            ''')
            cur.execute('''
            CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                number VARCHAR(15),
                client_id INTEGER REFERENCES clients(client_id)
            );
            ''')
            conn.commit()

    def add_client(conn):
        name = input('Имя клиента: ')
        surname = input('Фамилия клиента: ')
        email = input('email клиента: ')
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO clients(name, surname, email)
            VALUES (%s, %s, %s);
            ''', (name, surname, email))
            conn.commit()
        print ('Новый клиент добавлен в базу.')

    def add_phone(conn):
        id = int(input('Ведите ID клиента, которому хотите добавить номер телефона: '))
        phone = input('Введите номер телефона: ')
        with conn.cursor() as cur:
            cur.execute('''
            INSERT INTO phones(number, client_id)
            VALUES (%s, %s);
            ''', (phone, id))
            conn.commit()
        print ('Телефон добавлен.')

    def change_client(conn, phone=None):
        id = int(input('Ведите ID клиента, данные которого хотите изменить: '))
        name = input('Введите новое имя: ')
        surname = input('Введите новую фамилию: ')
        email = input('Введите новый имейл: ')
        with conn.cursor() as cur:
            cur.execute('''
            UPDATE clients SET name = %s, surname = %s, email = %s WHERE client_id= %s;
            ''', (name, surname, email, id))
            conn.commit()
        print ('Данные клиента изменены.')

    def delete_phone(conn):
        id = input('Ведите ID клиента, телефон которого хотите удалить: ')
        with conn.cursor() as cur:
            cur.execute('''
                   DELETE FROM phones
                   WHERE client_id = %s;
                   ''', id)
            conn.commit()
        print('Телефон удален.')

    def delete_client(conn):
        id = input('Ведите ID клиента, которого хотите удалить из базы: ')
        with conn.cursor() as cur:
            cur.execute('''
                       DELETE FROM clients 
                       WHERE client_id = %s;
                       ''', (id))
            conn.commit()
        print('Карточка клиента удалена.')

    def find_client(conn):
        keyword = input('Введите имя, фамилию, имейл или телефон клиента: ')
        with conn.cursor() as cur:
            cur.execute('''
            SELECT * FROM clients c
            FULL JOIN phones p ON c.client_id = p.client_id
            ''')
            data = cur.fetchall()
        for card in data:
            if keyword in card:
                print(f'Данные клиента: {card}')

# Соединение с базой и вызов функций

with psycopg2.connect(database="clients_db", user="postgres", password="***") as conn:
    Clients.create_db(conn)
    commands = ['a', 'p', 'c', 'r', 'd', 'f']
    while True:
        print('Что сделать? \n'
              'a — добавить в базу нового клиента;\n'
              'p — добавить телефон для существующего клиента;\n'
              'c — изменить данные о клиенте;\n'
              'r — удалить телефон существующего клиента;\n'
              'd — удалить из базы все данные о клиенте; \n'
              'f — найти клиента по его данным.')
        command = input('Введите команду: ')
        if command not in commands:
            print('Неверная команда')
            continue
        elif command == 'a':
            Clients.add_client(conn)
        elif command == 'p':
            Clients.add_phone(conn)
        elif command == 'c':
            Clients.change_client(conn, phone=None)
        elif command == 'r':
            Clients.delete_phone(conn)
        elif command == 'd':
            Clients.delete_client(conn)
        elif command == 'f':
            Clients.find_client(conn)
