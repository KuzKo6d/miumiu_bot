import psycopg2

import psycopg2

conn = psycopg2.connect(
    dbname="message",
    user="user",
    password="insecure",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


def write(message, chat_id, user_id, role) -> None:
    cursor.execute('''
    INSERT INTO messages (message, chat_id, user_id, role, deleted)
    VALUES (%s, %s, %s, %s, %s);
    ''', (message, chat_id, user_id, role, False))

    conn.commit()


def read_by_chat_id(chat_id) -> list:
    cursor.execute('''
    SELECT * FROM messages WHERE (chat_id = %s) AND (deleted = %s);
    ''', (chat_id, False))
    rows = cursor.fetchall()

    return [{'content': row[1], 'role': row[4]} for row in rows]

def delete(chat_id) -> None:
    cursor.execute('''
    UPDATE messages SET deleted = %s WHERE (chat_id = %s) AND (deleted = %s);
    ''', (True, chat_id, False))
    conn.commit()

print(read_by_chat_id(80085))