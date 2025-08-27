"""
The url gonna call the view which gonna call the serilizer --> model, and three mian view that dajngo rest freamwok
provides are Viewset, Apiview and Generic
"""

from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """If we ewat fnctionality like same view but differnet serilizers we ust overide the funtion Get_serliazer_call to have this behaviiur"""
    """View for manage recipe APIs."""
    # serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):#GET /api/recipe/reci/ → list all recipes (uses get_queryset + RecipeSerializer)
        """TO override the get query set to get the recipes of the authenticated users only"""
        return Recipe.objects.filter(user=self.request.user).order_by('-id')
    

 #Both of thses methods are mentioned in theh django rest freamowrk documentation on how they wotks anad how to override them adn their ehaviour, waht pararmters they expetsa nd waht objecst they already have
    def get_serializer_class(self):
        #we have orveitde this to make sure taht the DEatal gonna work fo =r the other endpints, othersie only ONe serlizer athata we  have provoded gonna work
        """Return appropriate serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return serializers.RecipeDetailSerializer
    
    def perform_create(self, serializer):#POST /api/recipe/reci/ → create a recipe (uses perform_create + RecipeDetailSerializer by default, unless overridden)
        """Create a new recipe.To attach the recipe object with the user"""
        serializer.save(user=self.request.user)

class TagViewSet(mixins.DestroyModelMixin,mixins.UpdateModelMixin ,mixins.ListModelMixin, viewsets.GenericViewSet):#mixins with GenericViewSet can use the routers
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


