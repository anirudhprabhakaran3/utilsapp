from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm
from django.contrib import messages


def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created.")
            return redirect("login")

    args = {
        "form": form
    }

    return render(request, "registration/register.html", args)
