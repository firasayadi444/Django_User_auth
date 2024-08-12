# Image/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import GeneratedImage


def generate_image_view(request):
    # Example view for generating an image
    # Replace with actual image generation logic
    prompt = request.GET.get('prompt', 'Default prompt')
    # Generate the image URL (dummy URL here)
    image_url = 'http://example.com/generated_image.jpg'

    # Save to the database
    generated_image = GeneratedImage.objects.create(
        user=request.user,  # Assume user is authenticated
        prompt=prompt,
        image_url=image_url
    )

    return JsonResponse({'image_url': image_url})
