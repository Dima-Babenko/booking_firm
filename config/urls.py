from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from config.views import home, register, dashboard, create_booking, my_bookings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path('create-booking/', create_booking, name='create_booking'),
    path('my-bookings/', my_bookings, name='my_bookings'),
]