from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Contact
from .serializers import ContactSerializer
from .permissions import IsAdminOrManager, IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the logged-in user as owner

        serializer.save(owner=self.request.user)

        @swagger_auto_schema(operation_summary='List all contacts')
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
        
        @swagger_auto_schema(operation_summary='Retrieve a single contact by ID')
        def retrieve(self, request, *args, **kwargs):
            return super().retrieve(request, *args, **kwargs)
        
        @swagger_auto_schema(operation_summary='Create a new contact')
        def create(self, request, *args, **kwargs):
            return super().create(request, *args, **kwargs)
        
        @swagger_auto_schema(operation_summary='Update a contact')
        def update(self, request, *args, **kwargs):
            return super().update(request, *args, **kwargs)
        
        @swagger_auto_schema(operation_summary='Delete a contact')
        def destroy(self, request, *args, **kwargs):
            return super().destroy(request, *args, **kwargs)



