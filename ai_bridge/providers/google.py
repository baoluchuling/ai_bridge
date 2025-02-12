import requests
from ai_bridge.providers.base_provider import ProviderStrategy

class GoogleProvider(ProviderStrategy):
    def __init__(self, provider=None, api_key=None, base_url=None, base_model=None):
        self.provider = provider or ""
        self.api_key = api_key or ""
        self.base_url = base_url or ""
        self.base_model = base_model or "gemini-1.5-flash"
        self.deployer = "google"

    async def ask_single(self, model, prompt: str):
        """支持单条 prompt 调用"""
        return await self.ask(model, [{"role": "user", "parts": [{"text": prompt}]}])
    
    async def ask(self, model, messages: list[dict], format: str = "text"):

        if model is None:
            model = self.base_model

        headers = {
            "Content-Type": "application/json"
        }
        
        if format == "json":
            payload = {
                "contents": self.convert_to_google(messages),
                "generationConfig": {"response_mime_type": "application/json"}
            }
        else:
            payload = {
                "contents": self.convert_to_google(messages),
            }

        url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"

        # logging.info("---- Request Information ----")
        # logging.info(f"URL: {url}")
        # logging.info(f"Headers: {json.dumps(headers, indent=4)}")
        # logging.info(f"Payload: {json.dumps(payload, indent=4)}")
        # logging.info("-----------------------------")

        response = requests.request("POST", url, json=payload, headers=headers)
        
        # logging.info("---- Response Information ----")
        # logging.info(f"Status Code: {response.status_code}")
        # logging.info(f"Response Body: {response.text.strip()}")
        # logging.info("-----------------------------")

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
    
    def convert_to_google(self, messages: list[dict]) -> list[dict]:
        """将 OpenAI 的消息格式转换为 Google API 格式"""
        converted = []
        for msg in messages:
            if "content" in msg:
                converted.append({
                    "role": "model" if msg["role"] == "system" else msg["role"],
                    "parts": [{"text": msg["content"]}]
                })
            else:
                raise ValueError(f"Message missing 'content' field: {msg}")
        return converted