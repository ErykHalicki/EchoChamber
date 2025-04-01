import json
from openai import OpenAI

class OpenAIClient:
    """
    A class to handle interactions with the OpenAI API.
    """
    
    def __init__(self, config_file='keys.json', model="gpt-4o"):
        """
        Initialize the OpenAIClient.
        
        Args:
            config_file (str): Path to the configuration file containing API keys
            model (str): Default model to use for completions
        """
        self.model = model
        self.client = self._initialize_client(config_file)
    
    def _initialize_client(self, config_file):
        """
        Initialize the OpenAI client using API key from the config file.
        
        Args:
            config_file (str): Path to the configuration file
            
        Returns:
            OpenAI: Initialized OpenAI client or None if initialization fails
        """
        try:
            with open(config_file, 'r') as file:
                keys_data = json.load(file)

                api_key = keys_data.get('openai_key')
                
                if not api_key:
                    raise ValueError(f"No 'openai_api_key' found in {config_file}")
                    
                return OpenAI(api_key=api_key)
                
        except FileNotFoundError:
            print(f"Error: {config_file} not found")
            return None
        except json.JSONDecodeError:
            print(f"Error: {config_file} is not valid JSON")
            return None
        except Exception as e:
            print(f"Error initializing model: {str(e)}")
            return None
    
    def send_chat_request(self, directions, prompt):
        """
        Send a chat completion request to the OpenAI API.
        
        Args:
            directions (str): System instructions/directions
            prompt (str): User prompt
            model (str, optional): Model to use for this request. If None, uses default model
            
        Returns:
            dict: API response or None if request fails
        """
        if not self.client:
            print("Error: Client not initialized")
            return None
        
        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=directions,
                input=prompt
            )
            return response.output_text
        except Exception as e:
            print(f"Error sending request: {str(e)}")
            return None
    
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
    openai_client = OpenAIClient(config_file = "../../keys.json")
    
    # Using responses API
    pirate_response = openai_client.send_chat_request(
        directions="Talk like donkey from shrek.",
        prompt="Are semicolons optional in JavaScript?"
    )
    print(pirate_response)
    
