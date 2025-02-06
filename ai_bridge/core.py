import json
import os
from ai_bridge.providers import OpenAIProvider, DeepSeekProvider, GoogleProvider
from ai_bridge.responses.ai_response_formatter import AIResponseFormatter

class AIBridge:
    def __init__(self):
        self.providers = {}
        self.load_providers()

    def load_providers(self):
        """
        从环境变量 `AI_BRIDGE_PROVIDERS` 加载提供商及其 API 密钥。
        格式: {"openai": {"api_key": "sk-xxx"}, "deepseek": {"api_key": "sk-yyy"}}
        """
        providers_config = os.getenv("AI_BRIDGE_PROVIDERS")

        if not providers_config:
            print("⚠️  No provider configuration found in environment variables.")
            return
        
        try:
            config = json.loads(providers_config)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in AI_BRIDGE_PROVIDERS")

        for provider_name, provider_config in config.items():
            api_key = provider_config.get("api_key")
            base_url = provider_config.get("base_url")
            if api_key and base_url:
                self.register_provider(provider_name, api_key, base_url)

    def register_provider(self, provider_name: str, api_key: str, base_url: str):
        """
        动态注册提供商及其 API 密钥
        """
        provider_classes = {
            "openai": OpenAIProvider,
            "deepseek": DeepSeekProvider,
            "google": GoogleProvider
        }

        if provider_name in provider_classes:
            self.providers[provider_name] = provider_classes[provider_name](api_key, base_url)
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")

    async def ask(self, provider: str, prompt: str, **kwargs):
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not registered.")
        response = await self.providers[provider].ask(prompt, **kwargs)
        return AIResponseFormatter.format(provider, response)