from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse


User = get_user_model()


# -------------------- HTML Pages --------------------

def register_view(request):
    """
    Render HTML register page.
    Registration is handled via JS fetch to /api/register/.
    """
    return render(request, "register.html")


def login_view(request):
    """
    Render HTML login page and handle HTML POST login requests.
    """
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
    """Render dashboard page for logged-in users"""
    return render(request, "dashboard.html")


def about_view(request):
    return render(request, "about.html")


def solutions_view(request):
    return render(request, "solutions.html")


def contact_us_view(request):
    return render(request, "contact_us.html")


def landing_view(request):
    return render(request, "landing.html")

@login_required
def inbox_view(request):
    return render(request, "inbox.html")  # create inbox.html template


# -------------------- API Endpoints --------------------





