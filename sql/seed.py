import faker
from db import db

USERS_COUNT = 10
TASKS_COUNT = 100


class Populator:
    def __init__(self):
        self.fake = faker.Faker()
        self.users = []
        self.tasks = []

    def generate_fake_users(self):
        for _ in range(USERS_COUNT):
            self.users.append({
                'fullname': self.fake.name(),
                'email': self.fake.email(),
            })

    @staticmethod
    def get_all_status_ids():
        with db() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM status')
                statuses = cur.fetchall()

        return [status[0] for status in statuses]

    def generate_fake_tasks(self, users_ids, status_ids):
        for _ in range(TASKS_COUNT):
            self.tasks.append({
                'title': self.fake.sentence(),
                'description': self.fake.text(),
                'status_id': self.fake.random_element(elements=status_ids),
                'user_id': self.fake.random_element(elements=users_ids)
            })

    def populate_users(self):
        insert_user = '''INSERT INTO users (fullname, email) VALUES (%s,%s) RETURNING id'''
        prep_users = []
        for user in self.users:
            prep_users.append((user['fullname'], user['email']))

        with db() as conn:
            with conn.cursor() as cur:
                cur.executemany(insert_user, prep_users)
                conn.commit()

            with conn.cursor() as cur:
                cur.execute('SELECT id FROM users')
                ids = cur.fetchall()

        return [id[0] for id in ids]

    def populate_tasks(self):
        insert_task = '''INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s,%s,%s,%s)'''
        prep_tasks = []
        for task in self.tasks:
            prep_tasks.append((task['title'], task['description'], task['status_id'], task['user_id']))

        with db() as conn:
            with conn.cursor() as cur:
                cur.executemany(insert_task, prep_tasks)
                conn.commit()


if __name__ == '__main__':
    populator = Populator()

    populator.generate_fake_users()
    user_ids = populator.populate_users()
    status_ids = populator.get_all_status_ids()
    
    populator.generate_fake_tasks(user_ids, status_ids)
    populator.populate_tasks()

    print('Database populated successfully')
