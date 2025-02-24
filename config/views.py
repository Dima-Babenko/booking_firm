from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from config.forms import RegisterForm
from booking.models import Location, Booking
from datetime import datetime

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
    locations = Location.objects.filter(is_available=True)
    return render(request, "create_booking.html", {"locations": locations})


@login_required
def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    if request.method == "POST":
        email = request.POST.get("email")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if not email or not start_date or not end_date:
            return render(request, "location_detail.html", {
                "location": location,
                "error": "Будь ласка, заповніть всі поля."
            })

        start_time = datetime.strptime(start_date, "%Y-%m-%d")
        end_time = datetime.strptime(end_date, "%Y-%m-%d")

        # Перевірка наявності бронювання
        overlapping_bookings = Booking.objects.filter(
            location=location,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_bookings.exists():
            return render(request, "location_detail.html", {
                "location": location,
                "error": "Ця локація вже зайнята у вибрані дати."
            })

        days = (end_time - start_time).days
        total_price = location.price * days

        booking = Booking.objects.create(
            user=request.user,
            location=location,
            start_time=start_time,
            end_time=end_time,
            total_price=total_price,
            confirmed=False
        )

        confirmation_link = f"{settings.SITE_URL}/confirm-booking/{booking.id}/"
        send_mail(
            "Підтвердження бронювання",
            f"Перейдіть за посиланням для підтвердження бронювання: {confirmation_link}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return redirect("my_bookings")

    return render(request, "location_detail.html", {"location": location})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "my_bookings.html", {"bookings": bookings})


@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect("my_bookings")


def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if not booking.confirmed:
        booking.confirmed = True
        booking.save()
    return redirect("my_bookings")
