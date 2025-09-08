from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'subject', 'body', 'sender', 
            'recipient', 'sender_username', 'recipient_username', 'read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at', 'sender_username', 'recipient_username']