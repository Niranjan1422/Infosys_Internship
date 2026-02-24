import requests
import os

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = os.getenv("OLLAMA_MODEL", "phi3")

def generate_answer(query: str, context: str):

    if not context:
        return "No relevant context found."

    # 🔥 REDUCE CONTEXT SIZE (very important)
    trimmed_context = context[:800]

    prompt = f"""
You are an enterprise AI knowledge assistant.

User Query:
{query}

Context:
{trimmed_context}

Provide:
- Short Summary
- Key Insights
- Business Relevance
Keep answer under 200 words.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 300
                }
            },
            timeout=60  # stable timeout
        )

        if response.status_code == 200:
            return response.json().get("response", "No response generated.")

        return f"LLM Error: {response.text}"

    except requests.exceptions.Timeout:
        return "LLM timeout. Model overloaded."

    except Exception as e:
        return f"LLM unavailable: {str(e)}"