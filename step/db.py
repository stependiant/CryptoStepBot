import psycopg2
from config import POSTGRES_CONN_STRING

def get_connection():
    return psycopg2.connect(POSTGRES_CONN_STRING)

def init_db():
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    coin VARCHAR(10),
                    interval INTEGER
                )
            """)
            curs.execute("""
                CREATE TABLE IF NOT EXISTS news_subscriptions (
                    user_id BIGINT PRIMARY KEY
                )
            """)
    conn.close()

def add_subscription(user_id, coin, interval):
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO subscriptions (user_id, coin, interval)
                VALUES (%s, %s, %s)
            """, (user_id, coin, interval))
    conn.close()

def remove_subscription(user_id, coin):
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                DELETE FROM subscriptions WHERE user_id = %s AND coin = %s
            """, (user_id, coin))
    conn.close()

def get_subscriptions(user_id):
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT coin, interval FROM subscriptions WHERE user_id = %s
            """, (user_id,))
            result = curs.fetchall()
    conn.close()
    return result

def get_all_subscriptions():
    """Возвращает все подписки из БД"""
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT user_id, coin, interval FROM subscriptions
            """)
            result = curs.fetchall()
    conn.close()
    return result

def add_news_subscription(user_id):
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO news_subscriptions (user_id)
                VALUES (%s)
                ON CONFLICT (user_id) DO NOTHING
            """, (user_id,))
    conn.close()

def remove_news_subscription(user_id):
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                DELETE FROM news_subscriptions WHERE user_id = %s
            """, (user_id,))
    conn.close()

def get_news_subscriptions():
    conn = get_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT user_id FROM news_subscriptions
            """)
            result = curs.fetchall()
    conn.close()
    return result
