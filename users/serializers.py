from users.models import *
from rest_framework import serializers
from fcm.models import Device





class InterestSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_url')
    #
    def get_url(self, obj):
         return obj.image.url

    class Meta:
        model = Interest
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # interest = InterestSerializer(read_only=True)

    #photo = serializers.SerializerMethodField('get_url')

    #def get_url(self, obj):
    #     return obj.image.url

    class Meta:
        model = User
        fields = '__all__'




class FavouriteContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteContact
        fields = '__all__'
        depth = 2


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

    # fields = ('dev_id','reg_id','name','is_active')
