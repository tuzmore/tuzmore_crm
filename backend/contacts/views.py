from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import Contact
from .serializers import ContactSerializer
# Create your views here.

class ContactCreateAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactListAPIView(generics.ListAPIView):
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backend = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'subject', 'message']

class ContactRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]

class ContactUpdateAPIView(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]

class ContactDeleteAPIView(generics.DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]
