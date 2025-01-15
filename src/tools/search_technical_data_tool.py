import json
#from tools.tool import Tool
from sentence_transformers import SentenceTransformer, util
import json

from tools.tool import Tool

# Load your JSON file
with open('./data/data_test_python.json', 'r') as file:
    data = json.load(file)

# Extract the issues and their associated steps
issues = [scenario['issue'] for scenario in data['troubleshooting_scenarios']]

# Initialize a pre-trained model for generating embeddings
print("Loading embeddings model...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight and fast

# Generate embeddings for the issues
print("Generating embeddings for the issues...")
issue_embeddings = model.encode(issues, convert_to_tensor=True)

# Function to find the most relevant issue for a query
def find_matching_issue(query):
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, issue_embeddings)
    top_k = 3  # Number of top matches to retrieve
    top_k_indices = similarities.topk(top_k).indices[0].tolist()  # Get the indices of the top k similarity scores
    
    top_matches = []
    for idx in top_k_indices:
        top_matches.append({
            "issue": issues[idx],
            "steps": data['troubleshooting_scenarios'][idx]['steps'],
            "similarity_score": float(similarities[0, idx])  # Convert tensor to float
        })
    
    return json.dumps(top_matches)


def SearchTechnicalDataTool():
    return Tool(description="Search technical data in the knowledge base",
                name="search-technical-data",
                function=find_matching_issue)