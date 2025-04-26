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
    raise ValueError("API daal saale.")  # 🤣 keeping your original insult

client = Groq(api_key=api_key)

app = Flask(__name__)

# Global variable to hold the debate state
debate_state = {
    "current_side": "for",       # Starts with 'for'
    "last_response": "",
    "topic": ""                  # Store the debate topic separately
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_debate", methods=["POST"])
def start_debate():
    topic = request.json.get("topic")
    debate_state["last_response"] = topic
    debate_state["topic"] = topic
    debate_state["current_side"] = "for"  # Reset to 'for' when new debate starts
    return jsonify({"success": True})

@app.route("/get_next_response", methods=["GET"])
def get_next_response():
    current_side = debate_state["current_side"]
    last_response = debate_state["last_response"]
    topic = debate_state["topic"]

    # Build the system prompt properly using the topic
    if current_side == "for":
        system_prompt = (
            f"You are debating *in favor* of the following topic:\n\n"
            f"\"{topic}\"\n\n"
            "Debate logically and convincingly, mock the opponent if needed, "
            "stay focused on the topic, reply in less than 2 lines, "
            "and sound highly human-like with varied tone."
        )
        model = "llama-3.3-70b-versatile"
    else:
        system_prompt = (
            f"You are debating *against* the following topic:\n\n"
            f"\"{topic}\"\n\n"
            "Provide strong counterarguments to the opponent, do not let the debate drift, "
            "carry a confident tone with some satire, reply in less than 2 lines, "
            "and vary your tone naturally."
        )
        model = "llama-3.1-8b-instant"

    # Get response from Groq
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

    # Delay depending on side
    delay = 5 if current_side == "for" else random.randint(5, 7)

    return jsonify({
        "side": current_side,
        "response": new_response,
        "delay": delay
    })

if __name__ == "__main__":
    app.run(debug=True)
