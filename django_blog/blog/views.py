from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "blog/register.html", {"form": form})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, "blog/profile.html")

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, "blog/profile.html")
