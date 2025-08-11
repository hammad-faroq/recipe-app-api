"""
THis gonna create the api view for the creation of the user through api suing suctom absed useer class and geenric class
"""
from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
