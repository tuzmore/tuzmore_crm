from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from deals.models import Deal
from contacts.models import Contact

User = get_user_model()


# ----------------- HTML Pages -----------------

def register_view(request):
    """Render register page"""
    return render(request, "register.html")


def login_view(request):
    """Render login page & handle HTML login POST"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "message": "Account not activated. Check your email."})
        else:
            return JsonResponse({"success": False, "message": "Invalid username or password."})
    return render(request, "login.html")


@login_required(login_url="/login/")
def dashboard_view(request):
    return render(request, "dashboard.html")


def about_view(request):
    return render(request, "about.html")


def solutions_view(request):
    return render(request, "solutions.html")


def contact_us_view(request):
    return render(request, "contact_us.html")


def landing_view(request):
    return render(request, "landing.html")


# ----------------- API Endpoints -----------------

@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    """Register a user via API or HTML form with real email verification"""
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    # Validation
    if not username or not email or not password:
        return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"detail": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({"detail": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

    # Create inactive user
    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_active = False  # require email verification
    user.save()

    # Send activation email
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://127.0.0.1:8000/api/activate/{uid}/{token}/"
        send_mail(
            "Activate your CRM account",
            f"Hi {user.username},\n\nPlease verify your email by clicking the link below:\n{activation_link}\n\nThanks!",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
    except Exception as e:
        print("Email sending failed:", e)
        return Response({"detail": "Registration failed. Could not send verification email."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"detail": "Registration successful! Please check your email to verify your account."},
                    status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    """Activate account via email link"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"detail": "Account activated successfully! You can now log in."})
    return Response({"detail": "Invalid or expired activation link."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    user = request.user
    deals = Deal.objects.filter(owner=user).order_by("-created_at")
    contacts = Contact.objects.filter(owner=user).order_by("-created_at")

    data = {
        "username": user.username,
        "deals": [{"id": d.id, "name": d.name, "status": d.status, "amount": float(d.amount),
                   "created_at": d.created_at.strftime("%Y-%m-%d %H:%M")} for d in deals],
        "contacts": [{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone,
                      "created_at": c.created_at.strftime("%Y-%m-%d %H:%M")} for c in contacts]
    }
    return Response(data)
