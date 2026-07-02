from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets

from .models import Deal
from .forms import DealForm
from .serializers import DealSerializer

# Create your views here.

@login_required
def deal_list(request):
    search = request.GET.get("search", "")

    deals = Deal.objects.filter(owner=request.user)

    if search:
        deals = deals.filter(
            Q(title__icontains=search) |
            Q(stage__icontains=search)
        )

    paginator = Paginator(deals, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "deals/deal_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )

@login_required
def deal_create(request):
    if request.method == "POST":
        form = DealForm(request.POST)

        if form.is_valid():
            deal = form.save(commit=False)
            deal.owner = request.user
            deal.save()

            return redirect("deal_list")
    else:
        form = DealForm()
    return render(
        request,
        "deals/deal_form.html",
        {"form": form}
    )

@login_required
def deal_detail(request, pk):
    deal = get_object_or_404(
        Deal, pk=pk, owner=request.user
    )
    return render(
        request,
        "deals/deal_detail.html",
        {"deal": deal}
    )

@login_required
def deal_update(request, pk):
    deal = get_object_or_404(
        Deal, pk=pk,
        owner=request.user
    )

    if request.method == "POST":
        form = DealForm(
            request.POST,
            instance=deal
        )

        if form.is_valid():
            form.save()
            return redirect("deal_list")
        
    else:
        form = DealForm(instance=deal)
    return render(
        request,
        "deals/deal_form.html",
        {"form": form}
    )

@login_required
def deal_delete(request, pk):
    deal = get_object_or_404(
        Deal, pk=pk,
        owner=request.user
    )

    if request.method == "POST":
        deal.delete()
        return redirect("deal_list")
    return render(
        request,
        "deals/deal_delete.html",
        {"deal": deal}
    )

class DealViewSet(viewsets.ModelViewSet):
    serializer_class = DealSerializer

    def get_queryset(self):
        return Deal.objects.filter(
            owner=self.request.user
        )
    
    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )
