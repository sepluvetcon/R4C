from django.test import TestCase

from .models import Order
from customers.models import Customer


class RobotTests(TestCase):

    @classmethod
    def setUpTestData(cls):
    	# Создание тестового заказчика.
        first_test_customer = Customer.objects.create(email='karomaddin@gmail.com')
        first_test_customer.save()
    	# Создание тестового заказа.
        test_order = Order.objects.create(customer=first_test_customer, robot_serial='75684')
        test_order.save()

    def test_customer(self):
    	customer = Customer.objects.get(id=1)
    	email = f'{customer.email}'

    	self.assertEqual(email, 'karomaddin@gmail.com')
    	self.assertNotEqual(email, 'mike@gmail.com')

    def test_order(self):
        order = Order.objects.get(id=1)
        customer = f'{order.customer}'
        robot_serial = f'{order.robot_serial}'

        self.assertEqual(customer, 'karomaddin@gmail.com')
        self.assertEqual(robot_serial, '75684')

