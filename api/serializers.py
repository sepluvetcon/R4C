from rest_framework import serializers
from robots.models import Robot


class RobotSerializer(serializers.ModelSerializer):
	'''
	Сериализатор класса Robot.
	'''
	class Meta:
		model = Robot
		fields = ('id', 'serial', 'model', 'version', 'created')
