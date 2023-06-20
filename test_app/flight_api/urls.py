from django.urls import path
from . import views

urlpatterns = [
    path('airports', views.airports, name="airports"),
    path('airport/<int:airport_id>', views.airport, name="airport"),
    path('flights', views.flights, name="flights")

]