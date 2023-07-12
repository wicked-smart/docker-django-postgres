from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from barfoo.models import *
from .serializers import *
from datetime import date, datetime

# Create your views here.

@api_view(['GET', 'POST'])
def airports(request):

    if request.method == 'GET':
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        data = request.data
      

        serializer = AirportSerializer(data=data, context = {'request': request})

        if serializer.is_valid(raise_exception=True):
            #check for unique Airport
            if Airport.objects.filter(**data).exists() :
                return Response({"message": "The combination of city and code must be unique!"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE' ])
def airport(request, airport_id):
    
    try:
        airport = Airport.objects.get(pk=airport_id)
    
    except Airport.DoesNotExist:
        return Response({"message": "Airport does not exists!"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AirportSerializer(airport)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':

        data = request.data
        serializer = AirportSerializer(airport, data=data, partial=True, context = {'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':

        airport.delete()
        return Response({"message": "Succesfully deleted!"}, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
def flights(request):

    if request.method == 'GET':
        flights = Flight.objects.all()

        serializer = FlightSerilizer(flights, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        data = request.data
        serializer = FlightSerilizer(data=data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET', 'PUT', 'DELETE'])
def flight(request, flight_id):

    try:
        flight = Flight.objects.get(pk=flight_id)
    
    except Flight.DoesNotExist:
        return Response({"message": "Flight Does not exists!"}, status=status.HTTP_404_NOT_FOUND )

    if request.method == 'GET':

        serializer = FlightSerilizer(flight, context = {"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        data = request.data
        serializer = FlightSerilizer(flight, data=data, partial=True, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        
        flight_test = f"{flight.origin.code}-{flight.destination.code}"
        flight.delete()
        return Response({"message": "%s Flight got deleted!" % (flight_test)}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def flight_book(request, flight_id):

    try:
        flight = Flight.objects.get(pk=flight_id)
    
    except Flight.DoesNotExist:
        return Response({'message': 'Flight does not exists! '})
    
    if request.method == 'GET':
        print(request.query_params)
        params =request.query_params

        if len(params) == 0:
            bookings = FlightBook.objects.filter(flight=flight)

        else:
            # Use QuerySerializer defined in the serializer file to validate and serializer query params
            query_serializer = BookingQueryParamsSerializer(data=params)
            if query_serializer.is_valid():

                on_date = params.get('on_date', None)
                from_date = params.get('from_date', None)
                to_date = params.get('to_date', None)

                if on_date:
                    bookings=FlightBook.objects.filter(flight=flight, booked_at__date=datetime.strptime(on_date, "%d-%m-%Y"))
                elif from_date and to_date:
                    bookings = FlightBook.objects.filter(flight=flight, 
                                                    booked_at__date__gte=datetime.strptime(from_date, "%d-%m-%Y"),
                                                    booked_at__date__lte=datetime.strptime(to_date, "%d-%m-%Y")
                                                )
            else:
                return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

        if not bookings.exists():
            return Response({'message': 'No bookings on this flight exists yet!'})
        else:
            serializer = FlightBookingSerializer(bookings, many=True, context={'request': request, 'flight': flight})
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data

        serializer = FlightBookingSerializer(data=data, context={'request': request, 'flight':flight})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def bookings(request, booking_ref):

    try:
        booking = FlightBook.objects.filter(booking_ref=booking_ref)
    except FlightBook.DoesNotExist:
        return Response({'message': 'Booking Does not exists!'})
    
        
    if request.method == 'GET':

        serializer = FlightBookingSerializer(booking[0], context={'request': request, 'booking': booking})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':

        data = request.data 

        serializer = FlightBookingSerializer(booking[0], data=data, partial=True, context={'request': request, 'booking': booking})


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == 'DELETE':

        booking.delete()

        return Response({'message': 'Succesfully deleted!'}, status=status.HTTP_200_OK)

