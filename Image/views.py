# Image/views.py



import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .models import GeneratedImage
from io import BytesIO
import base64
import time


from .serializers import GeneratedImageSerializer

# Your Hugging Face API URL and token
API_URL = "https://modelslab.com/api/v6/images/text2img"
API_TOKEN = "QLGhJU9PNw2Xc133dbBuwMGdye0u5y6Xr4VKuGLXNt8LfbAhZpoy072UpJuC"

def call_hugging_face_api(prompt, width=512, height=512):
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


def call_hugging_face_api_with_retries(prompt, width=512, height=512):
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

        # Wait for the specified delay before retrying
        time.sleep(DELAY_SECONDS)
        retry_count += 1

    return None  # Return None if the max retries are exceeded and no image is generated


@api_view(['POST'])
def generate_image(request):
    prompt = request.data.get('prompt')
    width = int(request.data.get('width', 512))
    height = int(request.data.get('height', 512))

    if not prompt:
        return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Call the API with retries
    img_data = call_hugging_face_api_with_retries(prompt, width, height)

    if img_data:
        return Response({
            'image_url': img_data['image_url'],
            'status': img_data['status']
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Image generation failed after multiple attempts"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
@api_view(['GET'])
def user_generated_images(request):
    images = GeneratedImage.objects.filter(user=request.user).order_by('-created_at')
    serializer = GeneratedImageSerializer(images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
