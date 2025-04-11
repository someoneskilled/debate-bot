import os
import time
import random
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API daal saale.")

client = Groq(api_key=api_key)

app = Flask(__name__)

# Global variable to hold the debate state
debate_state = {
    "current_side": "for",  # Starts with 'for'
    "last_response": ""
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_debate", methods=["POST"])
def start_debate():
    topic = request.json.get("topic")
    debate_state["last_response"] = topic
    return jsonify({"success": True})

@app.route("/get_next_response", methods=["GET"])
def get_next_response():
    current_side = debate_state["current_side"]
    last_response = debate_state["last_response"]

    if current_side == "for":
        system_prompt = "You are in favor of the topic. Debate logically and convincingly, mock them, even if you have to be illogical sometimes. Reply human-like in less than 2 lines."
        model = "llama-3.3-70b-versatile"
    else:
        system_prompt = "You are against the topic. Provide strong counterarguments. Reply human-like in less than 2 lines with satire. DOnt let deviate from topic."
        model = "llama-3.1-8b-instant"

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": last_response}
        ],
        model=model,
        temperature=0.7,
        top_p=1,
        stop=None
    )

    new_response = response.choices[0].message.content.strip()

    # Update debate state
    debate_state["last_response"] = new_response
    debate_state["current_side"] = "against" if current_side == "for" else "for"

    delay = 5 if current_side == "for" else random.randint(5, 7)

    return jsonify({
        "side": current_side,
        "response": new_response,
        "delay": delay
    })

if __name__ == "__main__":
    app.run(debug=True)
