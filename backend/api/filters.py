from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (ChoiceFilter,
                                                   ModelMultipleChoiceFilter)
from recipes.models import Recipe, Tag


class MyFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())
        return kwargs


class RecipeFilter(FilterSet):
    STATUS_CHOICES = (
        (0, 'False'),
        (1, 'True'),
    )

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user

    is_favorited = ChoiceFilter(
        choices=STATUS_CHOICES, method='filter_is_favorited')
    is_in_shopping_cart = ChoiceFilter(
        choices=STATUS_CHOICES, method='filter_is_in_shopping_cart')
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        if value == '0':
            return queryset.exclude(favorite__username=self.current_user)
        return queryset.filter(favorite__username=self.current_user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value == '0':
            return queryset.exclude(shopping__username=self.current_user)
        return queryset.filter(shopping__username=self.current_user)
