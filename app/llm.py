import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_maintenance_explanation(
    prediction: str,
    probability: float,
    risk_level: str,
    machine_data: dict,
    retrieved_knowledge: list,
):
    knowledge_text = "\n\n".join(
        f"Source: {item['source']}\n{item['content']}"
        for item in retrieved_knowledge
    )

    prompt = f"""
You are an industrial predictive-maintenance assistant.

Your job is to explain a machine-health prediction using the
provided machine data and maintenance knowledge.

IMPORTANT:
- Do not invent manufacturer limits.
- Do not claim that a prediction guarantees failure.
- Do not provide unsupported numerical operating limits.
- Treat the model prediction as a risk indicator.
- Base maintenance recommendations on the provided knowledge.
- Recommend inspection and appropriate corrective action.
- Keep the answer practical and concise.

Machine data:
{machine_data}

Model prediction:
Prediction: {prediction}
Failure probability: {probability}%
Risk level: {risk_level}

Retrieved maintenance knowledge:
{knowledge_text}

Provide:
1. A short explanation of why the machine is at this risk level.
2. The main parameters that should be investigated.
3. Recommended maintenance actions.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text