from faker import Faker
from locust import HttpUser, task

fake = Faker()


class UserAccess(HttpUser):
    @task
    def create_new_user(self):
        user = {
            'username': f'{fake.user_name()}',
            'email': f'{fake.email()}',
            'password': f'{fake.coordinate()}',
        }

        self.client.post(
            '/users/',
            json={
                'username': user['username'],
                'email': user['email'],
                'password': user['password'],
            },
        )
        
        self.client.post(
            '/auth/token',
            data={
                'username': user['email'],
                'password': user['password']
            }
        )

