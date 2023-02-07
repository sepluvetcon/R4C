from django.contrib.auth import get_user_model
from rest_framework import serializers
from robots.models import Robot


class UserSerializer(serializers.ModelSerializer):
	'''
	Сериализатор класса User.
	'''
	class Meta:
		model = get_user_model()
		fields = ('id', 'username')


class RobotSerializer(serializers.ModelSerializer):
	'''
	Сериализатор класса Robot.
	'''
	class Meta:
		model = Robot
		fields = ('id', 'serial', 'model', 'version', 'created')
