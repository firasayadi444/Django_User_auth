from unittest import TestCase

import jwt
import pytest
import os
import django
from django.contrib.auth import get_user_model
import datetime

from rest_framework.test import APIClient

# Set the DJANGO_SETTINGS_MODULE to the correct settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'auth.settings'

# Initialize Django settings
django.setup()

# Import necessary Django modules
from django.urls import reverse
from rest_framework import status
from users.models import User  # Import User model
@pytest.mark.django_db
def test_register(client):
    """
    Test the user registration endpoint.
    """
    url = reverse('register')  # Update with your actual URL name if necessary
    data = {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'password123',

    }

    response = client.post(url, data, format='json')

    # Assert that the registration was successful
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert 'name' in response.data
    assert 'email' in response.data
    assert 'password' not in response.data

@pytest.mark.django_db
def test_login(client):
    """
    Test the user login endpoint.
    """
    # Create a user to login
    user = get_user_model().objects.create_user(
        email='testuser@example.com',
        password='password123'
    )

    url = reverse('login')  # Update with your actual login URL if necessary
    data = {
        'email': 'testuser@example.com',
        'password': 'password123'
    }

    response = client.post(url, data, format='json')

    # Assert that the login was successful and JWT token is returned
    assert response.status_code == status.HTTP_200_OK
    assert 'jwt' in response.data  # Ensure token is returned
    assert response.cookies.get('jwt') is not None  # Check that JWT is set in the cookies

@pytest.mark.django_db
def test_logout(client):
    """
    Test the user logout endpoint.
    """
    # Create a user to logout
    user = get_user_model().objects.create_user(
        email='testuser@example.com',
        password='password123'
    )

    # Log in to obtain the JWT token
    login_url = reverse('login')  # Update with your actual login URL
    login_data = {
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    login_response = client.post(login_url, login_data, format='json')
    jwt_token = login_response.data['jwt']
    client.cookies['jwt'] = jwt_token  # Set the cookie for subsequent requests

    # Logout
    logout_url = reverse('logout')  # Update with your actual logout URL
    response = client.post(logout_url)

    # Assert that the logout was successful
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'success'  # Message returned by your logout view
