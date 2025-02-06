import requests
import json

class DeepSeekProvider:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"

    async def ask(self, prompt, **kwargs):

        payload = {
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "max_tokens": 512,
            "stop": ["null"],
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

        # 打印请求信息
        print("---- Request Information ----")
        print(f"URL: {url}")
        print(f"Headers: {json.dumps(headers, indent=4)}")
        print(f"Payload: {json.dumps(payload, indent=4)}")
        print("-----------------------------")

        response = requests.request("POST", url, json=payload, headers=headers)

        # 打印响应信息
        print("---- Response Information ----")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text.strip()}")
        print("-----------------------------")

        return response.text.strip()