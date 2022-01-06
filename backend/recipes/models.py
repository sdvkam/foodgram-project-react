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

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента', max_length=200, unique=True)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=10)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Amount_Ingredient(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient', verbose_name='ID ингридиента',
        related_name='amount')
    amount = models.PositiveIntegerField(
        'Количество ингридиента')

    class Meta:
        verbose_name = 'Количество ингридента'
        verbose_name_plural = 'Список ингридентов и их количество'

    def __str__(self):
        return self.ingredient


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор рецепта', on_delete=models.CASCADE,
        related_name='recipes')
    name = models.CharField(
        'Название рецепта', max_length=200)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        help_text='Введите дату',
        auto_now_add=True
    )
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

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
