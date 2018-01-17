from chatroom.models import *
from rest_framework import serializers
from users.serializers import *

class ChatGroupSerializer(serializers.ModelSerializer):
    # spot =  SpotSerializer(read_only=True)
    # users = UserSerializer(write_only=True)
    # users = serializers.StringRelatedField(many=True)

    class Meta:
        model = ChatGroup
        fields = '__all__'
        depth = 2


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # fields = '__all__'
        fields = ('content', 'photo', 'date_created', 'users')
        depth = 2



class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        depth = 2


