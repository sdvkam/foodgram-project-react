from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Имя тега', max_length=200, unique=True)
    color = models.CharField(
        'HEX-код цвета для тега', max_length=7,
        unique=True, null=True, blank=True)
    slug = models.SlugField(
        'Английское имя для тега', unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента', max_length=200)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient')
        ]

    def __str__(self):
        return ' '.join([self.name, '(', self.measurement_unit, ')'])


class AmountIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, related_name='amount', on_delete=models.CASCADE,
        verbose_name='Ингридиент')
    amount = models.PositiveIntegerField(
        'Количество ингридиента')

    class Meta:
        ordering = ['ingredient', 'amount']
        verbose_name = 'Количество ингридента'
        verbose_name_plural = 'Список ингридентов и их количество'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'amount'],
                name='unique_amountingredient')
        ]

    def __str__(self):
        return (' '.join([
            str(self.ingredient), '=',
            str(self.amount)]))


class Recipe(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes', on_delete=models.CASCADE,
        verbose_name='Автор рецепта')
    name = models.CharField(
        'Название рецепта', max_length=200)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', help_text='Введите дату',
        auto_now_add=True
    )
    image = models.ImageField(
        'Фотография блюда', upload_to='recipes/')
    text = models.TextField(
        'Описание')
    ingredients = models.ManyToManyField(
        AmountIngredient, related_name='recipes',
        verbose_name='Ингридиенты и их количество')
    tags = models.ManyToManyField(
        Tag, related_name='recipes',
        verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах')
    favorite = models.ManyToManyField(
        User, related_name='favorite_recipes',
        blank=True,
        verbose_name='Пользователи, обожающие этот рецепт')
    shopping = models.ManyToManyField(
        User, related_name='shopping_list',
        blank=True,
        verbose_name='Пользователи, собирающиеся готовить по этому рецепту')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Subscriptions(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
        help_text='Выберите пользователя, который хочет подписаться на кого-то'
    )
    selected_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='selected_author',
        verbose_name='Отслеживаемый автор рецептов',
        help_text='Выберите автора рецептов, на которого вы хотите подписаться'
    )

    class Meta:
        ordering = ['subscriber']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'selected_author'],
                name='unique_subscription')
        ]

    def save(self, *args, **kwargs):
        if self.subscriber == self.selected_author:
            return
        else:
            super().save(*args, **kwargs)
