"""
Database models user customized to login via email field not by nmae field (:.
"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

import uuid
import os #python library to interact with teh operating system
#self. normalize meail is a method which is in the parent calss already implemented, we are just implementing the create user and create super user methiod in the custom user model maanger class
def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image. Ensyre every image has unique idetifier uploads/recipe/550e8400-e29b-41d4-a716-446655440000.jpg"""
    ext = os.path.splitext(filename)[1]#splits the file name into (name, extension).
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)#valid path (uploads/recipe/<filename>).;#genereats the realtive path

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):#extra fileds if we deine the phone number as well in the cusmtom user mdoel, so the key will match the key in teh mdoel and sote it , other siwewe if not match throw an error, facy way to store more items in the cumtomuser modle 
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)#the set passowrd internally called the has function to store it 
        user.save(using=self._db)

        return user
    def create_superuser(self, email, password):
        """THis will be called when we use the manage,py to create the suer user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user




class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)#emal gonna have the build in email validation
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()#this line will tell the dkango to use the cusotm user model manager insted of the deafult one

    USERNAME_FIELD = 'email'#use email for the login/identification(by deaulft usename was)

#passowrd, lastlogin are automatically added when we inherit the abstractBaseuser, and is_superuser, groups & permissions
#are automcaticllay added when we inherit the PermissionMixin

class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')#Many 2 many Created a automatic join table between the two meodsl with the primary key as forign key of both tableswith on del cascade to del it from the recipe as well when we del the tag; Recipe has a many-2-many relationship with the tags
    # ingredients = models.ManyToManyField('Ingredient')# SAMKE LIKE THE TAGS
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)#db not gonna store the binary, it gonna store the path where  the actual image is uploaded like the static or mdeia folders i=on the server
    #image upload_to=recipe_image_file_path tells Django where inside your MEDIA_ROOT the file should be stored.
    def __str__(self):
        return self.title
    
class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name