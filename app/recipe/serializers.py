"""
Serilizers for the api, convets the model instances ,fields into python dicts

"""

from rest_framework import serializers

from core.models import Recipe, Tag

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serilizer for the recipe """
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "price", "link", "time_minutes",'tags']
        read_only_fields=['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                        user=auth_user,
                        **tag,
                    )
            recipe.tags.add(tag_obj)
    

    def create(self, validated_data):#for the posT OF THE viEW tAG
            """Create a recipe."""
            tags = validated_data.pop('tags', [])
            recipe = Recipe.objects.create(**validated_data)
            self._get_or_create_tags(tags, recipe)
            return recipe
    
    def update(self, instance, validated_data):# to make change the read only behaviour, this method is called when we do Put or Patch
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():#to set the validated data dict into the instanse attributes and save it
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view.Which is just the extension of the prevois calss and thats how we do it in the djano rest freamowrk"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
