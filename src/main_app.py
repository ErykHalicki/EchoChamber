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
    
    directions = "youre speaking with other AI's trying to solve the original question, take into account what Gemini, MIstral, Anthropic and OpeAI have to say, keep youre responses short and build off of the others. If you have nothing to add, say THATS WHAT I WAS GOING TO SAY!!!!. Also, a human will intervene intermitenetly to steer the conversation. DO NOT EMULATE OTHER AIS RESPONSES, ONLY SPEAK IN THE FIRST PERSON. Feel free to call out the bullshit of the other AI's they can halluciante sometimes."
    total_message = "Original Question: "
    # Gemini responds
    total_message += message
    total_message += "\n"
    for i in range(3):
        gemini_response = gemini.send_request(contents=total_message, directions = "You are GEMINI, " +directions)
        #print(f"Gemini:\n {gemini_response}")
        total_message += f"Gemini:\n {gemini_response}\n"
    
       # Anthropic responds to Gemini
        anthropic_response = anthropic.send_request(user_message=total_message, directions = "You are ANTHROPIC," +directions)
        #print(f"Anthropic:\n {anthropic_response}")
        total_message += f"Anthropic:\n {anthropic_response}\n"

        # Mistral responds to Anthropic
        mistral_response = mistral.send_request(prompt=total_message, directions = "You are MISTRAL, " +directions)
        #print(f"Mistral:\n {mistral_response}")
        total_message += f"Mistral:\n {mistral_response}\n"

        # OpenAI responds to Mistral
        openai_response = openai.send_request(prompt=total_message, directions = "You are OPENAI, " + directions)
        #print(f"OpenAI:\n {openai_response}")
        total_message += f"OpenAI:\n {openai_response}\n"
        print(total_message)
        user_input = input("\n Participate in the conversation: ")
        total_message += f"Human: {user_input}\n"


    

if __name__ == "__main__":
    main()
