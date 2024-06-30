from contextlib import contextmanager
from psycopg2 import connect


@contextmanager
def db():
    conn = connect(
        dbname='task_manager',
        user='admin',
        password='admin',
        host='localhost',
    )
    try:
        yield conn
    finally:
        conn.close()


def populate_db():
    with open('init.sql', 'r') as f:
        sql = f.read()
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()


if __name__ == '__main__':
    populate_db()
