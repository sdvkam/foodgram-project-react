from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Имя тега', max_length=200, unique=True,
        help_text=('Обязательно. Должно быть уникальным.'
                   '<br>Максимум 200 символов.')
    )
    color = models.CharField(
        'HEX-код цвета для тега', max_length=7, unique=True,
        help_text=('Обязательно. Должно быть уникальным.'
                   '<br>Пример: "#FF0000" - это красный')
    )
    slug = models.SlugField(
        'Английское имя для тега', max_length=200, unique=True,
        help_text=('Обязательно. Должно быть уникальным.'
                   '<br>Английские буквы, цифры, подчеркивания или дефисы.')
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента', max_length=200,
        help_text='Обязательно. Максимум 200 символов.')
    measurement_unit = models.CharField(
        'Единица измерения', max_length=200,
        help_text='Обязательно. Максимум 200 символов.')

    class Meta:
        ordering = ['name']
        verbose_name = 'ингридиент'
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
        verbose_name='Ингридиент', help_text='Обязательно.')
    amount = models.PositiveIntegerField(
        'Количество ингридиента', validators=[MinValueValidator(1)],
        help_text='Обязательно. Целое число >= 1.')

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
        verbose_name='Автор рецепта', help_text='Обязательно.')
    name = models.CharField(
        'Название рецепта', max_length=200,
        help_text='Обязательно. Максимум 200 символов.')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', help_text='Введите дату',
        auto_now_add=True
    )
    image = models.ImageField(
        'Фотография блюда', upload_to='recipes/',
        help_text='Обязательно.')
    text = models.TextField(
        'Описание', help_text='Обязательно.')
    ingredients = models.ManyToManyField(
        AmountIngredient, related_name='recipes',
        verbose_name='Ингридиенты и их количество', help_text='Обязательно.')
    tags = models.ManyToManyField(
        Tag, related_name='recipes',
        verbose_name='Теги', help_text='Обязательно.')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах', help_text='Обязательно.',
        validators=[MinValueValidator(1)])
    favorite = models.ManyToManyField(
        User, related_name='favorite_recipes',
        blank=True,
        verbose_name='Пользователи, обожающие этот рецепт')
    shopping = models.ManyToManyField(
        User, related_name='shopping_list',
        blank=True,
        verbose_name='Пользователи, собирающиеся готовить по этому рецепту')
    slug = models.SlugField(
        'Английское имя для рецепта', max_length=200, unique=True, blank=True,
        help_text=('cxcvzxУникальное.<br>Можно оставить пустым, '
                   'тогда будем сформирован автоматически '
                   'из названия рецепта и его номера в базе.'
                   '<br>Будьте осторожны при самостоятельном редактировании.'))

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def clean(self):
        slug = self.slug
        if slug == '':
            slug = slugify(
                self.name.translate(
                    str.maketrans(settings.DICT_TRANSLIT_RUS_TO_ENGLISH)))
            self.slug = f'{slug}_{self.id}'


class Subscriptions(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber',
        verbose_name='Подписчик',
        help_text=(
            'Обязательно.'
            '<br>Выберите пользователя, который хочет подписаться на кого-то')
    )
    selected_author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='selected_author',
        verbose_name='Отслеживаемый автор рецептов',
        help_text=(
            'Обязательно.'
            '<br>Выберите автора рецептов, на которого вы хотите подписаться')
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

    def clean(self):
        if self.subscriber == self.selected_author:
            raise ValidationError('Нельзя подписаться на самого себя')
