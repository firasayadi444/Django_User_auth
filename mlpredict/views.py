from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import request
from rest_framework.decorators import api_view
import random

from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

from Image.models import GeneratedImage
from users.models import User
from .models import load_models, load_prompts_from_csv  # Assuming load_prompts_from_csv is available

@csrf_exempt
@api_view(['POST'])
def predict_category(request):
    # Get the 'prompt' data from the request
    # prompt = request.data.get('prompt')
    prompt = lastprompt(request)
    print(prompt)

    # Check if prompt is provided
    if not prompt:
        return JsonResponse({"error": "No prompt provided"}, status=400)

    try:
        # Load all the models and vectorizers
        model, vectorizer, new_vect, new_labels, new_random_model = load_models()

        # If any model or vectorizer is None, return an error
        if model is None or vectorizer is None or new_random_model is None:
            return JsonResponse({"error": "One or more models could not be loaded."}, status=500)

        # Vectorize the prompt using the TF-IDF vectorizer
        prompt_tfidf = vectorizer.transform([prompt])

        # Predict the category using the old random forest model
        predicted_category = model.predict(prompt_tfidf)[0]

        # Load prompts from the CSV dataset
        category_to_prompts = load_prompts_from_csv()

        # If the predicted category is not found, select random prompts from all categories
        if predicted_category not in category_to_prompts:
            random_prompts = random.sample(
                [item for sublist in category_to_prompts.values() for item in sublist], 5
            )
            return JsonResponse({
                "error": f"Category '{predicted_category}' not found in dataset. Displaying random prompts.",
                "random_prompts": random_prompts
            })

        # Select random prompts from the predicted category
        prompts = random.sample(category_to_prompts[predicted_category], 5)

        # Return the prediction and generated prompts as a JSON response
        return JsonResponse({
            "predicted_category": predicted_category,
            "generated_prompts": prompts
        })

    except FileNotFoundError as e:
        # Specific error handling if any model files are missing
        return JsonResponse({"error": f"Model file not found: {str(e)}"}, status=500)

    except Exception as e:
        # General error handling for any unexpected issues
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


JWT_SECRET = 'secret'  # Replace with `os.getenv('JWT_SECRET')` in production

def get_user_from_token(request):
    """
    A helper function to decode the JWT token and retrieve the user.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed('Unauthenticated!')

    token = auth_header.split(' ')[1]  # Extract the token from 'Bearer <token>'

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = decoded_token.get('id')

        if not user_id:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=user_id).first()
        if not user:
            raise AuthenticationFailed('User not found!')

        return user
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired!')
    except jwt.DecodeError:
        raise AuthenticationFailed('Invalid token!')


def lastprompt(request):
    """
    View to retrieve the last prompt of the authenticated user.
    """
    try:
        user = get_user_from_token(request)

        # Fetch the latest prompt for the user (assuming a Prompt model exists)
        last_generated_image = GeneratedImage.objects.filter(user=user).order_by('-created_at').first()

        if not last_generated_image:
            return None



        return last_generated_image.prompt
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)
    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred", "details": str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
def getlastprompt(request):
    """
    View to retrieve the last prompt of the authenticated user.
    """
    try:
        user = get_user_from_token(request)

        # Fetch the latest prompt for the user (assuming a Prompt model exists)
        last_generated_image = GeneratedImage.objects.filter(user=user).order_by('-created_at').first()

        if not last_generated_image:
            return JsonResponse({"message": "No prompts found for this user"}, status=404)



        return JsonResponse({"last_prompt": last_generated_image.prompt}, status=200)
    except AuthenticationFailed as e:
        return JsonResponse({"error": str(e)}, status=401)
    except Exception as e:
        return JsonResponse({"error": "An unexpected error occurred", "details": str(e)}, status=500)


