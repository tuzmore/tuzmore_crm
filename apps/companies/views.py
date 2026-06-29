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
    companies = Company.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "companies/company_list.html",
        {
            "companies": companies,
        }
    )



    
        
        
    

@login_required
def company_create(request):
    print("VIEW HIT")

    if request.method == "POST":
        form = CompanyForm(request.POST)
        print("METHOD:", request.method)
        print("FORM:", form)
        

        if form.is_valid():
            print("VALID FORM")
            company = form.save(
                commit=False
            )

            company.owner = request.user
            company.save()
            return redirect(
                "company_list"
            )
    else:
            print("ERROS FORMS")
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

