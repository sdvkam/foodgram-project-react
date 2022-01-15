from django.contrib import admin
from .models import (
    Tag, Ingredient, AmountIngredient, Recipe, Subscriptions, User)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_editable = ('name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    list_editable = ('name', 'measurement_unit')


class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'amount')
    search_fields = (
        'ingredient__name', 'ingredient__measurement_unit',
        'amount', 'recipes__name')
    list_filter = ('recipes',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'amount_favorites')
    search_fields = ('name',)
    list_filter = ('author', 'tags')
    list_editable = ('name', 'author')
    readonly_fields = ('amount_favorites',)

    def amount_favorites(self, obj):
        return obj.favorite.count()

    amount_favorites.short_description = "Этот рецепт добавили в избранное"


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_editable = ('email',)
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'selected_author')
    list_editable = ('subscriber', 'selected_author')
    list_filter = ('subscriber', 'selected_author')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(AmountIngredient, AmountIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
