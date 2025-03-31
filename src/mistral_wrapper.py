import os
from mistralai import Mistral
import json

class MistralClient:
    """
    A class to handle interactions with the Mistral AI API.
    """
    
    def __init__(self, config_file='keys.json', model="mistral-large-latest"):
        """
        Initialize the MistralClient.
        
        Args:
            config_file (str): Path to the configuration file containing API keys
            model (str): Default model to use for completions
        """
        self.model = model
        self.client = self._initialize_client(config_file)
    
    def _initialize_client(self, config_file):
        """
        Initialize the Mistral client using API key from the config file.
        
        Args:
            config_file (str): Path to the configuration file
            
        Returns:
            Mistral: Initialized Mistral client or None if initialization fails
        """
        try:
            with open(config_file, 'r') as file:
                keys_data = json.load(file)
                api_key = keys_data.get('mistral_api_key')
                
                if not api_key:
                    raise ValueError(f"No 'mistral_api_key' found in {config_file}")
                    
                return Mistral(api_key=api_key)
                
        except FileNotFoundError:
            print(f"Error: {config_file} not found")
            return None
        except json.JSONDecodeError:
            print(f"Error: {config_file} is not valid JSON")
            return None
        except Exception as e:
            print(f"Error initializing model: {str(e)}")
            return None
    
    def send_chat_request(self, messages):
        """
        Send a chat completion request to the Mistral API.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            model (str, optional): Model to use for this request. If None, uses default model
            
        Returns:
            dict: API response or None if request fails
        """
        if not self.client:
            print("Error: Client not initialized")
            return None
        
        try:
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=messages
            )
            return chat_response
        except Exception as e:
            print(f"Error sending request: {str(e)}")
            return None
    
    def get_chat_response(self, prompt):
        """
        Get a simple chat response for a single prompt.
        
        Args:
            prompt (str): The user prompt
            model (str, optional): Model to use for this request
            
        Returns:
            str: Response content or error message
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.send_chat_request(messages, model)
        
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            return response.choices[0].message.content
        return "Error: Unable to get response"
    
    def set_model(self, model):
        """
        Set the default model for future requests.
        
        Args:
            model (str): Model identifier
        """
        self.model = model


# Example usage
if __name__ == "__main__":
    # Create client
    mistral_client = MistralClient()
    
    # Simple request
    response = mistral_client.get_chat_response("What is the best French cheese?")
    print(response)
    
    # More complex request with custom messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant with expertise in French cuisine."},
        {"role": "user", "content": "Tell me about the different regions of French cheese."}
    ]
    
    full_response = mistral_client.send_chat_request(messages)
    if full_response:
        print(full_response.choices[0].message.content)
