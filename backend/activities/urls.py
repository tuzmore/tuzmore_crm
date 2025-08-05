from django.urls import path, include
from .views import ActivityViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
]