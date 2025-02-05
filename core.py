import json
import os
from ai_bridge.providers import OpenAIProvider, DeepSeekProvider, GoogleProvider
from ai_bridge.providers.base_provider import ProviderStrategy

class AIBridge:
    def __init__(self, config_file=None):
        self.providers = {}
        self.load_providers(config_file)

    def load_providers(self, config_file=None):
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)

            # 从配置文件动态加载 API 密钥
            for provider_name, provider_config in config.get('providers', {}).items():
                api_key = provider_config.get('api_key')
                self.register_provider(provider_name, api_key)

    def register_provider(self, provider_name: str, api_key: str):
        """
        动态注册提供商及其 API 密钥
        """
        if provider_name == "openai":
            self.providers["openai"] = OpenAIProvider(api_key)
        elif provider_name == "deepseek":
            self.providers["deepseek"] = DeepSeekProvider(api_key)
        elif provider_name == "google":
            self.providers["google"] = GoogleProvider(api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")

    async def ask(self, provider: str, prompt: str, **kwargs):
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not registered.")
        return await self.providers[provider].ask(prompt, **kwargs)