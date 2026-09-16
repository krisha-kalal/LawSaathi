import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from environment variables.")

client = genai.Client(api_key=api_key)

def generate_answer(prompt: str, retries: int = 3) -> str:
    config = types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )
    
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=config
            )
            return response.text
        except ServerError as e:
            if attempt == retries - 1:
                raise e
            time.sleep(2 * (attempt + 1))  # Exponential backoff