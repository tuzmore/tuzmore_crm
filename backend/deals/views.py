# crm/deals/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Deal
from .serializers import DealSerializer
from .permissions import DealPermission

class DealViewSet(viewsets.ModelViewSet):
    """
    Deals CRUD API with role-based permissions.
    """
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated, DealPermission]

    def perform_create(self, serializer):
        # Always assign the logged-in user as the owner
        serializer.save(owner=self.request.user)
