from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from work_logger.models import Planner, Retrospect
from work_logger.forms import PlannerForm, RetrospectForm

# Create your views here.
@login_required
def home(request):
    planners = Planner.objects.all().order_by("-date")[:5]
    retrospects = Retrospect.objects.all().order_by("-date")[0:5]

    args = {
        "planners": planners,
        "retrospects": retrospects
    }

    return render(request, "work_logger/home.html", args)

@login_required
def list_planners(request):
    planners = Planner.objects.all().order_by("-date")
    args = {
        "planners": planners
    }

    return render(request, "work_logger/list_planners.html", args)

@login_required
def list_retrospects(request):
    retrospects = Retrospect.objects.all().order_by("-date")
    args = {
        "retrospects": retrospects
    }

    return render(request, "work_logger/list_retrospects.html", args)

@login_required
def add_planner(request):
    form = PlannerForm()
    today = timezone.now()

    today_planner = Planner.objects.filter(date=today)
    if today_planner:
        messages.error(request, f"A planner has already been made for today - {today.date()}")
        return redirect("work_logger_home")


    if request.method == "POST":
        form = PlannerForm(request.POST)
        if form.is_valid():
            planner = form.save(commit=False)
            planner.user = request.user
            planner.date = today
            planner.save()
            messages.success(request, f"Added planner for {today.date()}")
            return redirect("work_logger_home")
        
    args = {
        "form": form,
        "form_type": "Planner",
        "today": today.date()
    }

    return render(request, "work_logger/form.html", args)

@login_required
def add_retrospect(request):
    form = RetrospectForm()
    today = timezone.now()

    today_retrospect = Retrospect.objects.filter(date=today)
    if today_retrospect:
        messages.error(request, f"A retrospect has already been made for today - {today.date()}")
        return redirect("work_logger_home")


    if request.method == "POST":
        form = RetrospectForm(request.POST)
        if form.is_valid():
            retrospect = form.save(commit=False)
            retrospect.user = request.user
            retrospect.date = today
            retrospect.save()
            messages.success(request, f"Added retrospect for {today.date()}")
            return redirect("work_logger_home")
        
    args = {
        "form": form,
        "form_type": "Retrospect",
        "today": today.date()
    }

    return render(request, "work_logger/form.html", args)