from django.contrib.auth import get_user_model
from django.http import FileResponse
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from robots.models import Robot
from orders.models import Order
from customers.models import Customer

from .serializers import (RobotSerializer, UserSerializer, 
    CustomerSerializer, OrderSerializer)
from .permissions import IsSuperUserOnly
from .utils import get_last_week_robots, get_path_to_excel_file


class RobotViewSet(viewsets.ModelViewSet):
    '''
    ViewSet роботов.
    '''
    permission_classes = [permissions.IsAdminUser]
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer

    def create(self, request, *args, **kwargs):
        # Валидация входных данных.
        valid_data = self.serializer_class(data=request.data)
        if valid_data.is_valid():
            valid_data.save()
            return Response('Робот успешно сохранен в базе данных.')
        return Response('Данные не валидны. Проверьте введенные данные на соответствие условиям.')


class UserViewSet(viewsets.ModelViewSet):
    '''
    ViewSet пользователей.
    '''
    permission_classes = [IsSuperUserOnly]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class OrderViewSet(viewsets.ModelViewSet):
    '''
    ViewSet заказов.
    '''
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    '''
    ViewSet покупателей.
    '''
    permission_classes = [permissions.IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class LastWeekRobotsApiView(generics.ListAPIView):
    '''
    View роботов произведенных за последнюю неделю.
    '''
    permission_classes = [IsSuperUserOnly]
    queryset = get_last_week_robots()
    serializer_class = RobotSerializer


def get_last_week_robots_report(request):
    '''
    Функция получает путь к excel файлу со сводкой роботов 
    произведенных за последнюю неделю от функции get_path_to_excel_file
    и возвращает файл в виде FileResponse.
    '''
    file_location = get_path_to_excel_file()
    if request.user.is_superuser:
        file = open(file_location, 'rb') 
        response = FileResponse(file)
        return response
