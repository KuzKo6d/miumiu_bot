import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

#  postgres
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

conn = psycopg2.connect(
    dbname=POSTGRES_DB_NAME,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
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
