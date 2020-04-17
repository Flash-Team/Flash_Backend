import json
import logging

from django.test import TestCase


class AuthTest(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.user = {
            "username": "mebr0",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 1
        }

        self.client.post("/auth/register/", self.user, content_type="application/json")

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
        response = self.client.post("/auth/register/", self.user, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data.get('username')[0], 'User with this username already exists.')

    def test_login(self):
        response = self.client.post('/auth/login/', self.user)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get('token'))

    def test_wrong_login(self):
        # change user's password
        user = self.user
        user['password'] = user['password'] + '1'

        response = self.client.post('/auth/login/', user)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('non_field_errors')[0], 'Unable to log in with provided credentials.')


class ChangePasswordTest(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.user = {
            "username": "mebr0",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 1
        }

        self.client.post('/auth/register/', self.user, content_type="application/json")
        self.client.login(username=self.user['username'], password=self.user['password'])

    def test_change_password(self):
        new_password = self.user.get('password') + '1'
        request = {
            "password": new_password
        }

        response = self.client.put('/auth/password/', request, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'Password changed')

        result = self.client.login(username=self.user.get('username'), password=new_password)

        self.assertTrue(result)

    def test_drop_password(self):
        response = self.client.delete('/auth/password/', content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'Default password set')

        result = self.client.login(username=self.user.get('username'), password='qwe')

        self.assertTrue(result)

    def test_unauthorized_change_password(self):
        self.client.logout()

        request = {
            "password": 'qwe'
        }

        response = self.client.put('/auth/password/', request, content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_unauthorized_drop_password(self):
        self.client.logout()

        response = self.client.delete('/auth/password/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Authentication credentials were not provided.')


class UsersTest(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

        self.user = {
            "username": "mebr0",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 1
        }

        self.client.post('/auth/register/', self.user, content_type="application/json")
        self.client.login(username=self.user['username'], password=self.user['password'])

    def test_user_list(self):
        response = self.client.get('/auth/user/')

        self.assertEqual(response.status_code, 200)

        todo_list = response.data

        self.assertIsNotNone(todo_list)
        self.assertEqual(len(todo_list), 1)

        _list = todo_list[0]

        self.assertEqual(_list.get('id'), 1)
        self.assertEqual(_list.get('username'), self.user.get('username'))
        self.assertIsNone(_list.get("password"))
        self.assertEqual(_list.get('first_name'), self.user.get('first_name'))
        self.assertEqual(_list.get('last_name'), self.user.get('last_name'))
        self.assertEqual(_list.get('phone_number'), self.user.get('phone_number'))
        self.assertEqual(_list.get('role'), self.user.get('role'))
        self.assertFalse(_list.get("is_superuser"))

    def test_user_create(self):
        response = self.client.post('/auth/user/', {}, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data.get('message'), 'Not allowed create user here')

    def test_user_retrieve(self):
        _id = 1
        response = self.client.get(f'/auth/user/{_id}/')

        self.assertEqual(response.status_code, 200)

        _list = response.data

        self.assertEqual(_list.get('id'), 1)
        self.assertEqual(_list.get('username'), self.user.get('username'))
        self.assertIsNone(_list.get("password"))
        self.assertEqual(_list.get('first_name'), self.user.get('first_name'))
        self.assertEqual(_list.get('last_name'), self.user.get('last_name'))
        self.assertEqual(_list.get('phone_number'), self.user.get('phone_number'))
        self.assertEqual(_list.get('role'), self.user.get('role'))
        self.assertFalse(_list.get("is_superuser"))

    def test_user_update(self):
        user = self.user
        _id = 1
        user['first_name'] = user['first_name'] + 'a'
        response = self.client.put(f'/auth/user/{_id}/', user, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        _list = response.data

        self.assertEqual(_list.get('id'), 1)
        self.assertEqual(_list.get('username'), user.get('username'))
        self.assertIsNone(_list.get("password"))
        self.assertEqual(_list.get('first_name'), user.get('first_name'))
        self.assertEqual(_list.get('last_name'), user.get('last_name'))
        self.assertEqual(_list.get('phone_number'), user.get('phone_number'))
        self.assertEqual(_list.get('role'), user.get('role'))
        self.assertFalse(_list.get("is_superuser"))

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
