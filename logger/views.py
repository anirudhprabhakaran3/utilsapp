from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.utils import timezone

from logger.models import Log, Task
from logger.forms import LogForm, TaskFormsetHelper

today = timezone.now().date()

# Create your views here.
@login_required
def home(request):
    logs = Log.objects.filter(user=request.user).order_by("-date")[:5]
    args = {
        "logs": logs
    }
    return render(request, "logger/home.html", args)

@login_required
def list_logs(request):
    logs = Log.objects.filter(user=request.user).order_by("-date")
    args = {
        "logs": logs
    }

    return render(request, "logger/list_logs.html", args)

@login_required
def new_log(request):
    try:
        log = Log.objects.get(user=request.user, date=today)
        messages.warning(request, "Log has already been made for today.")
        return redirect("logger_view_log", pk=log.pk)
    except Log.DoesNotExist:
        pass

    log_form = LogForm(initial={
        "date": today,
        "user": request.user
    })
    TaskFormSet = modelformset_factory(Task, fields=["task", "completed"])
    task_formset = TaskFormSet()
    helper = TaskFormsetHelper()

    if request.method == "POST":
        log_form = LogForm(request.POST)
        task_formset = TaskFormSet(request.POST)
        if log_form.is_valid() and task_formset.is_valid():
            log = log_form.save(commit=False)
            log.user = request.user
            log.date = today
            log.save()

            tasks = task_formset.save(commit=False)
            for task in tasks:
                task.log = log
                task.save()

            messages.success(request, "Added log")
            return redirect("logger_home")


    args = {
        "log_form": log_form,
        "task_formset": task_formset,
        "today": today,
        "helper": helper,
    }

    return render(request, "logger/new_log.html", args)

@login_required
def view_log(request, pk):
    log = get_object_or_404(Log, pk=pk)

    if log.date == today:
        messages.warning(request, "This is today's log.")
        return redirect("logger_edit_log", pk=log.pk)

    tasks = Task.objects.filter(log=log)

    completed_tasks = tasks.filter(completed=True).count()
    total_tasks = tasks.count()
    if total_tasks == 0:
        progress = 0
    else:
        progress = completed_tasks / float(total_tasks) * 100.0

    args = {
        "log": log,
        "tasks": tasks,
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "progress": progress
    }

    return render(request, "logger/view_log.html", args)

@login_required
def edit_log(request, pk):
    log = get_object_or_404(Log, pk=pk)
    if log.user != request.user:
        messages.error(request, "Access denied.")
        return redirect("logger_home")
    
    if log.date != today:
        messages.info(request, "This is an archived log.")
        return redirect("logger_view_log", pk=log.pk)
    
    tasks = Task.objects.filter(log=log)
    TaskFormset = modelformset_factory(Task, fields=["task", "completed"])
    task_formset = TaskFormset(queryset=tasks)
    helper = TaskFormsetHelper()

    log_form = LogForm(instance=log)

    if request.method == "POST":
        if "tasks" in request.POST:
            task_formset = TaskFormset(request.POST, queryset=tasks)
            if task_formset.is_valid():
                tasks = task_formset.save(commit=False)
                for task in tasks:
                    task.log = log
                    task.save()

                messages.success(request, "Updated tasks.")
                return redirect("logger_edit_log", pk=log.pk)
            
        if "note" in request.POST:
            log_form = LogForm(request.POST, instance=log)
            if log_form.is_valid():
                log_form.save()
                messages.success(request, "Note updated!")
                return redirect("logger_edit_log", pk=log.pk)
            
    completed_tasks = tasks.filter(completed=True).count()
    total_tasks = tasks.count()
    if total_tasks == 0:
        progress = 0
    else:
        progress = completed_tasks / float(total_tasks) * 100.0
    
    args = {
        "log": log,
        "log_form": log_form,
        "task_formset": task_formset,
        "helper": helper,
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "progress": progress
    }

    return render(request, "logger/edit_log.html", args)