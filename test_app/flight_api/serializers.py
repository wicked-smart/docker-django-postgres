from rest_framework import serializers
from barfoo.models import *
from rest_framework.validators import UniqueTogetherValidator
from collections import OrderedDict



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

    #dynamically modify FlightSerializer fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.method == 'PUT':
            self.fields['origin'].allow_null = True
            self.fields['destination'].allow_null = True
            


    class Meta:
        model = Flight
        fields = ["id", "origin", "destination", "duration", "passengers"]
        extra_kwargs = {
            "duration": {"required": True}
        
        }
        #validators = [UniqueTogetherValidator(queryset=Flight.objects.all(), fields=['origin', 'destination', 'duration'])]

    def validate(self, attrs):

        request = self.context.get('request')
        if request and request.method == 'PUT':
            #get the instance 
            flight = self.instance

            #get the attributes
            origin = attrs.get('origin')
            destination = attrs.get('destination')
            duration = attrs.get('duration')

            if not origin and not destination:
                if not duration: 
                    raise serializers.ValidationError("All Fields can't be empty!")
                else:
                    return attrs
            
            if origin is not None:
                origin_airport = Airport.objects.filter(**origin)

            if destination is not None:
                destination_airport = Airport.objects.filter(**destination)

            if origin is None and destination_airport.exists():
                origin = flight.origin
                destination = destination_airport[0]

            elif destination is None and origin_airport.exists():
                origin = origin_airport[0]
                destination = flight.destination

            else:
                return attrs
            
            temp = Flight.objects.filter(origin=origin, destination=destination, duration=duration)    
            if temp.exists():
                raise serializers.ValidationError("The Flight already exists !")

            return attrs

        elif request and request.method == 'POST':

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
        rep = super().to_representation(instance)

        request = self.context.get('request', None)

        if request and ( request.method == 'POST' or request.method == 'PUT') :
            rep.pop('passengers')

        elif request and request.method == 'GET':

            keys = list(rep.keys())

            origin  = rep.pop('origin')
            destination = rep.pop('destination')
            

            #code to maintain order of the origin `rep` function
            origin_idx = keys.index('origin')
            
            temp = OrderedDict()

            #flatten the API response
            keys.insert(origin_idx, 'origin_city')
            keys.insert(origin_idx+1, 'origin_code')

            keys.insert(origin_idx+2, 'destination_city')
            keys.insert(origin_idx+3, 'destination_code')

            temp_keys = {
                "origin_city": origin['city'],
                "origin_code": origin['code'],
                "destination_city": destination['city'],
                "destination_code": destination['code']
            }

            for k in keys:
                if k in list(rep.keys()):
                    temp[k] = rep[k]
                elif k in temp_keys.keys():
                    temp[k] = temp_keys[k]
                    
            rep = temp
        
        return rep

    def create(self, validated_data):

        origin = validated_data.pop('origin')
        destination = validated_data.pop('destination')

        origin_flight, created = Airport.objects.get_or_create(**origin)
        destination_flight, created = Airport.objects.get_or_create(**destination)

        return Flight.objects.create(origin=origin_flight, destination=destination_flight, **validated_data)


    def update(self, instance, validated_data):
        origin = validated_data.get('origin')
        destination = validated_data.get('destination')
        duration = validated_data.get('duration')

        if origin is not None:
           origin_instance, _ = Airport.objects.get_or_create(**origin)
           instance.origin = origin_instance

        if destination is not None:
           destination_instance, _ = Airport.objects.get_or_create(**destination)
           instance.destination = destination_instance

        if duration is not None:
           instance.duration = duration

        instance.save()
        return instance




