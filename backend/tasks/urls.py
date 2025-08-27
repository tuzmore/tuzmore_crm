from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ActivityViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'activities',ActivityViewSet, basename='activity')

urlpatterns = router.urls