from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, Activity
from .serializers import TaskSerializer, ActivitySerializer
from users.permissions import IsAdmin, IsManager, IsSales
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager | IsSales )]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'sales':
            return
        Task.objects.filter(assigned_to=user)
        return Task.objects.all()
    

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated & (IsAdmin | IsManager | IsSales)]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'sales':
            return Activity.objects.filter(user=user)
        return Activity.objects.all()