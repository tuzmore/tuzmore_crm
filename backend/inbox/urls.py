from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register(r'inbox', MessageViewSet, basename='inbox')

urlpatterns = router.urls