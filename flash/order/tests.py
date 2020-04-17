import logging

from django.test import TestCase

# noinspection PyProtectedMember
from flash._auth.models import MyUser
from flash.order.models import Order
from flash.organization.models import Organization, Filial
from flash.product.models import Category, Product


class OrdersTest(TestCase):

    DEFAULT_PASSWORD = 'qwe'

    def setUp(self):
        # logging.disable(logging.CRITICAL)

        self._client = {
            "username": "mebr0",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 3
        }

        self.client.post('/auth/register/', self._client, content_type="application/json")
        self.client.login(username=self._client['username'], password=self._client['password'])

        courier_json = {
            'username': 'cour',
            'first_name': 'qwe',
            'last_name': 'qwe',
            'phone_number': '12312312312',
            'role': 4
        }

        self.courier = MyUser.save_user(courier_json, self.DEFAULT_PASSWORD)

        manager_json = {
            'username': 'man',
            'first_name': 'qwe',
            'last_name': 'qwe',
            'phone_number': '12312312312',
            'role': 2
        }

        self.manager = MyUser.save_user(manager_json, self.DEFAULT_PASSWORD)
        self.organization = Organization.objects.create(name='Flash', description='Sth sth', logo='bla bla',
                                                        manager=self.manager)
        self.filial = Filial.objects.create(address='Radostovets 152', organization=self.organization)

        self.category = Category.objects.create(name='Fast food')
        self.product = Product.objects.create(name='Burger', description='Very very delicious', logo='bla bla',
                                              price=100, organization=self.organization, category=self.category)

        self.count = 2
        self.order_json = {
            'address': 'Radostovets st., 34',
            'filial': self.filial.id,
            'products': [
                {
                    'product': self.product.id,
                    'count': self.count
                }
            ]
        }

        self.client.post('/order/', self.order_json, content_type='application/json')

    def test_order_list(self):
        response = self.client.get('/order/')

        self.assertEqual(response.status_code, 200)

        order_list = response.data

        self.assertIsNotNone(order_list)
        self.assertEqual(len(order_list), 1)

        order = order_list[0]

        self.assertEqual(order.get('id'), 1)
        self.assertEqual(order.get('filial'), self.filial.id)
        self.assertEqual(order.get('address'), self.order_json.get('address'))
        self.assertEqual(order.get('client').get('username'), self._client.get('username'))
        self.assertEqual(float(order.get('price')), self.product.price * self.count)
        self.assertEqual(order.get('delivered'), False)
        self.assertEqual(order.get('courier').get('username'), self.courier.username)

        self.assertIsNotNone(order.get('products'))
        self.assertEqual(len(order.get('products')), 1)
        self.assertIsNotNone(order.get('products')[0].get('product'))
        self.assertEqual(order.get('products')[0].get('product'), self.product.id)
        self.assertIsNotNone(order.get('products')[0].get('count'))
        self.assertEqual(order.get('products')[0].get('count'), self.count)

    def test_unauthorized_order_list(self):
        self.client.logout()

        response = self.client.get('/order/')

        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_order_create(self):
        self.client.login(username=self._client['username'], password=self._client['password'])

        # self.assertTrue(self.client.login(username=self._client.username, password=self.DEFAULT_PASSWORD))

        count = 2
        order_json = {
            'address': 'Radostovets st., 34',
            'filial': self.filial.id,
            'products': [
                {
                    'product': self.product.id,
                    'count': count
                }
            ]
        }

        response = self.client.post('/order/', order_json, content_type='application/json')

        self.assertEqual(response.status_code, 201)

        data = response.data

        self.assertIsNotNone(data.get('id'))
        self.assertEqual(data.get('filial'), self.filial.id)
        self.assertEqual(data.get('address'), order_json.get('address'))
        self.assertEqual(data.get('client').get('username'), self._client.get('username'))
        self.assertEqual(float(data.get('price')), self.product.price * count)
        self.assertEqual(data.get('delivered'), False)
        self.assertEqual(data.get('courier').get('username'), self.courier.username)

        self.assertIsNotNone(data.get('products'))
        self.assertEqual(len(data.get('products')), 1)
        self.assertIsNotNone(data.get('products')[0].get('product'))
        self.assertEqual(data.get('products')[0].get('product'), self.product.id)
        self.assertIsNotNone(data.get('products')[0].get('count'))
        self.assertEqual(data.get('products')[0].get('count'), count)

    def test_courier_order_create(self):
        self.assertTrue(self.client.login(username=self.courier.username, password=self.DEFAULT_PASSWORD))

        count = 2
        order_json = {
            'address': 'Radostovets st., 34',
            'filial': self.filial.id,
            'products': [
                {
                    'product': self.product.id,
                    'count': count
                }
            ]
        }

        response = self.client.post('/order/', order_json, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data.get('detail', 'You do not have permission to perform this action.'))

    def test_order_retriever(self):
        _id = 1
        response = self.client.get(f'/order/{_id}/')

        self.assertEqual(response.status_code, 200)

        order = response.data

        self.assertIsNotNone(order)
        self.assertEqual(order.get('id'), 1)
        self.assertEqual(order.get('filial'), self.filial.id)
        self.assertEqual(order.get('address'), self.order_json.get('address'))
        self.assertEqual(order.get('client').get('username'), self._client.get('username'))
        self.assertEqual(float(order.get('price')), self.product.price * self.count)
        self.assertEqual(order.get('delivered'), False)
        self.assertEqual(order.get('courier').get('username'), self.courier.username)

        self.assertIsNotNone(order.get('products'))
        self.assertEqual(len(order.get('products')), 1)
        self.assertIsNotNone(order.get('products')[0].get('product'))
        self.assertEqual(order.get('products')[0].get('product'), self.product.id)
        self.assertIsNotNone(order.get('products')[0].get('count'))
        self.assertEqual(order.get('products')[0].get('count'), self.count)

    def test_order_update(self):
        self.assertTrue(self.client.login(username=self.manager.username, password=self.DEFAULT_PASSWORD))

        _id = 1
        order_json = {
            "address": "Radostovets st., 35",
            "filial": self.filial.id,
            "client": 1
        }
        response = self.client.put(f'/order/{_id}/', order_json, content_type='application/json')

        self.assertEqual(response.status_code, 200)

        order = response.data

        self.assertIsNotNone(order)
        self.assertEqual(order.get('id'), 1)
        self.assertEqual(order.get('filial'), self.filial.id)
        self.assertEqual(order.get('address'), order_json.get('address'))
        self.assertEqual(order.get('client').get('username'), self._client.get('username'))

    def test_client_order_update(self):
        self.client.login(username=self._client['username'], password=self._client['password'])

        # self.assertTrue(self.client.login(username=self._client.username, password=self.DEFAULT_PASSWORD))

        _id = 1
        order_json = {
            "address": "Radostovets st., 35",
            "filial": self.filial.id,
            "client": 1
        }
        response = self.client.put(f'/order/{_id}/', order_json, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data.get('detail', 'You do not have permission to perform this action.'))

    def test_order_delete(self):
        # self.client.login(username=self._client['username'], password=self._client['password'])

        self.assertTrue(self.client.login(username=self.manager.username, password=self.DEFAULT_PASSWORD))

        _id = 1
        response = self.client.delete(f'/order/{_id}/')

        self.assertEqual(response.status_code, 204)

    def test_courier_order_delete(self):
        self.assertTrue(self.client.login(username=self.courier.username, password=self.DEFAULT_PASSWORD))

        _id = 1
        response = self.client.delete(f'/order/{_id}/')

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data.get('detail', 'You do not have permission to perform this action.'))


class ProductsTest(TestCase):

    def setUp(self):
        # logging.disable(logging.CRITICAL)

        self._client = {
            "username": "mebr0",
            "password": "qwe",
            "first_name": "asd",
            "last_name": "qwe",
            "phone_number": "87475620211",
            "role": 3
        }

        self.client.post('/auth/register/', self._client, content_type="application/json")
        self.client.login(username=self._client['username'], password=self._client['password'])

        courier_json = {
            'username': 'cour',
            'first_name': 'qwe',
            'last_name': 'qwe',
            'phone_number': '12312312312',
            'role': 4
        }

        self.courier = MyUser.save_user(courier_json, 'qwer')

        manager_json = {
            'username': 'man',
            'first_name': 'qwe',
            'last_name': 'qwe',
            'phone_number': '12312312312',
            'role': 2
        }

        self.manager = MyUser.save_user(manager_json, 'qwe')
        self.organization = Organization.objects.create(name='Flash', description='Sth sth', logo='bla bla',
                                                        manager=self.manager)
        self.filial = Filial.objects.create(address='Radostovets 152', organization=self.organization)

        self.category = Category.objects.create(name='Fast food')
        self.product = Product.objects.create(name='Burger', description='Very very delicious', logo='bla bla',
                                              price=100, organization=self.organization, category=self.category)

        self.count = 2
        self.order_json = {
            'address': 'Radostovets st., 34',
            'filial': self.filial.id,
            'products': [
                {
                    'product': self.product.id,
                    'count': self.count
                }
            ]
        }

        self.client.post('/order/', self.order_json, content_type='application/json')

    def test_product_list(self):
        _id = 1
        _product_id = 1
        response = self.client.get(f'/order/{_id}/product/')

        self.assertEqual(response.status_code, 200)

        product_list = response.data

        self.assertIsNotNone(product_list)
        self.assertEqual(len(product_list), 1)

        product = product_list[0]

        self.assertEqual(product.get('id'), 1)
        self.assertEqual(product.get('product'), self.product.id)
        self.assertEqual(product.get('count'), self.count)

    def test_product_create(self):
        self.assertTrue(self.client.login(username=self.manager.username, password='qwe'))

        _id = 1
        count = 5

        product_json = {
            "product": self.product.id,
            "count": count
        }

        init_price = Order.objects.get(id=1).price

        response = self.client.post(f'/order/{_id}/product/', product_json, content_type='application/json')

        self.assertEqual(response.status_code, 201)

        product = response.data

        self.assertEqual(product.get('id'), 2)
        self.assertEqual(product.get('product'), self.product.id)
        self.assertEqual(product.get('count'), count)

        final_price = Order.objects.get(id=1).price

        self.assertEqual(init_price + self.product.price * count, final_price)

    def test_client_create(self):
        self.assertTrue(self.client.login(username=self._client.get('username'), password=self._client.get('password')))

        _id = 1
        count = 5

        product_json = {
            "product": self.product.id,
            "count": count
        }

        response = self.client.post(f'/order/{_id}/product/', product_json, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data.get('detail', 'You do not have permission to perform this action.'))

    def test_product_retrieve(self):
        _id = 1
        _product_id = 1
        response = self.client.get(f'/order/{_id}/product/{_product_id}/')

        self.assertEqual(response.status_code, 200)

        product = response.data

        self.assertEqual(product.get('id'), 1)
        self.assertEqual(product.get('product'), self.product.id)
        self.assertEqual(product.get('count'), self.count)

    def test_unauthorized_product_retrieve(self):
        self.client.logout()

        _id = 1
        _product_id = 1
        response = self.client.get(f'/order/{_id}/product/{_product_id}/')

        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.data.get('detail'), 'Authentication credentials were not provided.')

    def test_product_update(self):
        self.assertTrue(self.client.login(username=self.manager.username, password='qwe'))

        _id = 1
        _product_id = 1
        count = 6

        product_json = {
            "product": self.product.id,
            "count": count
        }

        init_price = Order.objects.get(id=_product_id).price

        response = self.client.put(f'/order/{_id}/product/{_product_id}/', product_json,
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

        product = response.data
        self.assertTrue(self.client.login(username=self._client.get('username'), password=self._client.get('password')))

        self.assertEqual(product.get('id'), 1)
        self.assertEqual(product.get('product'), self.product.id)
        self.assertEqual(product.get('count'), count)

        final_price = Order.objects.get(id=_product_id).price

        self.assertEqual(init_price + self.product.price * (count - self.count), final_price)

    def test_courier_product_update(self):
        self.assertTrue(self.client.login(username=self.courier.username, password='qwer'))

        _id = 1
        _product_id = 1
        count = 6

        product_json = {
            "product": self.product.id,
            "count": count
        }

        response = self.client.put(f'/order/{_id}/product/{_product_id}/', product_json,
                                   content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data.get('detail', 'You do not have permission to perform this action.'))

    def test_product_delete(self):
        self.assertTrue(self.client.login(username=self.manager.username, password='qwe'))

        _id = 1
        _product_id = 1

        init_price = Order.objects.get(id=_product_id).price

        response = self.client.delete(f'/order/{_id}/product/{_product_id}/')

        self.assertEqual(response.status_code, 204)

        final_price = Order.objects.get(id=_product_id).price

        self.assertEqual(init_price - self.product.price * self.count, final_price)

    def test_client_product_delete(self):
        self.assertTrue(self.client.login(username=self._client.get('username'), password=self._client.get('password')))

        _id = 1
        _product_id = 1

        response = self.client.delete(f'/order/{_id}/product/{_product_id}/')

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data.get('detail', 'You do not have permission to perform this action.'))

