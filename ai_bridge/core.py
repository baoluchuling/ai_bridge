import json
import os
from ai_bridge.providers import OpenAIProvider, SiliconflowProvider, GoogleProvider
from ai_bridge.providers.aliyun import AliyunProvider
from ai_bridge.providers.base_provider import ProviderStrategy
from ai_bridge.responses.ai_response_formatter import AIResponseFormatter
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AIBridge:
    def __init__(self):
        self.providerList: dict  = {}
        self.load_providers()

    def load_providers(self):

        providers_config = os.getenv("AI_BRIDGE_PROVIDERS")

        if not providers_config:
            print("⚠️  No provider configuration found in environment variables.")
            return
        
        try:
            config = json.loads(providers_config)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in AI_BRIDGE_PROVIDERS")

        for provider_name, providers_config in config.items():
            deployer = providers_config.get("deployer")
            api_key = providers_config.get("api_key")
            base_url = providers_config.get("base_url")
            base_model = providers_config.get("base_model")
            if api_key and base_url and base_model:
                self.register_provider(provider_name, deployer, api_key, base_url, base_model)

    def register_provider(self, provider_name: str, deployer: str, api_key: str, base_url: str, base_model: str):
        
        deployer_classes = {
            "openai": OpenAIProvider,
            "siliconflow": SiliconflowProvider,
            "google": GoogleProvider,
            "aliyun": AliyunProvider
        }

        if deployer in deployer_classes:
            self.providerList[provider_name] = deployer_classes[deployer](provider_name, api_key, base_url, base_model)
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")

    async def ask_single(self, provider: str, prompt: str, model = None, format: str = "text"):
        if provider not in self.providerList:
            raise ValueError(f"Provider {provider} not registered.")
        provider: ProviderStrategy = self.providerList[provider]
        response = await provider.ask_single(model, prompt, format)
        return AIResponseFormatter.format(provider.deployer, response)
    
    async def ask(self, provider: str, messages: list[dict], model = None, format: str = "text"):
        if provider not in self.providerList:
            raise ValueError(f"Provider {provider} not registered.")
        provider: ProviderStrategy = self.providerList[provider]
        response = await provider.ask(model, messages, format)
        return AIResponseFormatter.format(provider.deployer, response)