# pip install -q -U google-genai
from google import genai
from google.genai import types
import json


class GeminiWrapper:
    def __init__(self):
        """
        Initialize the GeminiWrapper with an API key.
        """
        with open("../../keys.json", "r") as file:
            config = json.load(file)
        self.client = genai.Client(api_key=config["gemini_key"])

    def send_request(self, directions, contents: str) -> str:
        """
        Send a request to the Gemini API and return the response content.

        :param contents: The input content for the model.
        :return: The response content from the API.
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
            system_instruction=directions),
            contents=contents
        )        
        return response.text


# Example usage
if __name__ == "__main__":
    wrapper = GeminiWrapper()
    response = wrapper.send_request(
        contents="Explain how AI works in a few words",
    )
    print(response)
