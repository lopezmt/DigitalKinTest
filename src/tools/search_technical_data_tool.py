import json
from openai import OpenAI
import numpy as np
from tools.tool import Tool

client = OpenAI()

def generate_embeddings(texts):
    try:
        response = client.embeddings.create(input = texts, model="text-embedding-3-small")
        return np.array([np.array(embeddingObj.embedding) for embeddingObj in response.data])
    except Exception as e:
        print(f"An error occurred while generating embeddings: {e}")
        return None
    
def initialize():
    print("Initializing the search technical data tool...")
    # Load your JSON file
    with open('./data/data_test_python.json', 'r') as file:
        data = json.load(file)

    # Extract the issues and their associated steps
    issues = [scenario['issue'] for scenario in data['troubleshooting_scenarios']]

    print("Generating embeddings for the issues...")
    issue_embeddings = generate_embeddings(issues)

    return data, issues, issue_embeddings

def compute_cosine_similarity(query_embedding, issue_embeddings):
    # Normalize embeddings
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    issues_norm = issue_embeddings / np.linalg.norm(issue_embeddings, axis=1, keepdims=True)
    # Compute cosine similarities
    return np.dot(issues_norm, query_norm)

# Initialize the tool
data, issues, issue_embeddings = initialize()

def find_matching_issue(query):
    if issue_embeddings is None:
        return "An error occurred while generating embeddings for the issues"
    query_embedding = generate_embeddings([query])
    if query_embedding is None:
        return "An error occurred while generating embeddings for the query"
    similarities = compute_cosine_similarity(query_embedding[0], issue_embeddings)

    # Get the indices of the top k similarity scores
    top_k = 3
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]  # Sort and reverse for descending order

    # Prepare the top matches
    top_matches = []
    for idx in top_k_indices:
        top_matches.append({
            "issue": issues[idx],
            "steps": data['troubleshooting_scenarios'][idx]['steps'],
            "similarity_score": similarities[idx]
        })

    return json.dumps(top_matches, indent=2)

# Tool wrapper
def SearchTechnicalDataTool():
    return Tool(
        description="Search technical data in the knowledge base",
        name="search-technical-data",
        function=find_matching_issue
    )