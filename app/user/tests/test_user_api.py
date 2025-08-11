"""
Tests fot the user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status 

CREATE_USER_URL= reverse("user:create")

#I will write 3 test cases to check this one functionality of creating a user successfully

def create_user(**params):
    """creating and reurn a new user"""
    return get_user_model().objects.create_user(**params)

class PublicUSerApiTest(TestCase):
    """TEsting the public features of the api"""

    def test_create_user_successful(self):
        """Testing thhat the user will be created successfully or not"""
        payload={
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        res= self.client.post(CREATE_USER_URL, payload)
        user= get_user_model().objects.get(email=payload["email"])#Requeest karna ka bad khud sa filer kar ka chekc akrna ha 
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_wtih_email_exist(self):
        """Testing  that If aleadty a user is created via email, It shuold not create the new user with same email, so it us=must thrpugh 404 NOt found"""
        payload={
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        create_user(**payload)#The **pararms Automatically will do the email= Payload["eamil"] like stuff, Magic (:
        res=self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    def test_password_too_short_error(self):
        """THis function or method will test that are we able to craete a user with very week password like oly 4 chars,TEsign this funtionality andi it hsuold through the error if we try to create the user with small passwrod"""
        payload={
            "email": "test@example.com",
            "password": "pw",
            "name": "Test Name",
        }
        res=self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist= get_user_model().objects.filter(email= payload['email']).exists()
        self.assertFalse(user_exist)