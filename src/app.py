from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_socketio import emit
from gemini_wrapper import GeminiWrapper
from anthropic_wrapper import AnthropicWrapper
from mistral_wrapper import MistralClient
from openai_wrapper import OpenAIClient
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# Initialize AI clients
gemini = GeminiWrapper()
anthropic = AnthropicWrapper()
mistral = MistralClient(config_file="../../keys.json")
openai = OpenAIClient(config_file="../../keys.json")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    # Broadcast human message
    emit('receive_message', data, broadcast=True)

    if data.get("sender") == "human":
        user_message = data.get("message", "")

        # AI Conversation Setup
        directions = ("You're speaking with other AIs trying to solve the original question. "
                      "Consider what Gemini, Mistral, Anthropic, and OpenAI have to say. "
                      "Keep responses short and build off the others. "
                      "If you have nothing to add, say very specifically 'CONFIRM: nothing to say'"
                      "A human may intervene to steer the conversation. "
                      "DO NOT EMULATE OTHER AIS RESPONSES, ONLY SPEAK IN THE FIRST PERSON.")

        total_message = f"Original Question: {user_message}\n"

        ai_models = [
            ("Gemini", gemini.send_request, "contents"),
            ("Anthropic", anthropic.send_request, "user_message"),
            ("Mistral", mistral.send_request, "prompt"),
            ("OpenAI", openai.send_request, "prompt"),
        ]

        # Loop through AI models
        for ai_name, ai_func, arg_name in ai_models:
            ai_response = ai_func(**{arg_name: total_message}, directions=f"You are {ai_name}, " + directions)

            if "CONFIRM: nothing to say" not in ai_response:
                total_message += f"{ai_name}: {ai_response}\n"
                emit('receive_message', {"message": f"{ai_name}: {ai_response}", "sender": "ai"}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
