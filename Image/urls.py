from django.urls import path
from . import views
urlpatterns = [
    path('generate/', views.generate_image, name='generate_image'),  # Endpoint for image generation
    path('save-image/', views.save_image, name='save_image'),
    path('user-images/', views.user_images, name='user_images'),

]
