from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from logger.forms import CreateWorkItemForm
from logger.models import WorkItem, STATUS_CHOICES


# Create your views here.
@login_required
def home(request):
    in_progress = WorkItem.objects.filter(status="IP", user=request.user).order_by("-updated_at")[:20]
    done = WorkItem.objects.filter(status="DO", user=request.user).order_by("-updated_at")[:20]
    wont_do = WorkItem.objects.filter(status="WD", user=request.user).order_by("-updated_at")[:20]
    blocked = WorkItem.objects.filter(status="BL", user=request.user).order_by("-updated_at")[:20]

    args = {
        "in_progress": in_progress,
        "done": done,
        "wont_do": wont_do,
        "blocked": blocked,
    }

    return render(request, "logger/home.html", args)


@login_required
def create_work_item(request):
    form = CreateWorkItemForm()

    if request.method == "POST":
        form = CreateWorkItemForm(request.POST)
        if form.is_valid():
            work_item = form.save(commit=False)
            work_item.user = request.user
            work_item.status = "IP"
            work_item.save()
            messages.success(request, "Work item has been created.")
            return redirect("logger_home")

    args = {
        "form": form
    }

    return render(request, "logger/create_work_item.html", args)
