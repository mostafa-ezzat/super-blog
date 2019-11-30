import unittest
import json
from app.test.base import BaseTestCase
from app.main.util.dry_util import randomString


email = ''
username = ''


def register_user(self):
    global email, username
    email = f"{randomString(8)}@mail.com"
    username = randomString(8)
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email=email,
            username=username,
            password=username
        )),
        content_type='application/json'
    )


def login_user(self):
    print(f"Email {email} - Username {username}")
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=username
        )),
        content_type='application/json'
    )


class TestPostBlueprint(BaseTestCase):

    def test_create_post(self):
        with self.client:
            # user registration
            user_response = register_user(self)
            response_data = json.loads(user_response.data.decode())
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(user_response.status_code, 201)

            # registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['Authorization'])
            self.assertEqual(login_response.status_code, 200)
            post_response = self.client.post(
                '/post/',
                headers=dict(
                    Authorization=data['Authorization']
                ),
                data=json.dumps(dict(
                    title=randomString(50),
                    body=randomString(150),
                    category=['python', 'css', 'html', 'javascript'],
                    author=0
                )),
                content_type='application/json')
            post_data = json.loads(post_response.data.decode())
            self.assertEqual(post_response.status_code, 200)

    def test_user_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            user_response = register_user(self)
            response_data = json.loads(user_response.data.decode())
            print(response_data['Authorization'])
            self.assertTrue(response_data['Authorization'])
            self.assertEqual(user_response.status_code, 201)

            # registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['Authorization'])
            self.assertEqual(login_response.status_code, 200)

            # valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        login_response.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
