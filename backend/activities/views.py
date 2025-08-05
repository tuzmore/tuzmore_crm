from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import ActivitySerializer
from .models import Activity
# Create your views here.

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return
        Activity.objects.filter(user=self.request.user).order_by('-timestamp')

        def perform_create(self, serializer):
            serializer.save(user=self.request.user)
