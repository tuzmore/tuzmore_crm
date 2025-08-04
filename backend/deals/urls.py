from django.urls import path, include
from .views import DealViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', DealViewSet, basename='deal')

urlpatterns = [
    path('', include(router.urls)),
]