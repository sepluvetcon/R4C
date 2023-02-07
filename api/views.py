from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from robots.models import Robot

from .serializers import RobotSerializer

# Create your views here.
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