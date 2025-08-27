from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'assignments', AssignmentViewSet, basename='assignment')

urlpatterns = router.urls