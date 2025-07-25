from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'company', 'password', 'password2']

        def validate(self, data):
            if data['password'] != data['password2']:
                raise ValidationError('Passwors do not match!')
            return data
        
        def create(self, validated_data):
            validated_data.pop('password2')
            user = User.objects.create_user(**validated_data)
            return user

