from db import db


def select_all_tasks_for_user(id):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM tasks WHERE user_id = %s', (id,))
            tasks = cur.fetchall()

    return tasks


def select_tasks_by_status(status):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM tasks WHERE status_id IN(SELECT id FROM status WHERE name = %s)', (status,))
            tasks = cur.fetchall()

    return tasks


def update_task_status(task_id, status):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s',
                        (status, task_id))
            conn.commit()
            print(f'Task {task_id} updated to {status}')


def select_free_users():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT fullname FROM users WHERE id NOT IN (
                SELECT DISTINCT user_id FROM tasks
            )''')
            users = cur.fetchall()
    return users


def add_task_for_user(user_id, title, description, status):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO tasks (title, description, user_id, status_id)
                VALUES (%s, %s, %s, (SELECT id FROM status WHERE name = 'in progress' LIMIT 1));
            ''', (title, description, user_id))
            conn.commit()
            result = cur.fetchall()

    return result


def select_uncompleted_tasks():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
            SELECT * FROM tasks WHERE status_id NOT IN (SELECT id FROM status WHERE name='completed')
            ''')
            result = cur.fetchall()
            conn.commit()
    return result


def delete_task(id):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM tasks WHERE id = %s', (id,))
            conn.commit()
            print(f'Task {id} deleted')


def select_user_by_email(email):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users WHERE email LIKE %s', (email,))
            user = cur.fetchone()

    return user


def update_user_name(id, name):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('UPDATE users SET fullname = %s WHERE id = %s', (name, id))
            conn.commit()
            print(f'User {id} updated to {name}')


def group_tasks_by_status():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
            SELECT status.name, COUNT(tasks.id) FROM tasks
            JOIN status ON tasks.status_id = status.id
            GROUP BY status.name
            ORDER BY status.name
            ''')
            result = cur.fetchall()
    return result


def select_tasks_by_user_with_domain(domain):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
            SELECT tasks.title, tasks.description FROM tasks
            JOIN users ON tasks.user_id = users.id
            WHERE users.email LIKE %s
            ''', (f'%@{domain}',))
            result = cur.fetchall()
    return result


def select_tasks_without_description():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
            SELECT * FROM tasks WHERE description IS NULL
            ''')
            result = cur.fetchall()
    return result


def select_tasks_and_users_by_status(status):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
            SELECT tasks.title, users.fullname FROM tasks
            INNER JOIN users ON tasks.user_id = users.id
            WHERE tasks.status_id = (SELECT id FROM status WHERE name = %s)
            ''', (status,))
            result = cur.fetchall()
    return result


def tasks_count_per_user():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
            SELECT fullname, COUNT(tasks.id) FROM users
            LEFT JOIN tasks ON users.id = tasks.user_id
            GROUP BY users.fullname
            ORDER BY users.fullname
            ''')
            result = cur.fetchall()
    return result
