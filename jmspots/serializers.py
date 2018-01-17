from jmspots.models import *
from rest_framework import serializers


class HorairesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horaires
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 2


class SpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spot
        fields = '__all__'
        depth = 3


class EventSerializer(serializers.ModelSerializer):
    spot = SpotSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        depth = 2



class InstitutionSerializer(serializers.ModelSerializer):
    spot = SpotSerializer(read_only=True)

    class Meta:
        model = Institution
        fields = '__all__'
        depth = 2


class CardSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    institution = InstitutionSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    spot = SpotSerializer(read_only=True)



    class Meta:
        model = Card
        fields = '__all__'
        depth = 3




class UserCardSerializer(serializers.ModelSerializer):
    # spot = serializers.ReadOnlyField(read_only=True)
    spot = SpotSerializer(read_only=True)


    class Meta:
        model = UserCard
        # fields = '__all__' avant
        fields = ('sender', 'card', 'spot', 'id')
        depth = 3


class UserCardFavouriteSerializer(serializers.ModelSerializer):
    spot = SpotSerializer(read_only=True) # à commenter
    # spot = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = UserCardFavourite
        # fields = '__all__'
        fields = ('card', 'spot')
        depth = 3