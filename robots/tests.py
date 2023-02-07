from django.test import TestCase
from django.contrib.auth.models import User

from .models import Robot


class RobotTests(TestCase):

    @classmethod
    def setUpTestData(cls):
    	# Создание тестового пользователя.
        first_testuser = User.objects.create_user(
        	username='Karomaddin', password='Ac985164'
        )
        first_testuser.save()
    	# Создание тестового робота.
        test_robot = Robot.objects.create(
        	serial='78451', model='R2', 
        	version='D2', created='2023-01-07 20:10:01+00:00'
        )
        test_robot.save()

    def test_user(self):
    	user = User.objects.get(id=1)
    	username = f'{user.username}'
    	password = f'{user.password}'
    	email = f'{user.email}'

    	self.assertEqual(username, 'Karomaddin')
    	self.assertNotEqual(password, '12345678')
    	self.assertEqual(email, '')

    def test_robot(self):
        robot = Robot.objects.get(id=1)
        serial = f'{robot.serial}'
        model = f'{robot.model}'
        version = f'{robot.version}'
        created = f'{robot.created}'

        self.assertEqual(serial, '78451')
        self.assertEqual(model, 'R2')
        self.assertEqual(version, 'D2')
        self.assertEqual(created, '2023-01-07 20:10:01+00:00')
