import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are DocPilot, an AI assistant that answers questions about uploaded documents.

Rules:
1. Use ONLY the provided context.
2. Do not invent information.
3. If the answer is not clearly found in the context, say:
"I couldn't find that in the document."
4. Answer clearly and directly.
5. If the context includes multiple relevant points, organize them in bullet points.
6. Mention that the answer is based on the uploaded document.

Context:
{context}

User Question:
{question}

Answer:
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