from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Deal
from .serializers import DealSerializer
from .permissions import DealPermission
# Create your views here.

class DealViewSet(viewsets.ModelViewSet):
    # Deals CRUD API with role-based permissions.
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated, DealPermission]

    def perform_create(self, serializer):
        # Automatically assign logged-in users as owner if role is sales
        if self.request.user.role == 'sales':
            serializer.save(owner=self.request.user)
        else:
            serializer.save()
