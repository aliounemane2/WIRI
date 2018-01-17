from jmrequests.models import *
from rest_framework import serializers
from jmspots.serializers import SpotSerializer, CardSerializer
from users.serializers import UserSerializer





class RequestSerializer(serializers.ModelSerializer):

    spot =  SpotSerializer(read_only=True)
    card = CardSerializer(read_only=True)
    # sender = UserSerializer(read_only=True)
    # receivers = Request_ReceiversSerializer(read_only=True)


    class Meta:
        model = Request
        fields = '__all__'
        depth = 2



class Request_ReceiversSerializer(serializers.ModelSerializer):

    # spot =  SpotSerializer(read_only=True)
    # card = CardSerializer(read_only=True)


    # sender = UserSerializer(view_name='')
    # sender = serializers.StringRelatedField(many=True)
    # list_receivers = UserSerializer(read_only=True)
    # receivers = RequestSerializer(read_only=True)


    class Meta:
        model = Request_Receivers
        fields = '__all__'
        depth = 2
        #fields = ('sender', 'sender__first_name', 'sender__last_name', 'list_receivers__id', 'list_receivers__first_name', 'list_receivers__last_name',
        #          'is_active', 'state')
        #fields = ('sender', 'sender_first_name', 'list_receivers', 'is_active', 'state')



