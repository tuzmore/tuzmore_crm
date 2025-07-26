from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from.serializers import UserRegistrationSerializer
# Create your views here.

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "User registered successfully. Please log in."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.erros,status=status.HTTP_400_BAD_REQUEST)
