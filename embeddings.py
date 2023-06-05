import os
import pandas as pd
from transformers import BertModel, BertTokenizer
import torch
import re
import numpy as np
from nltk.tokenize import PunktSentenceTokenizer, sent_tokenize

print("Loading BERT model and tokenizer...")
model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def chunk_sentences(text, sentences_per_chunk=3):
    # Split the text into sentences
    sentences = sent_tokenize(text)

    # Group sentences into chunks
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = ' '.join(sentences[i:i+sentences_per_chunk])
        while len(tokenizer.encode(chunk)) > 512:  # If the chunk is too large for BERT
            sentences_per_chunk -= 1  # Reduce the number of sentences per chunk
            chunk = ' '.join(sentences[i:i+sentences_per_chunk])  # And recreate the chunk
        chunks.append(chunk)

    return chunks

def encode_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    print("Embedding a new chunk...")
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
df['chunks'] = df['text'].apply(chunk_sentences)
df = df.explode('chunks')
df['embedding'] = df['chunks'].apply(encode_text)

print("Converting embeddings to lists and saving DataFrame...")
df['embedding'] = df['embedding'].apply(lambda x: x.tolist())
df.to_pickle('data.pkl')

print("Done!")
