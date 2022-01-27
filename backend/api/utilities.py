from rest_framework import status

from recipes.models import Recipe

from .serializers import RecipeMiniFields


def shop_favorite_add_delete(method, recipe_id, user, is_shopping_list,
                             add_post, add_delete):
    messages = {
        'POST': f'Ошибка добавления в {add_post}',
        'DELETE': f'Ошибка исключения из {add_delete}'
    }
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        if is_shopping_list:
            list_users = recipe.shopping
        else:
            list_users = recipe.favorite
        is_current_user = list_users.filter(id=user.id).count()
        if not is_current_user and method == 'POST':
            list_users.add(user)
            return [RecipeMiniFields(recipe).data, status.HTTP_201_CREATED]
        elif is_current_user and method == 'DELETE':
            list_users.remove(user)
            return ['Удаление прошло успешно', status.HTTP_204_NO_CONTENT]
        raise Exception
    except Exception:
        return [messages[method], status.HTTP_400_BAD_REQUEST]
