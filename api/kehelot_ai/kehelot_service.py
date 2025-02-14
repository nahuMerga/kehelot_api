import os
import dotenv
from openai import OpenAI, RateLimitError, OpenAIError, AuthenticationError

# Load environment variables from .env
dotenv.load_dotenv()

# Retrieve API keys from the environment
API_KEYS = os.getenv("API_KEYS", "").split(",")

current_key_index = 0

def get_client():
    """Returns an OpenAI client with the current API key."""
    global current_key_index
    if current_key_index >= len(API_KEYS) or not API_KEYS[current_key_index]:
        return None  
    return OpenAI(
        base_url="https://api.aimlapi.com/v1", 
        api_key=API_KEYS[current_key_index]
    )

def generate_ai_response(message):
    global current_key_index

    while current_key_index < len(API_KEYS):
        client = get_client()
        if client is None:
            return "Service is temporarily unavailable. Please try again later."

        try:
            response = client.chat.completions.create(
                model="gpt-4o", 
                messages=[
                    {"role": "system", "content": "You are an AI assistant who knows everything."},
                    {"role": "user", "content": f"Reply in Amharic if only you know how to say it, Message: {message}"}
                ],
            )

            if response and hasattr(response, 'choices') and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "Could not generate a response at the moment."

        except RateLimitError:
            print(f"API key {API_KEYS[current_key_index]} hit the rate limit. Switching keys.")
            current_key_index += 1 

        except AuthenticationError:
            print(f"API key {API_KEYS[current_key_index]} is expired or invalid. Removing it.")
            del API_KEYS[current_key_index] 

        except OpenAIError:
            print(f"API key {API_KEYS[current_key_index]} encountered an issue. Removing it.")
            del API_KEYS[current_key_index]

        except Exception:
            return "Something went wrong. Please try again later."

    return "Service is temporarily unavailable. Please try again later."
