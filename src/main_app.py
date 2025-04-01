from gemini_wrapper import GeminiWrapper
from anthropic_wrapper import AnthropicWrapper
from mistral_wrapper import MistralClient
from openai_wrapper import OpenAIClient
import argparse

def main():
    # Initialize the wrappers
    gemini = GeminiWrapper()
    anthropic = AnthropicWrapper()
    mistral = MistralClient(config_file = "../../keys.json")
    openai = OpenAIClient(config_file = "../../keys.json")
    
    parser = argparse.ArgumentParser(description="Make AI models interact with each other.")
    parser.add_argument(
        "initial_message",
        type=str,
        help="The initial message to start the conversation between AI models.",
    )
    args = parser.parse_args()

    # Start the conversation
    message = args.initial_message
    print(f"Initial message: {message}")
    
    directions = ""
    total_message = ""
    # Gemini responds
    total_message += message
    gemini_response = gemini.send_request(contents=total_message, directions = directions)
    #print(f"Gemini:\n {gemini_response}")
    total_message += f"Gemini:\n {gemini_response}"

    # Anthropic responds to Gemini
    anthropic_response = anthropic.send_request(user_message=total_message, directions = directions)
    #print(f"Anthropic:\n {anthropic_response}")
    total_message += f"Anthropic:\n {anthropic_response}"
    print(total_message)

    # Mistral responds to Anthropic
    mistral_response = mistral.send_request(prompt=total_message, directions = directions)
    print(f"Mistral:\n {mistral_response}")
    total_message += f"Mistral:\n {mistral_response}"

    # OpenAI responds to Mistral
    openai_response = openai.send_request(prompt=total_message, directions = directions)
    print(f"OpenAI:\n {openai_response}")
    total_message += f"OpenAI:\n {openai_response}"

if __name__ == "__main__":
    main()
