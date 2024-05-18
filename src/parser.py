from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("No API key found. Please set the API_KEY environment variable.")

print(api_key)