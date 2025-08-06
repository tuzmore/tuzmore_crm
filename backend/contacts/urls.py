from django.urls import path
from .views import (
    ContactCreateAPIView,
    ContactListAPIView,
    ContactRetrieveAPIView,
    ContactUpdateAPIView,
    ContactDeleteAPIView,
)

urlpatterns = [
    path('create/', ContactCreateAPIView.as_view(), name='contact-create'),
    path('all/', ContactListAPIView.as_view(), name='contact-list'),
    path('<int:pk>/', ContactRetrieveAPIView.as_view(), name='contact-detail'),
    path('update/<int:pk>/', ContactUpdateAPIView.as_view(), name='contact-update'),
    path('delete/<int:pk>/', ContactDeleteAPIView.as_view(), name='contact-delete'),

]