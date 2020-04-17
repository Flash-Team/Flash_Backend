import json
import logging

from django.test import TestCase

from flash._auth.models import MyUser


class BaseAuthTest(TestCase):

    DEFAULT_PASSWORD = 'qwe'

    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.json_user = {
            "username": "mebr0",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 1
        }

        self.user = MyUser.save_user(self.json_user, self.DEFAULT_PASSWORD)

    def _login(self, password=None):
        if password:
            self.assertTrue(self.client.login(username=self.user.username, password=password))
        else:
            self.assertTrue(self.client.login(username=self.user.username, password=self.DEFAULT_PASSWORD))


class AuthTest(BaseAuthTest):

    def test_register(self):
        user = {
            "username": "mebr1",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 3
        }

        response = self.client.post("/auth/register/", user, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)

        self.assertEqual(data.get("username"), user["username"])
        self.assertIsNone(data.get("password"))
        self.assertEqual(data.get("first_name"), user["first_name"])
        self.assertEqual(data.get("last_name"), user["last_name"])
        self.assertEqual(data.get("phone_number"), user["phone_number"])
        self.assertEqual(data.get("role"), user["role"])
        self.assertFalse(data.get("is_superuser"))

    def test_already_register(self):
        response = self.client.post("/auth/register/", self.json_user, content_type="application/json")

        self.assertEqual(response.status_code, 400)

        data = json.loads(response.content)

        self.assertEqual(data.get('username')[0], 'User with this username already exists.')

    def test_login(self):
        response = self.client.post('/auth/login/', self.json_user)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get('token'))

    def test_wrong_login(self):
        user = self.json_user
        user['password'] = user['password'] + '1'

        response = self.client.post('/auth/login/', user)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('non_field_errors')[0], 'Unable to log in with provided credentials.')


class ChangePasswordTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self._login()

    def test_change_password(self):
        new_password = self.user.password + '1'
        request = {
            "password": new_password
        }

        response = self.client.put('/auth/password/', request, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'Password changed')

        self._login(new_password)

    def test_unauthorized_change_password(self):
        self.client.logout()

        request = {
            "password": 'qwe'
        }

        response = self.client.put('/auth/password/', request, content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_drop_password(self):
        response = self.client.delete('/auth/password/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'Default password set')

        self._login()

    def test_unauthorized_drop_password(self):
        self.client.logout()

        response = self.client.delete('/auth/password/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')


class UsersTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self._login()

    def test_user_list(self):
        response = self.client.get('/auth/user/')

        self.assertEqual(response.status_code, 200)

        user_list = response.data

        self.assertIsNotNone(user_list)
        self.assertEqual(len(user_list), 1)

        user = user_list[0]

        self.assertEqual(user.get('id'), 1)
        self.assertEqual(user.get('username'), self.user.username)
        self.assertIsNone(user.get("password"))
        self.assertEqual(user.get('first_name'), self.user.first_name)
        self.assertEqual(user.get('last_name'), self.user.last_name)
        self.assertEqual(user.get('phone_number'), self.user.phone_number)
        self.assertEqual(user.get('role'), self.user.role)
        self.assertFalse(user.get("is_superuser"))

    def test_user_create(self):
        response = self.client.post('/auth/user/', {}, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data.get('message'), 'Not allowed create user here')

    def test_user_retrieve(self):
        _id = 1

        response = self.client.get(f'/auth/user/{_id}/')

        self.assertEqual(response.status_code, 200)

        user = response.data

        self.assertEqual(user.get('id'), 1)
        self.assertEqual(user.get('username'), self.user.username)
        self.assertIsNone(user.get("password"))
        self.assertEqual(user.get('first_name'), self.user.first_name)
        self.assertEqual(user.get('last_name'), self.user.last_name)
        self.assertEqual(user.get('phone_number'), self.user.phone_number)
        self.assertEqual(user.get('role'), self.user.role)
        self.assertFalse(user.get("is_superuser"))

    def test_user_update(self):
        user = self.json_user
        _id = 1
        user['first_name'] = user['first_name'] + 'a'

        response = self.client.put(f'/auth/user/{_id}/', user, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        user = response.data

        self.assertEqual(user.get('id'), 1)
        self.assertEqual(user.get('username'), user.get('username'))
        self.assertIsNone(user.get("password"))
        self.assertEqual(user.get('first_name'), user.get('first_name'))
        self.assertEqual(user.get('last_name'), user.get('last_name'))
        self.assertEqual(user.get('phone_number'), user.get('phone_number'))
        self.assertEqual(user.get('role'), user.get('role'))
        self.assertFalse(user.get("is_superuser"))

    def test_user_create_and_delete(self):
        user = {
            "username": "mebr1",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 3
        }

        response = self.client.post('/auth/register/', user, content_type="application/json")

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)
        _id = data.get('id')

        response = self.client.delete(f'/auth/user/{_id}/')

        self.assertEqual(response.status_code, 204)

    def test_forbidden_user_list(self):
        user = {
            "username": "mebr1",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 3
        }

        self.client.post('/auth/register/', user, content_type="application/json")
        self.client.login(username=user['username'], password=user['password'])

        response = self.client.get('/auth/user/')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data.get('detail'), 'You do not have permission to perform this action.')
