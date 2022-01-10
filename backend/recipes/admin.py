from django.contrib import admin
from .models import (
    Tag, Ingredient, Amount_Ingredient, Recipe, Subscriptions, User)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_editable = ('name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    list_editable = ('name', 'measurement_unit')


class Amount_IngredientAdmin(admin.ModelAdmin):
    search_fields = ('ingredient__name', 'ingredient__measurement_unit')
    list_filter = ('amount',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'amount_favorites')
    search_fields = ('name',)
    list_filter = ('author', 'tag')
    list_editable = ('name', 'author')
    readonly_fields = ('amount_favorites',)

    def amount_favorites(self, obj):
        return obj.favorite.count()

    amount_favorites.short_description = "Этот рецепта добавили в избранное"


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_editable = ('email',)
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Amount_Ingredient, Amount_IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscriptions)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
