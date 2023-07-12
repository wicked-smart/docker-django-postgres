from django.urls import path
from . import views

urlpatterns = [
    path('airports', views.airports, name="airports"),
    path('airport/<int:airport_id>', views.airport, name="airport"),
    path('flights', views.flights, name="flights"),
    path('flight/<int:flight_id>', views.flight, name="flight"),
    path('flight/<int:flight_id>/book', views.flight_book, name="book"),
    path('flight/bookings/<str:booking_ref>', views.bookings, name="bookings")

]