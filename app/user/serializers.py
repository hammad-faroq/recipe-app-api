"""
Serilization for the APi View Json 
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """THis class gonna convert the correspond json into the user object whihc custom based user , overwtitting the method of the base class"""

    class Meta:
        model=get_user_model()
        fields=['email', 'password', "name"]
        extra_kwargs= {"password": {"write_only": True, 'min_length':5}}

    def create(self, validate_data):
        """Cretae the sucto based userr calss with the validated data provided"""
        return get_user_model().objects.create_user(**validate_data)