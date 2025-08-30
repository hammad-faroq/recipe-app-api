"""
The url gonna call the view which gonna call the serilizer --> model, and three mian view that dajngo rest freamwok
provides are Viewset, Apiview and Generic
"""

from rest_framework import viewsets,mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework.decorators import action#for the suctom action of image-upload
from rest_framework.response import Response#to give the resprective Status code with respose in the custom action


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """If we ewat fnctionality like same view but differnet serilizers we ust overide the funtion Get_serliazer_call to have this behaviiur"""
    """View for manage recipe APIs."""
    # serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()#creates the base query set
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    # def get_queryset(self):#GET /api/recipe/reci/ → list all recipes (uses get_queryset + RecipeSerializer)
    #     """TO override the get query set to get the recipes of the authenticated users only"""
    #     return Recipe.objects.filter(user=self.request.user).order_by('-id')#it will aslso give the tags associated with this recipe object

    def get_queryset(self):#the DRF calls the get_queryset, wehn we do the Get recipe/recipe, and we can apply filters into the getqueryser
        """Retrieve recipes for authenticated user."""
        tags = self.request.query_params.get('tags')#will give none is not passed endpint/?tags=["atga1",tag2]
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()
    

 #Both of thses methods are mentioned in theh django rest freamowrk documentation on how they wotks anad how to override them adn their ehaviour, waht pararmters they expetsa nd waht objecst they already have
    def get_serializer_class(self):
        #we have orveitde this to make sure taht the DEatal gonna work fo =r the other endpints, othersie only ONe serlizer athata we  have provoded gonna work
        """Return appropriate serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return serializers.RecipeDetailSerializer
    
    def perform_create(self, serializer):#POST /api/recipe/reci/ → create a recipe (uses perform_create + RecipeDetailSerializer by default, unless overridden)
        """Create a new recipe.To attach the recipe object with the user"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')#detail=True, gonna have the id with the url adn in the view
    def upload_image(self, request, pk=None):#the function for the custom action of image-upload
        """Upload an image to recipe."""#/api/recipe/recipes/{id}/upload-image/ (when detail is included)
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Refactoring the code 
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="assigned_only",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter by items assigned to recipes. 0 = all, 1 = only assigned.",
                enum=[0, 1],  # 👈 this makes it a dropdown in Swagger UI
            ),
        ]
    )
)
class BaseRecipeAttrViewset(mixins.DestroyModelMixin,mixins.UpdateModelMixin ,mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        print(assigned_only)
        queryset = self.queryset#if asssignonly=fasle, Give all the tags even the tags taht are not linkend to a recipe
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)#Return tags/ ingredinets are actually linkend to at least one recipe

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
    # def get_queryset(self):
    #     """Filter queryset to authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewset):#mixins with GenericViewSet can use the routers
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    
class IngredientViewSet(BaseRecipeAttrViewset):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()



