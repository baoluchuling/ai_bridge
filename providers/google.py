import aiohttp

class GoogleProvider:
    def __init__(self, api_key=None):
        self.api_key = api_key or "your-google-key"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    async def ask(self, prompt, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}?key={self.api_key}", json=payload, headers=headers) as resp:
                data = await resp.json()
                return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()