from django.db import models
from users.models import User  # Import the custom User model if you're using one

class GeneratedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links the image to the user
    prompt = models.TextField()  # Stores the text prompt used to generate the image
    image_url = models.URLField()  # URL to the generated image
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the image was created

    def __str__(self):
        return f'Image generated for {self.user.username} on {self.created_at}'
