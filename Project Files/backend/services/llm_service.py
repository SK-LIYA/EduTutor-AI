# services/llm_service.py

import os
import json
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

load_dotenv()

# Initialize IBM Watsonx LLM
llm = WatsonxLLM(
    model_id=os.getenv("WATSONX_MODEL_ID"),
    url=os.getenv("WATSONX_ENDPOINT"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    apikey=os.getenv("WATSONX_API_KEY")  # ✅ Correct param
)

def generate_mcq_from_context(context: str, topic: str, num_questions: int):
    prompt = f"""
    You are an AI tutor. Based on the following class material, generate {num_questions} multiple-choice questions (MCQs) on the topic "{topic}".
    Provide output in valid JSON format like:
    [
      {{
        "question": "What is ...?",
        "options": ["A", "B", "C", "D"],
        "answer": "B"
      }},
      ...
    ]

    Class Material:
    {context}
    """

    try:
        response = llm.invoke(prompt)
        return json.loads(response)
    except Exception as e:
        print("❌ Failed to parse LLM response:", e)
        return [{"question": "⚠️ Error parsing response.", "options": [], "answer": ""}]
