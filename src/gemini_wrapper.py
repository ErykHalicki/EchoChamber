# pip install -q -U google-genai
from google import genai
import json


class GeminiWrapper:
    def __init__(self):
        """
        Initialize the GeminiWrapper with an API key.
        """
        with open("../../keys.json", "r") as file:
            config = json.load(file)
        self.client = genai.Client(api_key=config["gemini_key"])

    def send_request_specific(self, model: str, contents: str) -> str:
        """
        Send a request to the Gemini API and return the response content.

        :param model: The model to use for the request.
        :param contents: The input content for the model.
        :return: The response content from the API.
        """
        response = self.client.models.generate_content(
            model=model, contents=contents
        )
        return response.text
    def send_request(self, contents: str, directions: str) -> str:
        """
        Send a request to the Gemini API and return the response content.

        :param contents: The input content for the model.
        :return: The response content from the API.
        """
        system_message = (directions)
        full_message = f"{system_message}\n\n{contents}"
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=full_message
        )
        return response.text


# Example usage
if __name__ == "__main__":
    wrapper = GeminiWrapper()
    response = wrapper.send_request(
        contents="Explain how AI works in a few words",
    )
    print(response)