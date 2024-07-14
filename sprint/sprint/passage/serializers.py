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
        fields = '__all__'

    def validate(self, data):
        if self.instance is not None:
            user_instance = self.instance.user
            user_data = data.get('user')
            fields_to_validate = [
                user_instance.name != user_data['name'],
                user_instance.fam != user_data['fam'],
                user_instance.otc != user_data['otc'],
                user_instance.email != user_data['email'],
                user_instance.phone != user_data['phone']
            ]

            if user_data is not None and any(fields_to_validate):
                raise ValidationError({'maessage': 'Вы не можете редактировать данные'})
        return data
