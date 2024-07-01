from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['fam', 'name', 'otc', 'email', 'phone']


class CoordinatesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coordinates
        fields = ['latitude', 'longitude', 'height']


class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = ['winter', 'spring', 'summer', 'autumn']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['data', 'title']


class PassageSerializer(WritableNestedModelSerializer):
    user = UsersSerializer()
    coordinates = CoordinatesSerializer()
    level = LevelsSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Passage
        exclude = ['add_time', 'status']
