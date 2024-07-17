from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class PassageViewset(viewsets.ModelViewSet):
    queryset = Passage.objects.all()
    serializer_class = PassageSerializer
    filterset_fields = ['user__email']

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

    def partial_update(self, request, *args, **kwargs):
        passage = self.get_object()
        if passage.status == 'new':
            serializer = PassageSerializer(passage, data=request.data, partial=True)
            if serializer.is_valid():
                return Response({
                    "status": "1",
                    "message": "Запись успешно изменена"
                })
            else:
                return Response({
                    "status": "0",
                    "message": serializer.errors
                })
        else:
            return Response({
                "status": "0",
                "message": f'Отклонено! Запись уже {passage.get_status_display()}'
            })
