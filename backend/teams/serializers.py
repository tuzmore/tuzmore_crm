from rest_framework import serializers
from .models import Team, Assignment
from users.serializers import UserSerializer
from contacts.serializers import ContactSerializer

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'members', 'created_at']

class AssignmentSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    assigned_to_user = UserSerializer(read_only=True)
    assigned_to_team = TeamSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = '__all__'