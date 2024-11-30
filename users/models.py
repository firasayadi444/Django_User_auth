from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager  # Import the UserManager

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)  # Use EmailField for email validation
    password = models.CharField(max_length=120)

    username = None  # Explicitly remove the username field from AbstractUser

    USERNAME_FIELD = 'email'  # Email is now the unique identifier
    REQUIRED_FIELDS = []  # Remove the default required username field

    objects = UserManager()  # Attach the custom manager
