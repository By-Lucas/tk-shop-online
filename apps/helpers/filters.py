import django_filters
from django import forms

from costumers.models import City
from costumers.models import Prefessions


class CityFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(label="Nome da cidade", lookup_expr='icontains', widget=forms.TextInput(
            attrs={
                'class':'form-control','placeholder': 'Digite o nome da cidade'
            }
        ))

    class Meta:
        model = City
        fields = ['uf', 'city']


class PrefessionsFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(label="Nome da profissão", lookup_expr='icontains', widget=forms.TextInput(
            attrs={
                'class':'form-control','placeholder': 'Digite o nome da cidade'
            }
        ))

    class Meta:
        model = Prefessions
        fields = ['description']