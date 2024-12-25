# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ml_model import load_model  # Import the function to load the model


@csrf_exempt
def predict_category(request):
    if request.method == 'POST':
        # Get the prompt from the POST request
        prompt = request.POST.get('prompt')

        if prompt is None:
            return JsonResponse({"error": "No prompt provided"}, status=400)

        # Load the model and vectorizer
        model, vectorizer = load_model()

        # Transform the new prompt using the vectorizer
        prompt_tfidf = vectorizer.transform([prompt])

        # Predict the category using the model
        predicted_category = model.predict(prompt_tfidf)

        # Return the predicted category as a JSON response
        return JsonResponse({"predicted_category": predicted_category[0]})

    return JsonResponse({"error": "Invalid request method"}, status=400)
