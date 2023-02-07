from django.contrib.auth import get_user_model
from rest_framework import serializers
from robots.models import Robot
from orders.models import Order
from customers.models import Customer


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


class OrderSerializer(serializers.ModelSerializer):
	'''
	Сериализатор класса Order.
	'''
	class Meta:
		model = Order
		fields = ('id', 'customer', 'robot_serial')


class CustomerSerializer(serializers.ModelSerializer):
	'''
	Сериализатор класса Customer.
	'''
	class Meta:
		model = Customer
		fields = ('id', 'email')
