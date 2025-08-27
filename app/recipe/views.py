"""
The url gonna call the view which gonna call the serilizer --> model, and three mian view that dajngo rest freamwok
provides are Viewset, Apiview and Generic
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """If we ewat fnctionality like same view but differnet serilizers we ust overide the funtion Get_serliazer_call to have this behaviiur"""
    """View for manage recipe APIs."""
    # serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """TO override the get query set to get the recipes of the authenticated users only"""
        return Recipe.objects.filter(user=self.request.user).order_by('-id')
 #Both of thses methods are mentioned in theh django rest freamowrk documentation on how they wotks anad how to override them adn their ehaviour, waht pararmters they expetsa nd waht objecst they already have
    def get_serializer_class(self):
        """Return appropriate serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return serializers.RecipeDetailSerializer
    
    def perform_create(self, serializer):
        """Create a new recipe.To attach the recipe object with the user"""
        serializer.save(user=self.request.user)


