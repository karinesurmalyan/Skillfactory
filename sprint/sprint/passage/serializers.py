from .models import *
from rest_framework import serializers


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


class PassageSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    coordinates = CoordinatesSerializer()
    level = LevelsSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Passage
        exclude = ['add_time', 'status']

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coordinates = validated_data.pop('coordinates')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        pass_user = Users.objects.filter(email=user['email'])
        if pass_user.exists():
            user_serializer = UsersSerializer(data=user)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        else:
            user = Users.objects.create(**user)

        coordinates = Coordinates.objects.create(**coordinates)
        level = Levels.objects.create(**level)
        passage = Passage.objects.create(**validated_data, user=user, coordinates=coordinates,
                                         level=level, status='new')

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            Images.objects.create(passage=passage, data=data, title=title)

        return passage
