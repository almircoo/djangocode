from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from django.contrib import messages


# Create your views here.
@login_required
def profile_view(request):
    return render(request, "oauth/profile.html")


@login_required
def change_profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS, "Success update profile!")
            return redirect("oauth:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "oauth/change_profile.html", context={"form": form})
