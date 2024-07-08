from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError


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
        exclude = ['status']

    def validate(self, data):
        user_data = data.get('user')
        user = self.instance.user
        if user_data is not None:
            if user.name != user_data.get('name') \
                    or user.fam != user_data.get('fam') \
                    or user.otc != user_data.get('otc') \
                    or user.email != user_data.get('email') \
                    or user.phone != user_data.get('phone'):
                raise ValidationError({'maessage': 'Вы не можете редактировать данные'})
            return data
