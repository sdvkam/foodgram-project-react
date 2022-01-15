from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import RecipeViewSet


router = DefaultRouter()
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
