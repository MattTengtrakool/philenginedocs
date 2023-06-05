from flask import Flask, request, render_template, session, jsonify, redirect, url_for
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from transformers import BertModel, BertTokenizer

app = Flask(__name__, static_folder='static')
app.secret_key = 'asdfasdfasdfas'

model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

df = pd.read_pickle('data.pkl')

def encode_query(query):
    inputs = tokenizer(query, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        session['query'] = query
        return redirect(url_for('results'))
    return render_template('index.html')

@app.route('/results', methods=['GET'])
def results():
    documents = []
    page = request.args.get('page', 1, type=int)
    per_page = 5
    query = session.get('query', '')

    if query:
        query_embedding = encode_query(query)

        similarities = cosine_similarity(query_embedding.reshape(1, -1), np.vstack(df['embedding'].values))

        indices = similarities[0].argsort()[-per_page*page:][::-1]
        documents = df.iloc[indices].to_dict(orient='records')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(documents)

    return render_template('results.html', documents=documents, page=page, query=query)

if __name__ == '__main__':
    app.run(debug=True)
