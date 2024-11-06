from rest_framework import serializers
from .models import GeneratedImage

class GeneratedImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()  # Add the image field

    class Meta:
        model = GeneratedImage
        fields = ['id', 'user', 'prompt', 'image', 'created_at']