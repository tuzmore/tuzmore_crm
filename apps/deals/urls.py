from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import(
    deal_list,
    deal_create,
    deal_detail,
    deal_update,
    deal_delete,
    DealViewSet
)

router = DefaultRouter()
router.register(
    "api",
    DealViewSet,
    basename="deal"
)


urlpatterns = [
    path("", deal_list, name="deal_list"),
    path("create/", deal_create, name="deal_create"),
    path("<int:pk>/", deal_detail, name="deal_detail"),
    path("<int:pk>/edit/", deal_update, name="deal_update"),
    path("<int:pk>/delete/", deal_delete, name="deal_delete")
]

urlpatterns += router.urls