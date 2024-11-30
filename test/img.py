import os
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from io import BytesIO
from PIL import Image as PILImage
import django
from rest_framework.test import APITestCase

from Image.models import GeneratedImage
from users.models import User
# Set the DJANGO_SETTINGS_MODULE to the correct settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'auth.settings'

# Initialize Django settings
django.setup()

# @pytest.mark.django_db
# def test_generate_image(client):
#     """
#     Test the 'generate_image' endpoint to ensure it generates an image successfully.
#     """
#     url = reverse('generate_image')
#     data = {'prompt': 'A sunset over mountains', 'width': 512, 'height': 512}
#     response = client.post(url, data)
#
#     assert response.status_code == status.HTTP_200_OK
#     assert 'image_url' in response.data


@pytest.mark.django_db
def test_save_image(client):
    """
    Test the 'save_image' endpoint to ensure an image is saved correctly.
    """
    user = User.objects.create_user(email='user@example.com', password='password123')

    url = reverse('save_image')
    data = {
        'user_id': user.id,
        'image_url': 'https://png.pngtree.com/thumb_back/fh260/background/20230511/pngtree-nature-background-sunset-wallpaer-with-beautiful-flower-farms-image_2592160.jpg',
        'prompt': 'A futuristic city'
    }
    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert 'image' in response.data



class ImageGenerationTests(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Authentication (Login)
        self.client.login(username='testuser', password='testpassword')

    @patch('image.views.call_hugging_face_api_with_retries')
    def test_generate_image(self, mock_generate):
        # Mock the API response for image generation
        mock_generate.return_value = {'status': 'success', 'image_url': 'http://example.com/image.png'}

        # Define the data for the POST request
        data = {
            'prompt': 'A beautiful sunset over the ocean',
            'width': 512,
            'height': 512
        }

        # Send the POST request
        response = self.client.post(reverse('generate_image'), data, format='json')

        # Assert the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image_url', response.data)
        self.assertEqual(response.data['status'], 'success')

    def test_save_image(self):
        # First generate an image URL (You can mock it too, as done above)
        image_url = 'http://example.com/image.png'
        prompt = 'A beautiful sunset over the ocean'

        data = {
            'user_id': self.user.id,
            'image_url': image_url,
            'prompt': prompt
        }

        # Save the generated image
        response = self.client.post(reverse('save_image'), data, format='json')

        # Check if the response is successful and image is saved
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', response.data)
        self.assertEqual(response.data['message'], 'Image saved successfully')

    def test_user_images(self):
        # Create a generated image for the user
        image = GeneratedImage.objects.create(
            user=self.user,
            prompt='A beautiful sunset over the ocean',
            image='path/to/image.png'
        )

        # Fetch the images for the user
        response = self.client.get(reverse('user_images'), {'user_id': self.user.id}, format='json')

        # Assert the response contains the image
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return 1 image
        self.assertEqual(response.data[0]['prompt'], 'A beautiful sunset over the ocean')
