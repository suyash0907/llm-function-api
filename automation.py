import os
import webbrowser
import psutil
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
def open_chrome():
    webbrowser.open("https://www.google.com")

def open_calculator():
    os.system("calc")

def open_notepad():
    if os.name == 'nt': 
        os.system("notepad.exe")
    else:
        print("Operating system not supported for opening Notepad.")

def get_cpu_usage():
    return psutil.cpu_percent()

def get_ram_usage():
    return psutil.virtual_memory().percent

def run_command(command):
    os.system(command)

function_metadata = {
    "open_chrome": "Opens the Google Chrome web browser.",
    "open_calculator": "Opens the Windows Calculator application.",
    "open_notepad": "Opens the Notepad text editor.",
    "get_cpu_usage": "Retrieves the current CPU usage as a percentage.",
    "get_ram_usage": "Retrieves the current RAM usage as a percentage.",
    "run_command": "Executes a command in the operating system's command line."
}
# Load the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  

# Generate embeddings for function descriptions
function_descriptions = list(function_metadata.values())
embeddings = model.encode(function_descriptions)
embedding_dimension = embeddings.shape[1]

# Create a FAISS index
index = faiss.IndexFlatL2(embedding_dimension)  
index.add(embeddings.astype('float32'))

# Store function names for retrieval
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

# Example usage:
query = "launch chrome"
result = get_function_and_generate_code(query)
print("Function:", result["function"])
print("Code:\n", result["code"])