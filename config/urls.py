from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from config.views import home, register, dashboard, create_booking, my_bookings, location_detail, complete_booking, confirm_booking

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create-booking/", create_booking, name="create_booking"),
    path("location/<int:location_id>/", location_detail, name="location_detail"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    path("complete-booking/<int:booking_id>/", complete_booking, name="complete_booking"),
    path("confirm-booking/<int:booking_id>/", confirm_booking, name="confirm_booking"),
]