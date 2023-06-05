import os
import pandas as pd
from transformers import BertModel, BertTokenizer
import torch
import numpy as np

print("Loading BERT model and tokenizer...")
model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Function to chunk text
def chunk_text(text, chunk_size=512):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def encode_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        title = lines[0].strip()
        author = lines[1].strip()
        link = lines[2].strip()
        text = ' '.join(line.strip() for line in lines[3:])
        return title, author, link, text

print("Reading files...")
data = []
for file_name in os.listdir('docs'):
    print(f"Reading file: {file_name}")
    file_path = os.path.join('docs', file_name)
    title, author, link, text = read_file(file_path)
    data.append({'title': title, 'author': author, 'link': link, 'text': text})

print("Creating DataFrame...")
df = pd.DataFrame(data)

print("Chunking text and creating embeddings...")
df['chunks'] = df['text'].apply(chunk_text)
df = df.explode('chunks')
df['embedding'] = df['chunks'].apply(encode_text)

print("Converting embeddings to lists and saving DataFrame...")
df['embedding'] = df['embedding'].apply(lambda x: x.tolist())
df.to_pickle('data.pkl')

print("Done!")
