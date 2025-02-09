from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from config.forms import RegisterForm
from booking.models import Location


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def create_booking(request):
    locations = Location.objects.all()
    return render(request, "create_booking.html", {"locations": locations})

@login_required
def my_bookings(request):
    return render(request, "my_bookings.html")