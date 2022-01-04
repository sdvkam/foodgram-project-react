from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Имя тега', max_length=100, unique=True)
    color = models.CharField(
        'HEX-код цвета для тега', max_length=7, unique=True)
    slug = models.SlugField(
        'Английское имя для тега', unique=True)


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента', max_length=200, unique=True)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=10)


class Amount_Ingredient(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient', verbose_name='ID ингридиента',
        related_name='amount')
    amount = models.PositiveIntegerField(
        'Количество ингридиента')


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор рецепта', on_delete=models.CASCADE,
        related_name='recipes')
    name = models.CharField(
        'Название рецепта', max_length=200)
    image = models.ImageField(
        'Фотография блюда', upload_to='recipes/')
    text = models.TextField(
        'Описание')
    ingredients = models.ManyToManyField(
        'Amount_Ingredient', verbose_name='Ингридиенты и их количество',
        related_name='recipes')
    tag = models.ManyToManyField(
        'Tag', verbose_name='Тег', related_name='recipes')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления')
