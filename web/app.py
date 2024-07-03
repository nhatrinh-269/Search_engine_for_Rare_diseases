from flask import Flask, render_template, request
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch
import pickle
from transformers import BertForSequenceClassification
from spellchecker import SpellChecker
import language_tool_python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('punkt')

def calculate_similarity(reference_text, target_texts):
    # Initialize the vectorizer and transform the texts into TF-IDF vectors
    vectorizer = TfidfVectorizer().fit_transform([reference_text] + target_texts)
    vectors = vectorizer.toarray()
    
    # Calculate cosine similarity between reference_text and each target_text
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    return cosine_similarities

def correct_spelling(text):
    # Initialize spell checker
    spell = SpellChecker()
    
    # Split words and correct spelling
    words = text.split()
    corrected_words = []
    for word in words:
        corrected_word = spell.correction(word)
        if corrected_word is None:
            corrected_word = word
        corrected_words.append(corrected_word)
    
    # Join corrected words back into a single string
    corrected_text = ' '.join(corrected_words)
    return corrected_text

def classify_text(text, model, tokenizer, label_encoder):
    model.eval()
    # Tokenize the input text
    encodings = tokenizer(text, truncation=True, padding=True, max_length=128, return_tensors='pt')
    input_ids = encodings['input_ids']
    attention_mask = encodings['attention_mask']

    with torch.no_grad():
        # Get model predictions
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
    
    # Determine the predicted label
    predicted_label_id = torch.argmax(logits, axis=1).item()
    predicted_label = label_encoder.inverse_transform([predicted_label_id])[0]
    return predicted_label

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://user:passs@cluster0.*******.mongodb.net/")
db = client['disease_db']
disease_collection = db['disease']
link_collection = db['link']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Paths to saved models and encoders
    tokenizer_save_path = '/path/web/models/tokenizer.pkl'
    label_encoder_save_path = '/path/web/models/label_encoder.pkl'
    model_save_path = '/path/web/models/model_weights.pth'
    
    # Load tokenizer
    with open(tokenizer_save_path, 'rb') as f:
        tokenizer = pickle.load(f)
        
    # Load label encoder
    with open(label_encoder_save_path, 'rb') as f:
        label_encoder = pickle.load(f)
        
    # Load model and weights
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label_encoder.classes_))

    # Map the model to CPU
    model.load_state_dict(torch.load(model_save_path, map_location=torch.device('cpu')))
    model.eval()

    # Get user input and correct spelling
    free_text = correct_spelling(request.form.get('disease'))
    predicted_label = classify_text(free_text, model, tokenizer, label_encoder)

    type_disease = predicted_label.split(" ")[0]
    disease= predicted_label[len(type_disease):].strip()

    # Query MongoDB for matching documents
    results = link_collection.find({
        "$and": [
            {"attribute.Rare disease": disease},
            {"attribute.type": type_disease}
        ],
    }, {
        "_id": 0
    })

    # Query MongoDB for disease description
    description_result = disease_collection.find({"Rare disease": disease})
    diseases = list(results)
    description = list(description_result)
    
    print(disease)

    if not diseases or not description:
        no_data_message = "No data found."
        return render_template('index.html', no_data_message=no_data_message)
    else:
        description = description[-1]["attribute"].get(f"{type_disease}", "No description available")
        
        # Extract descriptions from the diseases list for similarity comparison
        target_texts = [d['description'] for d in diseases]
        
        # Calculate similarity scores
        similarities = calculate_similarity(free_text, target_texts)
        
        # Add similarity scores to disease list
        for i, score in enumerate(similarities):
            diseases[i]['similarity_score'] = score
        
        # Sort diseases by similarity score
        diseases_sorted = sorted(diseases, key=lambda x: x['similarity_score'], reverse=True)

        return render_template('index.html', results=diseases_sorted, query=f"{type_disease} of {disease}", desciption=f"{type_disease} of {disease}: {description}")

if __name__ == '__main__':
    app.run(debug=True)
