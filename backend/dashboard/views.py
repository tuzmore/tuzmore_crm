from django.db.models import Count, Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from deals.models import Deal
from contacts.models import Contact


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """
    Dashboard API
    Returns summary of deals, contacts, and revenue.
    """

    # Total deals
    total_deals = Deal.objects.count()

    # Deals grouped by status
    deals_by_status = Deal.objects.values('status').annotate(
        count=Count('id'),
        total_amount=Sum('amount')
    )

    # Total revenue (sum of won deals)
    total_revenue = Deal.objects.filter(status='won').aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Total contacts
    total_contacts = Contact.objects.count()

    # Recent deals (last 5)
    recent_deals = Deal.objects.select_related('contact', 'owner').order_by('-created_at')[:5]
    recent_deals_data = [
        {
            "id": deal.id,
            "name": deal.name,
            "status": deal.status,
            "amount": float(deal.amount),
            "contact": deal.contact.name if deal.contact else None,
            "owner": deal.owner.username if deal.owner else None,
            "created_at": deal.created_at,
        }
        for deal in recent_deals
    ]

    return Response({
        "total_deals": total_deals,
        "total_contacts": total_contacts,
        "total_revenue": float(total_revenue),
        "deals_by_status": list(deals_by_status),
        "recent_deals": recent_deals_data,
    })
