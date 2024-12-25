import joblib
import os
import pandas as pd

def load_models():
    # Define paths for the model files
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Model-IA', 'random_forest_model.pkl')
    vectorizer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Model-IA', 'tfidf_vectorizer.pkl')
    newvect_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Model-IA', 'vect.pkl')
    newlabel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Model-IA', 'label.pkl')
    newrandommodel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Model-IA', 'randomodel.pkl')

    # Check if model files exist
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
    if not os.path.exists(newvect_path):
        raise FileNotFoundError(f"Vectorizer file not found: {newvect_path}")
    if not os.path.exists(newlabel_path):
        raise FileNotFoundError(f"Label file not found: {newlabel_path}")
    if not os.path.exists(newrandommodel_path):
        raise FileNotFoundError(f"Random model file not found: {newrandommodel_path}")

    # Load models and resources
    model = joblib.load(model_path)  # Old model (Random Forest)
    vectorizer = joblib.load(vectorizer_path)  # TF-IDF vectorizer
    new_vect = joblib.load(newvect_path)  # New vectorizer or model (if needed)
    new_labels = joblib.load(newlabel_path)  # New label encoder (if used)
    new_random_model = joblib.load(newrandommodel_path)  # New random model (used for generating prompts)

    return model, vectorizer, new_vect, new_labels, new_random_model
# Load the CSV dataset
def load_prompts_from_csv():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Model-IA', 'cleaned_prompts_and_categories.csv')

    df = pd.read_csv(csv_path)
    category_to_prompts = {}

    # Group prompts by category
    for _, row in df.iterrows():
        category = row['category']
        prompt = row['prompt']
        if category not in category_to_prompts:
            category_to_prompts[category] = []
        category_to_prompts[category].append(prompt)

    return category_to_prompts