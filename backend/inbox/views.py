from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from .permissions import MessagePermission

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, MessagePermission]

    def perform_create(self, serializer):
        # Automatically assign sender
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, "role", None)

        if role in ["admin", "manager"]:
            return Message.objects.all()

        if role == "sales":
            return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)

        return Message.objects.none()