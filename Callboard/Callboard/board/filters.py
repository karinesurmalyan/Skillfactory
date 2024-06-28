from django_filters import FilterSet, DateFilter, CharFilter, ChoiceFilter
from .models import Announcement, Comment
from django import forms
from django.forms import DateInput
from .extensions import *


class PostFilter(FilterSet):
    date_in = DateFilter(
        field_name='date_in',
        widget=DateInput(attrs={'type': 'date'}),
        label='Date',
        lookup_expr='date__gte'
    )

    category = CharFilter(
        choices=ROLES,
        label='Категория',
        widget=forms.Select(attrs={'class': 'myfield'})
    )

    title = CharFilter(
        label='Заголовок',
        lookup_expr='icontains',
        field_name='title',
        widget=forms.TextInput(attrs={'class': 'myfield'}),
    )

    class Meta:
        model = Announcement
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = [
            'comment_post',
        ]