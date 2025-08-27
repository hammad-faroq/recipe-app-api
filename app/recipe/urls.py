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

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
