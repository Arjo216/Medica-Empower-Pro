import os
from google import genai
from dotenv import load_dotenv

# Load your environment variables
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

def list_gemini_models():
    # Initialize the standard Google GenAI client
    client = genai.Client(api_key=gemini_key)
    
    print("🔵 LIVE GEMINI MODELS:")
    try:
        # Fetch and iterate through the model generator
        for model in client.models.list():
            # Simply print the name of the model
            print(f" - {model.name}")
    except Exception as e:
        print(f"Error fetching Gemini models: {e}")

if __name__ == "__main__":
    list_gemini_models()