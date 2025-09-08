from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from .permissions import IsAdminUserReadOnly

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUserReadOnly]

    def perform_create(self, serializer):
        serializer.save()  # optionally, you can assign received_by here if admin