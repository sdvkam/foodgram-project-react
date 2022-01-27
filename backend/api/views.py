from http import HTTPStatus

from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Subscriptions, Tag, User

from .filters import MyFilterBackend, RecipeFilter
from .paginations import MyCustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (EmptySerializer, IngedientSerializer,
                          RecipeSerializer, SubscriptionsSerializer,
                          TagSerializer, UserChangePasswordSerializer,
                          UserSerializer, UserWithPasswordSerializer,
                          UserWithRecipes)
from .utilities import shop_favorite_add_delete


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = (MyFilterBackend,)
    filter_class = RecipeFilter

    def get_filterset_kwargs(self):
        return {
            'current_user': self.request.user,
        }

    def get_serializer_class(self):
        if self.action in [
            'shopping_cart',
            'favorite', 'download_shopping_cart'
        ]:
            return EmptySerializer
        else:
            return RecipeSerializer

    @action(
        detail=False, methods=['GET'],
        permission_classes=(permissions.IsAuthenticated, ))
    def download_shopping_cart(self, request):
        list_ingredients = Ingredient.objects.filter(
            amount__recipes__shopping=request.user
            ).annotate(
                nums=Sum('amount__amount'))
        list_response = []
        for i, obj in enumerate(list_ingredients, start=1):
            one = f'{i}. {obj.name} ({obj.measurement_unit}) — {obj.nums}'
            list_response.append(one)
        response = HttpResponse(
            '\n'.join(list_response),
            content_type='text/plain; charset=utf-8',
            status=HTTPStatus.OK)
        response['Content-Disposition'] = 'attachment; filename="shopping.txt"'
        return response

    @action(
        detail=True, methods=['POST', 'DELETE'],
        permission_classes=(permissions.IsAuthenticated, ))
    def shopping_cart(self, request, pk):
        data = shop_favorite_add_delete(
            request.method, pk, request.user, True,
            'список покупок', 'списка покупок')
        return Response(data[0], data[1])

    @action(
        detail=True, methods=['POST', 'DELETE'],
        permission_classes=(permissions.IsAuthenticated, ))
    def favorite(self, request, pk):
        data = shop_favorite_add_delete(
            request.method, pk, request.user, False,
            'избранное', 'избранного')
        return Response(data[0], data[1])


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngedientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngedientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', )


class ListCreateRetrieveViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class UserViewSet(ListCreateRetrieveViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    pagination_class = MyCustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserWithPasswordSerializer
        elif self.action == 'set_password':
            return UserChangePasswordSerializer
        elif self.action == 'subscriptions':
            return UserWithRecipes
        elif self.action == 'subscribe':
            return SubscriptionsSerializer
        else:
            return UserSerializer

    @action(
        detail=False, methods=['GET'], url_path='me',
        permission_classes=(permissions.IsAuthenticated,))
    def get_yourself(self, request):
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,))
    def set_password(self, request):
        data = {
            'new_password': request.data.get('new_password'),
            'current_password': request.data.get('current_password')
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.check_password(data['current_password']):
            user.set_password(data['new_password'])
            user.save()
            return Response(
                'Пароль успешно изменен.', status=status.HTTP_204_NO_CONTENT)
        return Response(
            'Неправильный текущий пароля.', status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        selected_authors = User.objects.filter(
            selected_author__subscriber=request.user).order_by('id')
        page = self.paginate_queryset(selected_authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(selected_authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=['POST', 'DELETE'],
        permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, pk):
        selected = get_object_or_404(User, id=pk)
        data = {
            'subscriber': request.user.id,
            'selected_author': selected.id
        }
        if request.method == 'POST':
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        subscription = get_object_or_404(
            Subscriptions, subscriber=request.user, selected_author=selected)
        subscription.delete()
        return Response('Вы отписались',  status.HTTP_204_NO_CONTENT)
