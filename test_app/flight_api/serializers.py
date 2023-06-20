from rest_framework import serializers
from barfoo.models import *
from rest_framework.validators import UniqueTogetherValidator



class AirportSerializer(serializers.ModelSerializer):
    departures = serializers.StringRelatedField(required=False, many=True)
    arrivals = serializers.StringRelatedField(required=False, many=True)

    class Meta:
        model = Airport
        fields = [ "id", "city", "code", "departures", "arrivals"]
        extra_kwargs = {
            "city": {"required": True},
            "code": {"required": True}
        }
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        request = self.context.get('request', None)

        if request and ( request.method == 'POST' or request.method == 'PUT' ) :
            ret.pop('departures')
            ret.pop('arrivals')
        
        return ret





# Flight Serializer 
class FlightSerilizer(serializers.ModelSerializer):
    origin  = AirportSerializer(required=True)
    destination = AirportSerializer(required=True)
    passengers = serializers.StringRelatedField(required=False, many=True)

    class Meta:
        model = Flight
        fields = ["id", "origin", "destination", "duration", "passengers"]
        extra_kwargs = {
            "duration": {"required": True}
        
        }
        #validators = [UniqueTogetherValidator(queryset=Flight.objects.all(), fields=['origin', 'destination', 'duration'])]

    def validate(self, attrs):

        origin = attrs.pop('origin')
        destination = attrs.pop('destination')

        origin_airport = Airport.objects.filter(**origin)
        destination_airport = Airport.objects.filter(**destination)

        if origin_airport.exists() and destination_airport.exists() :   
            if Flight.objects.filter(origin=origin_airport[0], destination=destination_airport[0], **attrs).exists():
                raise serializers.ValidationError("Flight already exists! Try with diffrent one...")

        attrs['origin'] = origin
        attrs['destination'] = destination

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get('request', None)

        if request and request.method == 'POST':
            representation.pop('passengers')
        
        return representation

    def create(self, validated_data):

        origin = validated_data.pop('origin')
        destination = validated_data.pop('destination')

        origin_flight, created = Airport.objects.get_or_create(**origin)
        destination_flight, created = Airport.objects.get_or_create(**destination)

        return Flight.objects.create(origin=origin_flight, destination=destination_flight, **validated_data)



