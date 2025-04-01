# pip install anthropic

import json
import anthropic


class AnthropicWrapper:
    def __init__(self):
        """
        Initialize the AnthropicWrapper with an API key from keys.json.
        """
        with open("../../keys.json", "r") as file:
            config = json.load(file)
        self.client = anthropic.Anthropic(api_key=config["anthropic_key"])

    def send_request_specific(self, model: str, max_tokens: int, user_message: str) -> str:
        """
        Send a request to the Anthropic API and return the response content.

        :param model: The model to use for the request.
        :param max_tokens: The maximum number of tokens for the response.
        :param user_message: The message content from the user.
        :return: The response content from the API.
        """
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content

    def send_request(self, directions, user_message: str) -> str:
        """
        Send a request to the Anthropic API and return the response content.

        :param user_message: The message content from the user.
        :return: The response content from the API.
        """
        system_message = (
            "You are part of a conversation with Mistral, OpenAI, and Gemini. "
            "Please acknowledge their contributions in your response."
        )
        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1024,
            system=directions,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text


# Example usage
if __name__ == "__main__":
    wrapper = AnthropicWrapper()
    response = wrapper.send_request(
        user_message="Hello, Claude",
    )
    print(response)
