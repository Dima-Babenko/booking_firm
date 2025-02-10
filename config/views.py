from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings
from config.forms import RegisterForm
from booking.models import Location, Booking


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
    locations = Location.objects.filter(is_available=True)  # Додаємо фільтр доступності
    return render(request, "create_booking.html", {"locations": locations})


@login_required
def book_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    if request.method == "POST":
        email = request.POST.get("email")
        days = int(request.POST.get("days", 1))

        if not email:
            return render(request, "book_location.html", {"location": location, "error": "Email є обов'язковим."})

        start_time = now()
        end_time = start_time + timedelta(days=days)
        total_price = location.price * days

        booking = Booking.objects.create(
            user=request.user,
            location=location,
            start_time=start_time,
            end_time=end_time,
            total_price=total_price,
            confirmed=False
        )

        location.is_available = False
        location.save()

        confirmation_link = f"{settings.SITE_URL}/confirm-booking/{booking.id}/"
        send_mail(
            "Підтвердження бронювання",
            f"Перейдіть за посиланням для підтвердження бронювання: {confirmation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return redirect("my_bookings")

    return render(request, "book_location.html", {"location": location})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "my_bookings.html", {"bookings": bookings})


@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    location = booking.location
    booking.delete()
    location.is_available = True
    location.save()
    return redirect("my_bookings")


def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if not booking.confirmed:
        booking.confirmed = True
        booking.save()
    return redirect("my_bookings")