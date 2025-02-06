import json
import os
from ai_bridge.providers import OpenAIProvider, DeepSeekProvider, GoogleProvider
from ai_bridge.responses.ai_response_formatter import AIResponseFormatter

class AIBridge:
    def __init__(self):
        self.vendorList = {}
        self.load_vendors()

    def load_vendors(self):

        vendors_config = os.getenv("AI_BRIDGE_PROVIDERS")

        if not vendors_config:
            print("⚠️  No provider configuration found in environment variables.")
            return
        
        try:
            config = json.loads(vendors_config)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in AI_BRIDGE_PROVIDERS")

        for vendor_name, vendors_config in config.items():
            api_key = vendors_config.get("api_key")
            base_url = vendors_config.get("base_url")
            if api_key and base_url:
                self.register_vendor(vendor_name, api_key, base_url)

    def register_vendor(self, vendor_name: str, api_key: str, base_url: str):
        provider_classes = {
            "openai": OpenAIProvider,
            "deepseek": DeepSeekProvider,
            "google": GoogleProvider
        }

        if vendor_name in provider_classes:
            self.vendorList[vendor_name] = provider_classes[vendor_name](api_key, base_url)
        else:
            raise ValueError(f"Unsupported provider: {vendor_name}")

    async def ask_single(self, vendor: str, prompt: str, model = None):
        if vendor not in self.vendorList:
            raise ValueError(f"Provider {vendor} not registered.")
        response = await self.vendorList[vendor].ask(model, prompt)
        return AIResponseFormatter.format(vendor, response)
    
    async def ask(self, vendor: str, messages: list[dict], model = None):
        if vendor not in self.vendorList:
            raise ValueError(f"Provider {vendor} not registered.")
        response = await self.vendorList[vendor].ask(model, messages)
        return AIResponseFormatter.format(vendor, response)