from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class ImagesViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PassageViewset(viewsets.ModelViewSet):
    queryset = Passage.objects.all()
    serializer_class = PassageSerializer

    def create(self, request, *args, **kwargs):
        serializer = PassageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message": None,
                "id": serializer.data['id']
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Bad request",
                "id": None
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ошибка подключения к базе данных",
                "id": None
            })

    def update(self, request, *args, **kwargs):
        pass