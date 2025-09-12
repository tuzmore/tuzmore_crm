from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


# ---------------- Profile Serializer ----------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["bio", "phone", "company"]


# ---------------- Register Serializer ----------------
class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles public user registration.
    - Ensures unique email
    - Confirms password
    - Sets role = sales by default
    - Marks account inactive & unverified until email confirmation
    """
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value.lower()

    def validate(self, data):
        # check password match
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # enforce Django password validators (min length, common passwords, etc.)
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password")

        # Force default role = sales and inactive until email verification
        user = User.objects.create_user(
            password=password,
            role=User.ROLE_SALES,
            is_active=False,
            is_verified=False,
            **validated_data
        )
        return user


# ---------------- Public User Serializer ----------------
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "profile"]
        read_only_fields = ["id", "role", "profile"]


# ---------------- Admin Create User Serializer ----------------
class AdminCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_role(self, value):
        if value not in dict(User.ROLE_CHOICES).keys():
            raise serializers.ValidationError("Invalid role.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            password=password,
            is_active=False,
            is_verified=False,
            **validated_data
        )
        return user


# ---------------- Custom JWT Serializer ----------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_verified:
            raise serializers.ValidationError({"detail": "Email not verified. Please check your inbox."})

        # include role for frontend redirect
        data["role"] = user.role
        return data
