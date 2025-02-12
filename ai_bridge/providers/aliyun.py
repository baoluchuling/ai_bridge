import requests
import json

from ai_bridge.providers.base_provider import ProviderStrategy

class AliyunProvider(ProviderStrategy):
    def __init__(self, provider=None, api_key=None, base_url=None, base_model=None):
        self.provider = provider or ""
        self.api_key = api_key or ""
        self.base_url = base_url or ""
        self.base_model = base_model or "qwen-max-latest"
        self.deployer = "aliyun"
    
    async def ask_single(self, model, prompt: str, format: str = "text"):
        """支持单条 prompt 调用"""
        return await self.ask(model, [{"role": "user", "content": prompt}], format)

    async def ask(self, model, messages: list[dict], format: str = "text"):
        if model is None:
            model = self.base_model

        if format == "json":
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {"type": "json_object"},
            }
        else:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "frequency_penalty": 0.5,
                "n": 1,
                "response_format": {"type": "text"},
            }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        url = self.base_url

        # print("---- Request Information ----")
        # print(f"URL: {url}")
        # print(f"Headers: {json.dumps(headers, indent=4)}")
        # print(f"Payload: {json.dumps(payload, indent=4)}")
        # print("-----------------------------")

        response = requests.request("POST", url, json=payload, headers=headers)

        # print("---- Response Information ----")
        # print(f"Status Code: {response.status_code}")
        # print(f"Response Body: {response.text.strip()}")
        # print("-----------------------------")

        if response.status_code < 200 or response.status_code >= 300:
            try:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message") or error_data.get("message")
            except Exception:
                error_message = response.text

            return {
                "error": True,
                "message": f"API request failed: {error_message}" if error_message else "Unknown API error.",
                "status_code": response.status_code
            }

        return response.json()