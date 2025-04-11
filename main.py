import os
import time
import random
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set GROQ_API_KEY in the .env file.")

client = Groq(api_key=api_key)

def debate_bot():
    topic = input("Enter the debate topic: ")
    response_for_text = topic  # Initialize with the topic

    while True:
        # Argument 'For'
        response_for = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are in favor of the topic. Debate logically and convincingly, mock them, even if you have to be illogical sometimes with your examples.reply human like and in less than 2 lines"},
                {"role": "user", "content": response_for_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            top_p=1,
            stop=None
        )
        response_for_text = response_for.choices[0].message.content.strip()
        print(f"\n🟢 In Favor: {response_for_text}")

        time.sleep(5)  # Wait for 2 seconds before "Against"

        # Argument 'Against'
        response_against = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are against the topic. Provide strong counterarguments and dont let the topic deviate. reply human like and in less than 2 lines and carry satire."},
                {"role": "user", "content": response_for_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            top_p=1,
            stop=None
        )
        response_against_text = response_against.choices[0].message.content.strip()
        print(f"🔴 Against: {response_against_text}")

        time.sleep(random.randint(5, 7))  # Wait for 5-7 seconds before next "For"

        response_for_text = response_against_text  # Pass response to next iteration

if __name__ == "__main__":
    debate_bot()



