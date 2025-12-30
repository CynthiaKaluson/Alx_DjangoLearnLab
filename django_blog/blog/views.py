from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get("email")
            user.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "registration/profile.html")
