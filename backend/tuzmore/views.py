# backend/apps/users/views.py

from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from deals.models import Deal
from contacts.models import Contact

User = get_user_model()


# ----------------- HTML Pages -----------------

def register_view(request):
    return render(request, "register.html")


def about_view(request):
    return render(request, "about.html")

def solutions_view(request):
    return render(request, 'solutions.html')


def login_view(request):
    return render(request, "login.html")

@login_required(login_url="/login/")  # redirect unauthenticated users to login
def dashboard_view(request):
    """
    Render dashboard template only if user is logged in.
    """
    return render(request, "dashboard.html")

def landing_view(request):
    return render(request, "landing.html")


# ----------------- API Endpoints -----------------

@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    """
    Register a user but keep them inactive until they verify via email.
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(username=username).exists():
        return Response({"detail": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"detail": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    # Create inactive user
    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_active = False
    user.save()

    # Generate verification link
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"http://127.0.0.1:8000/api/activate/{uid}/{token}/"  # ⚡ change to your domain

    # Send verification email
    send_mail(
        "Activate your CRM account",
        f"Hi {user.username},\n\nPlease verify your email by clicking the link below:\n{activation_link}\n\nThanks!",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return Response({"detail": "User registered successfully. Please check your email to verify your account."},
                    status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    """
    Activate a user account if the token is valid.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"detail": "Account activated successfully! You can now log in."})
    else:
        return Response({"detail": "Invalid or expired activation link."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    """
    Return only the logged-in user's deals and contacts.
    """
    user = request.user

    deals = Deal.objects.filter(owner=user).order_by("-created_at")
    contacts = Contact.objects.filter(owner=user).order_by("-created_at")

    data = {
        "username": user.username,
        "deals": [
            {
                "id": deal.id,
                "name": deal.name,
                "status": deal.status,
                "amount": float(deal.amount),
                "created_at": deal.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for deal in deals
        ],
        "contacts": [
            {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "created_at": contact.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for contact in contacts
        ]
    }

    return Response(data)
