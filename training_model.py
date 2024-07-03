from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd
from pymongo import MongoClient
import re
import torch
import pickle
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

def clean_text(text):
    # Remove special characters and convert text to lowercase
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    cleaned_text = cleaned_text.lower()
    return cleaned_text

def extract_first_word(text):
    # Extract the first word from the text
    match = re.match(r'\b\w+\b', text)
    if match:
        return match.group(0)
    return None

# Connect to MongoDB
client = MongoClient("mongodb+srv://user:passs@cluster0.*******.mongodb.net/")
db = client['disease_db']
disease_collection = db['disease']
link_collection = db['link']

# Fetch data from MongoDB
disease_data = disease_collection.find({})
link_data = link_collection.find({})

disease_data_list = list(disease_data)
disease_df = pd.DataFrame(disease_data_list)

link_data_list = list(link_data)
link_df = pd.DataFrame(link_data_list)

# Extract attributes and create label column
attribute_df = link_df['attribute'].apply(pd.Series)
attribute_df.columns = ['Rare disease', 'type']
attribute_df['label'] = attribute_df['type'] + ' ' + attribute_df['Rare disease']

link_df = link_df.drop(columns=['attribute']).join(attribute_df)

# Prepare data for training
label = []
description = []
# In the project we only used about 15 rabies because our system could not train more
for index, i in link_df.iterrows():
    i["Rare disease"]
    for index, j in disease_df[:15].iterrows():
        if i["Rare disease"] == j["Rare disease"]:
            label.append(i["label"])
            description.append(clean_text(i["description"]))

# Create samples for training model includes label and description 
sample_disease = pd.DataFrame({'label': label, 'description': description})
documents = [clean_text(i) for i in sample_disease["description"]]

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(sample_disease["label"])
sample_disease["description"] = [clean_text(i) for i in sample_disease["description"]]

# Split data into training and testing sets
train_texts, test_texts, train_labels, test_labels = train_test_split(
    documents, encoded_labels, test_size=0.2, random_state=42)

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(set(encoded_labels)))

# Prepare data for training
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=128)

train_inputs = torch.tensor(train_encodings['input_ids'])
train_masks = torch.tensor(train_encodings['attention_mask'])
train_labels = torch.tensor(train_labels).long()  # Convert labels to LongTensor

test_inputs = torch.tensor(test_encodings['input_ids'])
test_masks = torch.tensor(test_encodings['attention_mask'])
test_labels = torch.tensor(test_labels).long()  # Convert labels to LongTensor

batch_size = 128

# Create DataLoader for training and testing data
train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_sampler = RandomSampler(train_data)
train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

test_data = TensorDataset(test_inputs, test_masks, test_labels)
test_sampler = SequentialSampler(test_data)
test_dataloader = DataLoader(test_data, sampler=test_sampler, batch_size=batch_size)

# Initialize optimizer
optimizer = AdamW(model.parameters(), lr=2e-5)

# Train model
model.train()  # Set the model to training mode
for epoch in range(50):  # Train for 50 epochs
    for batch in train_dataloader:
        batch_inputs, batch_masks, batch_labels = batch  # Get inputs, masks, and labels for the batch
        optimizer.zero_grad()  # Clear the gradients of all optimized tensors
        outputs = model(batch_inputs, attention_mask=batch_masks, labels=batch_labels)  # Forward pass
        loss = outputs.loss  # Calculate the loss
        loss.backward()  # Backward pass to calculate gradients
        optimizer.step()  # Update model parameters

# Evaluate model
model.eval()  # Set the model to evaluation mode
predictions, true_labels = [], []

for batch in test_dataloader:
    batch_inputs, batch_masks, batch_labels = batch  # Get inputs, masks, and labels for the batch

    with torch.no_grad():  # Disable gradient calculation for evaluation
        outputs = model(batch_inputs, attention_mask=batch_masks)  # Forward pass
        logits = outputs.logits  # Get the logits

    predictions.extend(torch.argmax(logits, axis=1).tolist())  # Get the predicted labels
    true_labels.extend(batch_labels.tolist())  # Get the true labels

# Print the classification report
target_names = list(map(str, label_encoder.classes_))
print(classification_report(true_labels, predictions, target_names=target_names, labels=np.unique(true_labels)))

# Path to save and load model weights
model_save_path = '/path/web/models/model_weights.pth'
torch.save(model.state_dict(), model_save_path)

# Save tokenizer
tokenizer_save_path = '/path/web/models/tokenizer.pkl'
with open(tokenizer_save_path, 'wb') as f:
    pickle.dump(tokenizer, f)

# Save label_encoder
label_encoder_save_path = '/path/web/models/label_encoder.pkl'
with open(label_encoder_save_path, 'wb') as f:
    pickle.dump(label_encoder, f)
