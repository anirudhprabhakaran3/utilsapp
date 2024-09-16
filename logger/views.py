from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from logger.forms import CreateWorkItemForm, WorkItemPreferencesForm
from logger.models import WorkItem, WorkItemPreferences, STATUS_CHOICES, TIME_CHOICES
from django.utils import timezone
from datetime import timedelta


# Create your views here.
@login_required
def home(request):
    preferences = WorkItemPreferences.objects.get(user=request.user)
    preferences_form = WorkItemPreferencesForm(instance=preferences)

    last_time = timezone.now().date() - timedelta(days=preferences.time_amount)
    if preferences.time_unit == "W":
        last_time = timezone.now().date() - timedelta(weeks=preferences.time_amount)
    elif preferences.time_unit == "M":
        last_time = timezone.now().date() - timedelta(weeks=preferences.time_amount * 4)

    in_progress = WorkItem.objects.filter(status="IP", user=request.user, updated_at__gt=last_time).order_by(
        "-updated_at")
    done = WorkItem.objects.filter(status="DO", user=request.user, updated_at__gt=last_time).order_by("-updated_at")
    wont_do = WorkItem.objects.filter(status="WD", user=request.user, updated_at__gt=last_time).order_by("-updated_at")
    blocked = WorkItem.objects.filter(status="BL", user=request.user, updated_at__gt=last_time).order_by("-updated_at")

    args = {
        "in_progress": in_progress,
        "done": done,
        "wont_do": wont_do,
        "blocked": blocked,
        "form": preferences_form
    }

    return render(request, "logger/home.html", args)


@login_required
def update_preferences(request):
    preferences = WorkItemPreferences.objects.get(user=request.user)
    form = WorkItemPreferencesForm(instance=preferences)

    if request.method == "POST":
        form = WorkItemPreferencesForm(instance=preferences, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Preferences updated successfully")
            return redirect("logger_home")

    return redirect("logger_home")


@login_required
def create_work_item(request):
    form = CreateWorkItemForm()

    if request.method == "POST":
        form = CreateWorkItemForm(request.POST)
        if form.is_valid():
            work_item = form.save(commit=False)
            work_item.user = request.user
            work_item.updated_at = timezone.now().date()
            work_item.save()
            messages.success(request, "Work item has been created.")
            return redirect("logger_home")

    args = {
        "form": form
    }

    return render(request, "logger/create_work_item.html", args)


@login_required
def view_item(request, item_id):
    item = get_object_or_404(WorkItem, pk=item_id)

    if item.user != request.user:
        messages.error(request, "You are not allowed to view this item.")
        return redirect("logger_home")

    args = {"item": item}

    return render(request, "logger/view_item.html", args)


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(WorkItem, pk=item_id)

    if item.user != request.user:
        messages.error(request, "You are not allowed to edit this item.")
        return redirect("logger_home")

    form = CreateWorkItemForm(instance=item)
    if request.method == "POST":
        form = CreateWorkItemForm(request.POST, instance=item)
        if form.is_valid():
            work_item = form.save(commit=False)
            work_item.updated_at = timezone.now().date()
            work_item.save()
            messages.success(request, "Work item has been updated.")
            return redirect("logger_home")

    args = {"form": form, "item": item}

    return render(request, "logger/edit_work_item.html", args)


@login_required
def view_all_status(request, status):
    flag = True
    for s in STATUS_CHOICES:
        if status == s[0]:
            flag = False
            break

    if flag:
        messages.error(request, "Not a valid status.")
        return redirect("logger_home")

    items = WorkItem.objects.filter(status=status, user=request.user).order_by("-updated_at")

    for s in STATUS_CHOICES:
        if s[0] == status:
            status = s[1]

    args = {
        "items": items,
        "status": status
    }

    return render(request, "logger/view_all.html", args)
