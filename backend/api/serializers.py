import base64
import imghdr
import uuid

import six
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (AmountIngredient, Ingredient, Recipe,
                            Subscriptions, Tag, User)


class EmptySerializer(serializers.Serializer):
    pass


class MyTokenSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ('email', 'password')


def validate_string_empty(value):
    if value.strip() == '' or value is None:
        raise serializers.ValidationError(
            'Это поле обязательно для заполнения.')
    return value


class UserMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'help_text': 'Required.'},
            'first_name': {'help_text': 'Required.'},
            'last_name': {'help_text': 'Requred.'}
        }

    def validate_email(self, value):
        return validate_string_empty(value)

    def validate_first_name(self, value):
        return validate_string_empty(value)

    def validate_last_name(self, value):
        return validate_string_empty(value)


class UserWithPasswordSerializer(UserMiniSerializer):

    class Meta(UserMiniSerializer.Meta):
        fields = UserMiniSerializer.Meta.fields + ('password',)
        extra_kwargs = {
            **UserMiniSerializer.Meta.extra_kwargs,
            **{'password': {'help_text': 'Required.', 'write_only': True}}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(UserMiniSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserMiniSerializer.Meta):
        fields = UserMiniSerializer.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if not current_user.is_authenticated:
            return False
        is_subscribed = Subscriptions.objects.filter(
            subscriber=current_user, selected_author=obj).count()
        return bool(is_subscribed)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngedientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class AmountIngredientSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField(read_only=True,)
    measurement_unit = serializers.SerializerMethodField(read_only=True,)

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class ImageBase64(serializers.Field):

    def to_representation(self, value):
        return value.url

    def to_internal_value(self, data):
        if not isinstance(data, six.string_types):
            self.fail('Что-то не так с картинкой')
        default_extension = 'jpg'
        if 'data:' in data and ';base64,' in data:
            header, data = data.split(';base64,')
            # не всегда можно определить расширение картинки по ее байтикам
            if '/' in header:
                default_extension = header.split('/')[1]
        try:
            decoded_image = base64.b64decode(data)
        except TypeError:
            self.fail('Что-то не так с картинкой')
        file_name = str(uuid.uuid4())[:8]
        extension = imghdr.what(file_name, decoded_image)
        if extension is None:
            extension = default_extension
        if extension == "jpeg":
            extension = "jpg"
        data = ContentFile(
            decoded_image,
            name='.'.join([file_name, extension])
        )
        return data


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags_for_read = TagSerializer(many=True, read_only=True, source='tags')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = AmountIngredientSerializer(many=True, required=True)
    image = ImageBase64(required=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'ingredients', 'tags', 'tags_for_read', 'author',
            'is_favorited', 'is_in_shopping_cart', 'image',
            'name', 'text', 'cooking_time')
        extra_kwargs = {
            'tags': {'write_only': True, 'required': True}
        }

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user
        if not current_user.is_authenticated:
            return False
        is_favorited = obj.favorite.filter(username=current_user).count()
        return bool(is_favorited)

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user
        if not current_user.is_authenticated:
            return False
        is_in_shopping_cart = obj.shopping.filter(
            username=current_user).count()
        return bool(is_in_shopping_cart)

    def create(self, validated_data):
        validated_data.pop('ingredients')
        ingredients = self.initial_data['ingredients']
        tags = validated_data.pop('tags')
        validated_data['author'] = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        amount_ingredient = []
        for ingredient in ingredients:
            cur_ingredient, status = AmountIngredient.objects.get_or_create(
                ingredient_id=ingredient['id'], amount=ingredient['amount'])
            amount_ingredient.append(cur_ingredient.id)
        recipe.ingredients.set(amount_ingredient)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.tags.set(validated_data.get('tags', instance.tags))
        if 'ingredients' in self.initial_data:
            amount_ingredient = []
            for ingredient in self.initial_data['ingredients']:
                cur_ingredient, status = (
                    AmountIngredient.objects.get_or_create(
                        ingredient_id=ingredient['id'],
                        amount=ingredient['amount']))
                amount_ingredient.append(cur_ingredient.id)
            instance.ingredients.set(amount_ingredient)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return_data = {}
        return_data['id'] = data['id']
        return_data['tags'] = data['tags_for_read']
        return_data['author'] = data['author']
        return_data['ingredients'] = data['ingredients']
        return_data['is_favorited'] = data['is_favorited']
        return_data['is_in_shopping_cart'] = data['is_in_shopping_cart']
        return_data['name'] = data['name']
        return_data['image'] = data['image']
        return_data['text'] = data['text']
        return_data['cooking_time'] = data['cooking_time']
        return return_data


class RecipeMiniFields(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserWithRecipes(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        if 'recipes_limit' in self.context['request'].query_params:
            recipes_limit = (
                int(self.context['request'].query_params['recipes_limit']))
            if type(recipes_limit) == int:
                queryset = queryset[:int(recipes_limit)]
        serializer = RecipeMiniFields(queryset, many=True)
        return serializer.data


class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=150, write_only=True, required=True)
    current_password = serializers.CharField(
        max_length=150, write_only=True, required=True)


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriptions
        fields = ('subscriber', 'selected_author')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscriptions.objects.all(),
                fields=('subscriber', 'selected_author'),
                message='Такая подписка уже существует'
            )
        ]

    def validate(self, data):
        if data['subscriber'] == data['selected_author']:
            raise serializers.ValidationError(
                'Нельзя подписатся на самого себя.')
        return data
