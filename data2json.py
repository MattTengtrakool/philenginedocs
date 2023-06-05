import json
import random
import pandas as pd

# Load your data
df = pd.read_pickle('data.pkl')

# Create nodes
nodes = [{"id": title} for title in df['title'].unique()]

# Create links
links = []
for i, row1 in df.iterrows():
    for j, row2 in df.iterrows():
        if i != j:  # Exclude self-links
            # Generate a random semantic similarity value between 0 and 1
            similarity = random.random()
            links.append({"source": row1['title'], "target": row2['title'], "value": similarity})

# Save as JSON
with open('graph.json', 'w') as f:
    json.dump({"nodes": nodes, "links": links}, f)
