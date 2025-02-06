import requests
import json

class GoogleProvider:
    def __init__(self, api_key=None):
        self.api_key = api_key or ""
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    async def ask(self, prompt, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        url = f"{self.base_url}?key={self.api_key}"

        # 打印请求信息
        print("---- Request Information ----")
        print(f"URL: {url}")
        print(f"Headers: {json.dumps(headers, indent=4)}")
        print(f"Payload: {json.dumps(payload, indent=4)}")
        print("-----------------------------")
        
        # 发送请求
        response = requests.request("POST", url, json=payload, headers=headers)
        
        # 打印响应信息
        print("---- Response Information ----")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text.strip()}")
        print("-----------------------------")

        return response.text.strip()