from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateInput

class PostFilter(FilterSet):
    date_in = DateFilter(
        field_name = 'date_in',
        widget = DateInput(attrs={'type': 'date'}),
        label = 'Date',
        lookup_expr = 'date__gte'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'date_in': ['gt'],
        }