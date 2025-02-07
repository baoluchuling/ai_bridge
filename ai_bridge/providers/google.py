import requests
import json

class GoogleProvider:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or ""
        self.base_url = base_url or ""

    async def ask_single(self, model, prompt: str):
        """支持单条 prompt 调用"""
        return await self.ask(model, [{"role": "user", "parts": [{"text": prompt}]}])
    
    async def ask(self, model, messages: list[dict]):

        if model is None:
            model = "gemini-1.5-flash"

        headers = {
            "Content-Type": "application/json"
        }
        payload = {"contents": self.convert_to_google(messages)}

        url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"

        print("---- Request Information ----")
        print(f"URL: {url}")
        print(f"Headers: {json.dumps(headers, indent=4)}")
        print(f"Payload: {json.dumps(payload, indent=4)}")
        print("-----------------------------")
        
        response = requests.request("POST", url, json=payload, headers=headers)
        
        print("---- Response Information ----")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text.strip()}")
        print("-----------------------------")

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