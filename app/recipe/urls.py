"""
Urls mapping for the recipe APi
"""

from django.urls import (
    path,include
)

from rest_framework.routers import DefaultRouter
from recipe import views

#the router gonna create all the urls from the viewset we are proding according to the functionality available
#LIke CRUd (Get, Put, Post, Patch, Delete)

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'#need to set this variable for the reverse name mapping

urlpatterns = [
    path('', include(router.urls)),#include all the urls generaetd but the router 
]


"""This sinle line gonna create this vuiew
router.register('recipes', views.RecipeViewSet)
GET /api/recipe/reci/ → list

POST /api/recipe/reci/ → create

GET /api/recipe/reci/{id}/ → retrieve

PUT /api/recipe/reci/{id}/ → update

PATCH /api/recipe/reci/{id}/ → partial update

DELETE /api/recipe/reci/{id}/ → delete

"""