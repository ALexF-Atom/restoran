from rest_framework import serializers

from hall.models import Restoran, Hall
# from reserver.models import Client, Reservation


class ResRestoranApi(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restoran
        fields = '__all__'


class HallApi(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'
