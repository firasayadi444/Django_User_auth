# Image/views.py
import jwt
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .models import GeneratedImage
from users.models import User
from .serializers import GeneratedImageSerializer

from io import BytesIO
import base64
import time


from .serializers import GeneratedImageSerializer

# Your Hugging Face API URL and token
API_URL = "https://modelslab.com/api/v6/images/text2img"
API_TOKEN = "aFSFwozCywkcfPRDerqBvA9cC8bpbjdEg2POULMLzirP28YIpHC3AEBRvxQ8"

def call_hugging_face_api(prompt, width, height):
    payload = {
        "key": API_TOKEN,
        "model_id": "midjourney",
        "prompt": prompt,
        "negative_prompt": None,
        "width": width,
        "height": height,
        "samples": "1",
        "num_inference_steps": "30",
        "safety_checker": "no",
        "enhance_prompt": "yes",
        "seed": None,
        "guidance_scale": 7.5,
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": None,
        "lora_model": None,
        "tomesd": "yes",
        "use_karras_sigmas": "yes",
        "vae": None,
        "lora_strength": None,
        "scheduler": "DDIMScheduler",
        "webhook": None,
        "track_id": None
    }

    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    return None



# Maximum number of retries and delay time in seconds
MAX_RETRIES = 6
DELAY_SECONDS = 30


def call_hugging_face_api_with_retries(prompt, width, height):
    retry_count = 0

    while retry_count < MAX_RETRIES:
        # Call the Hugging Face API
        img_data = call_hugging_face_api(prompt, width, height)

        if img_data:
            rsp_status = img_data.get('status', '')
            image_urls = img_data.get('output', [])

            # If the API response is successful and an image URL is returned
            if rsp_status == 'success' and image_urls:
                return {
                    'status': rsp_status,
                    'image_url': image_urls[0]
                }
            else:
                print("status",rsp_status)


        # Wait for the specified delay before retrying
        time.sleep(DELAY_SECONDS)
        retry_count += 1

    return None  # Return None if the max retries are exceeded and no image is generated


@api_view(['POST'])
def generate_image(request):
    prompt = request.data.get('prompt')
    width = int(request.data.get('width'))
    height = int(request.data.get('height'))

    if not prompt:
        return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Call the API with retries

    img_data = call_hugging_face_api_with_retries(prompt,width,height)

    if img_data:
        return Response({
            'image_url': img_data['image_url'],
            'status': img_data['status']
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Image generation failed after multiple attempts"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def save_image(request):
    # Get the user ID from the request data
    user_id = request.data.get('user_id')
    print("User ID received:", user_id)  # Log the user ID for debugging

    # Fetch the user using the user ID
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

    # Get the image URL and prompt from the request data
    image_url = request.data.get('image_url')
    prompt = request.data.get('prompt')

    if not image_url or not prompt:
        return Response({"error": "Image URL and prompt are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Save the image and its associated data to the database
    generated_image = GeneratedImage.objects.create(
        user=user,
        prompt=prompt,
        image_url=image_url
    )
    generated_image.save()

    # Serialize and return the saved image data
    serializer = GeneratedImageSerializer(generated_image)

    return Response({
        'message': 'Image saved successfully',
        'image': serializer.data
    }, status=status.HTTP_201_CREATED)
@api_view(['GET'])
def user_images(request):
    # Get the user ID from the query parameters or request data
    user_id = request.GET.get('user_id')  # Change to GET if using query parameters
    print("userid", user_id)

    if not user_id:
        return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the user by ID
        user = User.objects.filter(id=user_id).first()
        print("user",user)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Fetch images that belong to the user
    images = GeneratedImage.objects.filter(user=user).order_by('-created_at')

    # Check if the user has any images
    if not images.exists():
        return Response({"error": "No images found for this user"}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the images and return the response
    serializer = GeneratedImageSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)