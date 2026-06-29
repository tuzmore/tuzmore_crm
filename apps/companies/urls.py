from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet

from .views import (
    company_list,
    company_create,
    company_detail,
    company_update, 
    company_delete
)



urlpatterns = [
    path("", company_list, name="company_list"),
    path("create/", company_create, name="company_create"),
    path("<int:pk>/", company_detail, name="company_detail"),
    path("<int:pk>/edit/", company_update, name="company_update"),
    path("<int:pk>/delete/", company_delete, name="company_delete"),
]

router = DefaultRouter()
router.register(
    "api", 
    CompanyViewSet,
    basename="company"
)
urlpatterns += router.urls