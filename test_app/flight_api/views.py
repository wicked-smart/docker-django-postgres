from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from barfoo.models import *
from .serializers import *

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

        serializer = FlightSerilizer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        data = request.data
        serializer = FlightSerilizer(data=data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        