from django.shortcuts import render
from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import ProfilePictureSerializer
# Create your views here.

class ProfilePictureUpdateView(generics.UpdateAPIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return
        UserProfile.objects.get(user=self.request.user)
