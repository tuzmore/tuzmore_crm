from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Deal
from .serializers import DealSerializer
# Create your views here.

class DealViewSet(viewsets.ModelViewSet):
    get_queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return
        Deal.objects.filter(owner=self.request.user)

        def perform_create(self, seializer):
            serializer.save(owner=self.request.user)
