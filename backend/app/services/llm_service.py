import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are DocPilot, an AI document assistant.

Answer the user's question using ONLY the context below.
If the answer is not found in the context, say:
"I couldn't find that in the document."

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()
    return response.json()["response"]