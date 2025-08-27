from django.shortcuts import render
from rest_framework import viewsets
from .models import Team, Assignment
from .serializers import TeamSerializer, AssignmentSerializer
from .permissions import IsAdminOrManager
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
