import requests
from ai_bridge.providers.base_provider import ProviderStrategy

class OpenAIProvider(ProviderStrategy):
    def __init__(self, provider=None, api_key=None, base_url=None, base_model=None):
        self.provider = provider or ""
        self.api_key = api_key or ""
        self.base_url = base_url or ""
        self.base_model = base_model or "gpt-4o"
        self.deployer = "openai"

    async def ask_single(self, model, prompt: str):
        """支持单条 prompt 调用"""
        return await self.ask(model, [{"role": "user", "content": prompt}])
    
    async def ask(self, model, messages: list[dict], format: str = "text"):
        if model is None:
            model = self.base_model

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "store": True,
            "messages": messages
        }

        url = f"{self.base_url}"

        # print("---- Request Information ----")
        # print(f"URL: {url}")
        # print(f"Headers: {json.dumps(headers, indent=4)}")
        # print(f"Payload: {json.dumps(payload, indent=4)}")
        # print("-----------------------------")
        
        response = requests.request("POST", url, json=payload, headers=headers, verify=False)
        
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