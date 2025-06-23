import os
from groq import Groq
from ..core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

async def summarize_text(prompt: str) -> str:
    """
    Sends a prompt to the Groq API and returns the summarized text.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Could not summarize."

async def get_chat_response(message: str) -> str:
    """
    Sends a user's chat message to Groq and gets a response.
    """
    # This is a placeholder for your chat logic. 
    # You can customize the persona and instructions.
    prompt = f"You are a helpful assistant. Respond to the following message: {message}"
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful personal assistant."
                },
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "I am having trouble responding right now."