from rest_framework import permissions


class IsSuperUserOnly(permissions.BasePermission):
	'''
	Этот класс разрешения будет запрещать разрешение 
	любому пользователю кроме суперпользователя.
	'''
	def has_permission(self, request, view):
		if request.user.is_superuser:
			return True
		return False
