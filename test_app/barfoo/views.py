from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.urls import reverse

# Create your views here.

def index(request):
    flights = Flight.objects.select_related().all()

    return render(request, "barfoo/index.html", {
        "flights": flights
    })


def flight(request, flight_id):

    try:
        flight = Flight.objects.get(id=flight_id)
        passengers = flight.passengers.all()
        non_passengers = Passenger.objects.exclude(flight=flight)

        return render(request, "barfoo/flight.html", {
            "flight": flight,
            "passengers": passengers,
            "non_passengers": non_passengers
        })
    
    except Flight.DoesNotExist:
        return render(request, "barfoo/index.html", {
            "message" : "Flight does not exists!"
        })
     

def book_flight(request, flight_id):

    flight = Flight.objects.get(id=flight_id)

    passenger_id = int(request.POST.get("passenger"))
    passenger = Passenger.objects.get(id=passenger_id)

    flight.passengers.add(passenger)
    return HttpResponseRedirect(reverse("flight",  args=(flight_id,)))
