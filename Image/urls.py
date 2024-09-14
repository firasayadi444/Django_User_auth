from django.urls import path
from . import views
urlpatterns = [
    path('generate', views.generate_image, name='generate_image'),  # Endpoint for image generation
    path('user-images/', views.user_generated_images, name='user_generated_images'),  # Endpoint to get user images
]
