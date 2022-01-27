from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngedientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngedientViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
