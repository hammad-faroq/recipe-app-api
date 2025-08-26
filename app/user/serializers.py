"""
Serilization for the APi View Json , which converts the models into then json or can be jsut used to authenticate and validate
"""

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """THis class gonna convert the correspond json into the user object whihc custom based user , overwtitting the method of the base class"""

    class Meta:
        model=get_user_model()
        fields=['email', 'password', "name"]
        extra_kwargs= {"password": {"write_only": True, 'min_length':5}}#password wapis response ma na jya,test case

    def create(self, validate_data):#serilizers.modelserlilzers calls the deauflt create with no passord hash, override it to call the custom create user in custom user model
        """Cretae the sucto based userr calss with the validated data provided"""
        return get_user_model().objects.create_user(**validate_data)
    #it will serilize and return the json in the form {
  #"email": "test@example.com",
#  "name": "Test Name"
#} when called by generic.CreateAPiVIew and passed this class as a serilizer which uses the post to call create()

    
    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token.wWHihc is doing the input validation and authentication not creating the tokken, the token will be creatd in the view, we are just returning the validated object so tath it could be used i teh vbiews to create the token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):#attrs is a dict of validated fields which is automaticlaly get passed to this function after filed level validation secceed
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(#authenticate checks if the user exists already with thihs email
            request=self.context.get('request'),#optional pararmter to give some extra info aout which ip calinng from to limimt login attempts
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user#attach user object to the attrs dict, wihch will be used by the Token.objects.get_or_create(user=user).ObtainAuthToken class
        return attrs
    
"""
line 41
{
  "non_field_errors": [
    "Invalid credentials"
  ]
}"""
"""line 61 mixed wiht the view output is like
{ "token": "as9d8uasd9asud98a" }
"""
#DRF automatically converts the Python exception into a JSON response with HTTP 400 (Bad Request) status.
