# LLM + RAG Function Execution API

This API uses an LLM and RAG to map user prompts to automation functions and generate Python code for execution.

## Installation

To set up and run this API:

1.  Clone the repository.
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
4.  Install dependencies: `pip install fastapi "uvicorn[standard]" sentence-transformers faiss-cpu psutil tf-keras`

## Usage

To start the API:

bash
uvicorn api:app --reload