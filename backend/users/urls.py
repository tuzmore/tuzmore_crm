from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView,
    AdminUserViewSet,
    manager_dashboard,
    sales_dashboard,
    activate_user,
)

# Router for admin user management
router = DefaultRouter()
router.register(r'admin/users', AdminUserViewSet, basename='admin-users')

app_name = "users" 

urlpatterns = [
    # Auth endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/activate/<uidb64>/<token>/', activate_user, name='activate'),

    # Role-based dashboards
    path("manager-dashboard/", manager_dashboard, name="manager-dashboard"),
    path("sales-dashboard/", sales_dashboard, name="sales-dashboard"),

    # Admin user management
    path("", include(router.urls)),
]
