"""
Database models user customized to login via email field not by nmae field (:.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
#self. normalize meail is a method which is in the parent calss already implemented, we are just implementing the create user and create super user methiod in the custom user model maanger class


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
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()#this line will tell the dkango to use the cusotm user model manager insted of the deafult one

    USERNAME_FIELD = 'email'#use email for the login/identification(by deaulft usename was)

#passowrd, lastlogin are automatically added when we inherit the abstractBaseuser, and is_superuser, groups & permissions
#are automcaticllay added when we inherit the PermissionMixin