import requests
import json

class GoogleProvider:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or ""
        self.base_url = base_url or ""

    async def ask(self, prompt, **kwargs):
        headers = {
            # "Authorization": f"Bearer {self.api_key}",
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

        # 如果请求失败（非 2xx 状态码）
        if response.status_code < 200 or response.status_code >= 300:
            # 尝试解析 API 返回的错误消息
            try:
                error_data = response.json()  # 尝试解析 JSON
                error_message = error_data.get("error", {}).get("message") or error_data.get("message")
            except Exception:
                error_message = response.text  # 解析失败时，直接返回文本信息

            # 生成更准确的错误信息
            return {
                "error": True,
                "message": f"API request failed: {error_message}" if error_message else "Unknown API error.",
                "status_code": response.status_code
            }

        # 尝试解析 JSON，如果失败，则返回固定文案
        return response.json()