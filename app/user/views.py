"""
THis gonna create the api view for the creation of the user through api suing suctom absed useer class and geenric class
"""
from rest_framework import generics
from user.serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer



class CreateTokenView(ObtainAuthToken):#this is the lcasss of the rest freamworj which we gonna inhetit to implement the tokken authentication and it used the serlilization instead of the temaplest int eh django
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
