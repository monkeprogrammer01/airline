from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("flight/<int:flight_id>/", views.flight, name="flight"),
    path("flight/<int:id>/book/", views.book_flight, name="book_flight"),
    path("airport/<int:airport_id>/", views.airport, name="airport"),
    path("bookings/", views.bookings, name="bookings"),
    path("check-booking/", views.check_booking, name="check_booking"),
    path("api/flights/", views.api_flights, name="api_flights"),
    path("api/flights/<int:id>/", views.api_flight_detail, name="api_flight_detail"),
]