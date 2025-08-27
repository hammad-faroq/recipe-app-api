"""
THis gonna create the api view for the creation of the user through api suing suctom absed useer class and geenric class
"""
from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)
#this class which we have inherited implements GEt, Put and PAtch
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]#This line expects tokken in header like ;Authorization: Token as9d8uasd9asud98a
    permission_classes = [permissions.IsAuthenticated]#to specify the persmion on the autenticateed user, just one inthis case (it must be authenticated)

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


#implements the post automatically, TO create a new user
class CreateUserView(generics.CreateAPIView):#The View returns a Response(serializer.errors, status=400) automatically if invalid
    """Create a new user in the system."""
    serializer_class = UserSerializer


#Implenets the post automatically, to create a tokken for that user 
#obtain auth tokken calls the .is_valid which we have implented to check taht whttee the user exist wth this email or not?

class CreateTokenView(ObtainAuthToken):#obtain Auth tokken does this ; after post to the serlilizerwe have provided ;Token.objects.get_or_create(user=user).
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

"""
api_settings.DEFAULT_RENDERER_CLASSES measn
[
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]
This means:

If you call the API via Postman → you get JSON.

If you call it in a browser → you get DRF’s nice browsable API UI.

"""


