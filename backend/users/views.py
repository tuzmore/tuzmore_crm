# backend/apps/users/views.py
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    AdminCreateUserSerializer,
)
from .permissions import IsAdmin, IsManager, IsSales
from .tokens import account_activation_token

from deals.models import Deal
from contacts.models import Contact

User = get_user_model()


# -------------------------------
# Register with Email Verification
# -------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()  # inactive + unverified

        # Generate email verification link
        current_site = get_current_site(self.request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = f"http://{current_site.domain}{reverse('users:activate', kwargs={'uidb64': uid, 'token': token})}"

        # Send email
        subject = "Verify your Tuzmore account"
        message = render_to_string("activation_email.html", {
            "user": user,
            "activation_link": activation_link,
        })
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.content_subtype = "html"
        email.send(fail_silently=False)


# -------------------------------
# Email Activation View
# -------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        return Response({"detail": "✅ Email verified successfully! You can now log in."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "❌ Invalid or expired activation link."}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# Admin-only user management
# -------------------------------
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AdminCreateUserSerializer
        return UserSerializer


# -------------------------------
# Role-based Dashboards
# -------------------------------
@api_view(["GET"])
@permission_classes([IsManager])
def manager_dashboard(request):
    return Response({"message": "📊 Welcome Manager! You can view reports here."})


@api_view(["GET"])
@permission_classes([IsSales])
def sales_dashboard(request):
    return Response({"message": "📈 Welcome Sales! You can view your leads here."})


# -------------------------------
# User Dashboard API
# -------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    user = request.user

    deals = Deal.objects.filter(owner=user).order_by("-created_at")
    contacts = Contact.objects.filter(owner=user).order_by("-created_at")

    data = {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", None),
        },
        "deals": [
            {
                "id": d.id,
                "name": d.name,
                "status": d.status,
                "amount": float(d.amount),
                "created_at": d.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for d in deals
        ],
        "contacts": [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for c in contacts
        ],
    }
    return Response(data, status=status.HTTP_200_OK)
