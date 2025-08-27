from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now, timedelta

from contacts.models import Contact
from deals.models import Deal
from tasks.models import Task
from users.models import User


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """
    Dashboard API
    Returns summary statistics, recent items, and role-based data
    """

    user = request.user
    role = user.role  # assuming we added role in custom AbstractUser

    # Base queryset filters based on role
    contact_qs = Contact.objects.all()
    deal_qs = Deal.objects.all()
    task_qs = Task.objects.all()

    if role == "sales":
        contact_qs = contact_qs.filter(owner=user)
        deal_qs = deal_qs.filter(owner=user)
        task_qs = task_qs.filter(assigned_to=user)
        invoice_qs = invoice_qs.filter(owner=user)

    elif role == "manager":
        # Manager can see only their team (simplified for now)
        team_members = User.objects.filter(manager=user)
        contact_qs = contact_qs.filter(owner__in=team_members)
        deal_qs = deal_qs.filter(owner__in=team_members)
        task_qs = task_qs.filter(assigned_to__in=team_members)
        invoice_qs = invoice_qs.filter(owner__in=team_members)

    # Admin sees everything, no filter applied

    # Dashboard Summary
    summary = {
        "contacts": contact_qs.count(),
        "deals": {
            "total": deal_qs.count(),
            "open": deal_qs.filter(status="open").count(),
            "won": deal_qs.filter(status="won").count(),
            "lost": deal_qs.filter(status="lost").count(),
        },
        "tasks_due_today": task_qs.filter(due_date__date=now().date()).count(),
        "invoices": {
            "paid": invoice_qs.filter(status="paid").count(),
            "unpaid": invoice_qs.filter(status="unpaid").count(),
        },
    }

    # Recent items (limit 5 for dashboard preview)
    recent = {
        "recent_contacts": list(contact_qs.order_by("-created_at")[:5].values("id", "name", "email")),
        "recent_deals": list(deal_qs.order_by("-created_at")[:5].values("id", "title", "status", "amount")),
        "recent_tasks": list(task_qs.order_by("-created_at")[:5].values("id", "title", "due_date")),
        "recent_invoices": list(invoice_qs.order_by("-created_at")[:5].values("id", "invoice_no", "status", "amount")),
    }

    return Response({
        "summary": summary,
        "recent": recent,
    })
