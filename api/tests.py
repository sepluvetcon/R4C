from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import force_authenticate

from robots.models import Robot


class RobotAPIViewTests(APITestCase):
	robots_url = reverse('robots-list')

	def setUp(self):
		# Создание тестового пользователя.
		self.user = User.objects.create_user(
			username='Karomaddin', 
			password='Ac985164', 
			is_staff=True,
		)
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

	def test_get_robots_authenticated(self):
		# Аутентифицированный get запрос на список роботов
		response = self.client.get(self.robots_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_robots_un_authenticated(self):
		# Не аутентифицированный get запрос на список роботов
		self.client.force_authenticate(user=None, token=None)
		response = self.client.get(self.robots_url)
		self.assertEquals(response.status_code, 403)

	def test_post_robots_authenticated(self):
		# Аутентифицированный post запрос для создания робота 
		data = {
			'serial': '78451', 
			'model': 'R2', 
        	'version': 'D2', 
        	'created': '2023-01-07 20:10:01+00:00'
		}
		response = self.client.post(self.robots_url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class RobotDetailAPIViewTests(APITestCase):
	robot_url = reverse('robots-detail', args=[1])
	robots_url = reverse('robots-list')

	def setUp(self):
		# Создание тестового пользователя.
		self.user = User.objects.create_user(
			username='Karomaddin', 
			password='Ac985164', 
			is_staff=True,
		)
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

		# Создание тестового робота.
		data = {
			'serial': '87436', 
			'model': 'R3', 
			'version': 'D4', 
			'created': '2023-02-01 19:11:21+00:00'
		}
		self.client.post(self.robots_url, data, format='json')

	def test_get_robot_autheticated(self):
		# Аутентифицированный get запрос на страницу робота 
		response = self.client.get(self.robot_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['model'], 'R3')

	def test_get_robot_un_authenticated(self):
		# Не аутентифицированный get запрос на страницу робота
		self.client.force_authenticate(user=None, token=None)
		response = self.client.get(self.robot_url)
		self.assertEqual(response.status_code, 403)

	def test_delete_robot_authenticated(self):
		# Аутентифицированный delete запрос на страницу робота
		response = self.client.delete(self.robot_url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
