from django.shortcuts import render
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAdmin, IsManager, IsSales
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

@api_view(['GET'])
@permission_classes([IsManager])
def manager_dashboard(request):
    return Response({"message": "Welcome Manager! you can view reports here."})

@api_view(['GET'])
@permission_classes([IsSales])
def sales_dashboard(request):
    return Response({"message": "Welcome Sales! you can view your leads here."})