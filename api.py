from fastapi import FastAPI, HTTPException
from typing import Dict
import automation
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = FastAPI()

# Load the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function Metadata (same as before)
function_metadata = {
    "open_chrome": "Opens the Google Chrome web browser.",
    "open_calculator": "Opens the Windows Calculator application.",
    "open_notepad": "Opens the Notepad text editor.",
    "get_cpu_usage": "Retrieves the current CPU usage as a percentage.",
    "get_ram_usage": "Retrieves the current RAM usage as a percentage.",
    "run_command": "Executes a command in the operating system's command line."
}

# Generate embeddings (same as before)
function_descriptions = list(function_metadata.values())
embeddings = model.encode(function_descriptions)
embedding_dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dimension)
index.add(embeddings.astype('float32'))
function_names = list(function_metadata.keys())

def generate_code(function_name):
    code = f"""
from automation_functions import {function_name}

def main():
    try:
        {function_name}()
        print("{function_name} executed successfully.")
    except Exception as e:
        print(f"Error executing function: {{e}}")

if __name__ == "__main__":
    main()
"""
    return code

def get_function_and_generate_code(query):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding.astype('float32'), k=1)
    closest_index = I[0][0]
    function_name = function_names[closest_index]
    code = generate_code(function_name)
    return {"function": function_name, "code": code}

@app.post("/execute")
async def execute_prompt(request: Dict[str, str]) -> Dict[str, str]:
    try:
        prompt = request["prompt"]
        result = get_function_and_generate_code(prompt)
        return result
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing 'prompt' in request")
