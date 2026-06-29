from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_view(request):
    print("DASHBOARD IS WORKING")

    context = {}
    return render(
        request, "dashboard/dashboard.html", 
        context
    )
