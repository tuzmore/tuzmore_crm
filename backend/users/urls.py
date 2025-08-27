from django.urls import path
from .views import RegisterView, UserListView, manager_dashboard, sales_dashboard
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('sales-dashboard/', sales_dashboard, name='sales-dashboard'),
]

