from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from work_logger.models import Planner, Retrospect

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

    return render(request, "work_logger/planners/list.html", args)

@login_required
def list_retrospects(request):
    retrospects = Retrospect.objects.all().order_by("-date")
    args = {
        "retrospects": retrospects
    }

    return render(request, "work_logger/retrospects/list.html", args)