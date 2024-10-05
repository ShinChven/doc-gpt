from openai import OpenAI
import requests

class AIClient:
    def __init__(self, config):
        self.config = config

    def request(self, messages, model_alias=None):
        if not model_alias:
            model_alias = self.config.get('default_model')
            if not model_alias:
                raise ValueError("No default model specified in configuration")
        
        if model_alias not in self.config.get('models', {}):
            raise ValueError(f"Model alias '{model_alias}' not found in configuration")
        
        model_config = self.config['models'][model_alias]
        provider = model_config.get('provider')
        
        if not provider:
            raise ValueError(f"Provider not specified for model alias '{model_alias}'")
        
        if provider == 'openai':
            return self._openai_request(messages, model_config)
        elif provider == 'ollama':
            return self._ollama_request(messages, model_config)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _openai_request(self, messages, model_config):
        if 'key' not in model_config or not model_config['key']:
            raise ValueError("API key not provided for OpenAI")
        
        api_base = model_config.get('api_base')
        if not api_base:
            api_base = 'https://api.openai.com/v1'

        openAIClient = OpenAI(api_key=model_config['key'], base_url=api_base)
        response = openAIClient.chat.completions.create(
                model=model_config['model_name'],
                messages=messages,
                stream=False)
        return response.choices[0].message.content

    def _ollama_request(self, messages, model_config):
        api_base = model_config.get('api_base')
        if not api_base:
            api_base = 'http://localhost:11434'
        api_base += '/api/chat'

        response = requests.post(
            api_base,
            json={
                "model": model_config['model_name'],
                "messages": messages,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()['message']['content']