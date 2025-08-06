from django.urls import path
from .views import ProfilePictureUpdateView

urlpatterns = [
    path('profile/upload-picture/', ProfilePictureUpdateView.as_view(), name='upload-profile-picture'),
]