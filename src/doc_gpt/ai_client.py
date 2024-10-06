from openai import OpenAI, AzureOpenAI
import requests
import anthropic
import google.generativeai as genai

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
        
        print(f"Requesting content from model '{model_alias}' using provider '{provider}'")

        if provider == 'openai':
            return self._openai_request(messages, model_config)
        elif provider == 'azure-openai':
            return self._azure_openai_request(messages, model_config)
        elif provider == 'ollama':
            return self._ollama_request(messages, model_config)
        elif provider == 'claude':
            return self._claude_request(messages, model_config)
        elif provider == 'google-generativeai':
            return self._google_generativeai_request(messages, model_config)
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

    def _azure_openai_request(self, messages, model_config):
        if 'key' not in model_config or not model_config['key']:
            raise ValueError("API key not provided for Azure OpenAI")
        
        if 'api_base' not in model_config or not model_config['api_base']:
            raise ValueError("API base URL not provided for Azure OpenAI")
        
        if 'model_name' not in model_config or not model_config['model_name']:
            raise ValueError("Azure deployment name not provided for Azure OpenAI, please set it as 'model_name' in the configuration")

        azureOpenAIClient = AzureOpenAI(
            api_key=model_config['key'],
            api_version="2023-07-01-preview",
            azure_endpoint=model_config['api_base']
        )

        response = azureOpenAIClient.chat.completions.create(
            model=model_config['model_name'],
            messages=messages,
            stream=False
        )
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

    def _claude_request(self, messages, model_config):
        if 'key' not in model_config or not model_config['key']:
            raise ValueError("API key not provided for Claude")

        client = anthropic.Anthropic(api_key=model_config['key'])
        
        # Convert messages to Anthropic's format
        anthropic_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
        
        response = client.messages.create(
            model=model_config['model_name'],
            max_tokens=model_config.get('max_tokens', 1024),
            messages=anthropic_messages
        )
        return response.content

    def _google_generativeai_request(self, messages, model_config):
        if 'key' not in model_config or not model_config['key']:
            raise ValueError("API key not provided for Google Generative AI")

        genai.configure(api_key=model_config['key'])
        model = genai.GenerativeModel(model_config['model_name'])

        # Convert messages to a single prompt string
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

        response = model.generate_content(prompt)
        return response.text