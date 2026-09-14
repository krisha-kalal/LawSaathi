import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env file.")

client = genai.Client(api_key=api_key)

def generate_answer(prompt: str) -> str:
    config = types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=config
    )
    return response.text