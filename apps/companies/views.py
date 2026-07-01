from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets

from .models import Company
from .forms import CompanyForm
from .serializers import CompanySerializer
from django.http import HttpResponse


# Create your views here.

@login_required
def company_list(request):

    search = request.GET.get("search", "")
    companies = Company.objects.filter(
        owner=request.user
    )

    if search:
        companies = companies.filter(
            Q(name__icontains=search)|
            Q(email__icontains=search)|
            Q(industry__icontains=search)
        )

    paginator = Paginator(
            companies,
            10
        )

    page_number = request.GET.get(
            "page"
        )

    page_obj = paginator.get_page(
            page_number
        )

    return render(
        request,
        "companies/company_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )



@login_required
def company_create(request):

    if request.method == "POST":
        form = CompanyForm(request.POST)
        

        if form.is_valid():
            company = form.save(
                commit=False
            )

            company.owner = request.user
            company.save()
            return redirect(
                "company_list"
            )
    else:
            
            form = CompanyForm()
    return render(
                request,
                "companies/company_form.html",
                {"form": form}
            )
        

@login_required
def company_detail(request, pk):
    company = get_object_or_404(
        Company, pk=pk,
        owner=request.user
    )

    return render(
        request,
        "companies/company_detail.html",
        {"company": company}
    )

@login_required
def company_update(request, pk):

    company = get_object_or_404(
        Company, pk=pk,
        owner=request.user
    )

    if request.method == "POST":

        form = CompanyForm(
            request.POST,
            instance=company
        )

        if form.is_valid():
            form.save()
            return redirect(
                "company_list"
            )
    else:
            form = CompanyForm(
                instance=company
            )
    return render(
                request,
                "companies/company_form.html",
                {"form": form}
            )
        

@login_required
def company_delete(request, pk):
    
    company = get_object_or_404(
        Company, pk=pk,
        owner=request.user
    )

    if request.method == "POST":
        company.delete()
        return redirect(
            "company_list"
        )
    return render(
        request,
        "companies/company_delete.html",
        {"company": company}
    )

class CompanyViewSet(
    viewsets.ModelViewSet
):
    serializer_class = CompanySerializer
    def get_queryset(self):
        return Company.objects.filter(
            owner=self.request.user
        )
    
    def perform_create(
            self,
            serializer
    ):
        serializer.save(
            owner=self.request.user
        )

