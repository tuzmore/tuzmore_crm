from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["bio", "phone", "company"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Registration serializer.
    - write_only password
    - DO NOT allow clients to set role (prevents privilege escalation).
    """
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        # do NOT include role here
        fields = ["id", "username", "email", "password", "password2"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value.lower()

    def validate(self, data):
        # check password match
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # enforce Django password validators (e.g. min length, common passwords)
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        # remove password2
        validated_data.pop("password2", None)
        password = validated_data.pop("password")

        # Force default role = sales on registration (prevent client from choosing role)
        user = User.objects.create_user(
            password=password,
            role=User.ROLE_SALES,
            **validated_data
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Public user serializer (safe fields).
    Include nested profile read-only.
    """
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "profile"]
        read_only_fields = ["id", "role", "profile"]


class AdminCreateUserSerializer(serializers.ModelSerializer):
    """
    Admin-only serializer for creating users with explicit role.
    Use this in admin dashboard endpoints only.
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.validationError('Email already in use')
        return value

    def validate_role(self, value):
        if value not in dict(User.ROLE_CHOICES).keys():
            raise serializers.ValidationError("Invalid role.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
        username=validated_data('username'),
        password = validated_data.pop("password"),
        email=validated_data('email'),
        role=validated_data.get|('role', User.ROLE_SALES),
        is_active=False,
        is_verified=False
        )
        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_verified:
            raise
        serializers.validationError({'detail': 'Email not verified'})
        # include role if you want for fronted redirect

        data['role'] = user.role
        return data 