from django.db import models
from .extensions import *
# from .services import get_path_upload_photos


class Users(models.Model):
    email = models.EmailField()
    fam = models.TextField(max_length=30, verbose_name="Фамилия")
    name = models.TextField(max_length=30, verbose_name="Имя")
    otc = models.TextField(max_length=30, verbose_name="Отчество")
    phone = models.CharField(max_length=30, verbose_name="Номер телефона")

    class Meta:
        verbose_name = "Турист"


class Coordinates(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    class Meta:
        verbose_name = 'Координаты'


class Levels(models.Model):
    winter = models.CharField(max_length=3, choices=LEVEL, verbose_name='Зима', null=True, blank=True)
    spring = models.CharField(max_length=3, choices=LEVEL, verbose_name='Весна', null=True, blank=True)
    summer = models.CharField(max_length=3, choices=LEVEL, verbose_name='Лето', null=True, blank=True)
    autumn = models.CharField(max_length=3, choices=LEVEL, verbose_name='Осень', null=True, blank=True)

    class Meta:
        verbose_name = 'Уровень сложности'


class Passage(models.Model):
    beauty_title = models.TextField(blank=True, null=True, verbose_name='Название')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название вершины')
    other_titles = models.CharField(max_length=100, blank=True, null=True, verbose_name='Другие названия')
    connect = models.TextField(blank=True, null=True, verbose_name='Что соединяет')
    add_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
    coordinates = models.ForeignKey(Coordinates, on_delete=models.CASCADE)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='new')

    class Meta:
        verbose_name = 'Перевал'


class Images(models.Model):
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    data = models.URLField(blank=True, null=True)
    title = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
