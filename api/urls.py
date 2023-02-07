from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import RobotViewSet, UserViewSet, LastWeekRobotsApiView, get_last_week_robots_report


router = SimpleRouter()
router.register('users', UserViewSet, basename='users') # Список пользователей 
router.register('', RobotViewSet, basename='robots') # Список роботов

urlpatterns = [
	# Cводка по суммарным показателям производства роботов за последнюю неделю (API EndPoint).
	path('get-last-week-robots/', LastWeekRobotsApiView.as_view()),
	
	# Cводка по суммарным показателям производства роботов за последнюю неделю (Excel файл).
	path('get-last-week-robots-report/', get_last_week_robots_report, name='get-last-week-robots-report')
] + router.urls
