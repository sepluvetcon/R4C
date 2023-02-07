from rest_framework.routers import SimpleRouter

from .views import RobotViewSet


router = SimpleRouter()
router.register('', RobotViewSet, basename='robots') # Список роботов

urlpatterns = [] + router.urls
