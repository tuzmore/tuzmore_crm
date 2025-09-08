from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet

router = DefaultRouter()
router.register(r'inbox', ContactMessageViewSet, basename='inbox')

urlpatterns  =  router.urls
