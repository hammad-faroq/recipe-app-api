"""
Serilizers for the api, convets the model instances ,fields into python dicts

"""

from rest_framework import serializers

from core.models import Recipe, Tag

class RecipeSerializer(serializers.ModelSerializer):
    """Serilizer for the recipe """

    class Meta:
        model = Recipe
        fields = ["id", "title", "price", "link", "time_minutes"]
        read_only_fields=['id']



class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view.Which is just the extension of the prevois calss and thats how we do it in the djano rest freamowrk"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
