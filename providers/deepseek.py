import requests

class DeepSeekProvider:
    def __init__(self, api_key=None):
        self.api_key = api_key or "your-google-key"
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
            "Authorization": "Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", self.base_url, json=payload, headers=headers)

        return response.text.strip()