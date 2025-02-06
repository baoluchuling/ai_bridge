import json

class AIResponseFormatter:
    """统一 AI API 响应数据格式"""

    @staticmethod
    def format(provider, response):
        """
        统一解析不同 AI API 的返回结果，支持错误处理。
        
        :param response: API 响应（dict 或 None）
        :param provider: AI 提供商名称（str）
        :return: 统一格式的 dict
        """
        try:
            # 处理 API 请求失败（response 可能是 None 或非 dict）
            if not response or not isinstance(response, dict):
                return AIResponseFormatter._error_response(provider, "Invalid or empty response")

            # 处理 HTTP 错误情况
            if "error" in response:
                return AIResponseFormatter._error_response(
                    provider,
                    response.get("error", {}).get("message", "Unknown API error"),
                    code=response.get("error", {}).get("code", "unknown")
                )

            # 解析不同 AI 提供商的响应
            if provider == "openai":
                return AIResponseFormatter._format_openai(response)
            elif provider == "deepseek":
                return AIResponseFormatter._format_deepseek(response)
            elif provider == "google":
                return AIResponseFormatter._format_google(response)
            else:
                return AIResponseFormatter._error_response(provider, "Unsupported provider")
        except Exception as e:
            return AIResponseFormatter._error_response(provider, f"Error formatting response: {str(e)}")

    @staticmethod
    def _error_response(provider, message):
        """
        统一错误格式
        """
        return {
            "error": True,
            "provider": provider,
            "message": message,
            "text": "",
            "reasoning": "",
            "tokens_used": 0
        }
    
    @staticmethod
    def _format_google(response: dict) -> dict:
        """格式化 Google Gemini AI 响应"""
        try:
            text = response["candidates"][0]["content"]["parts"][0]["text"]
            tokens_used = response["usageMetadata"]["totalTokenCount"]
            model = response.get("modelVersion", "unknown")
            reasoning_content = ""  # Google API 没有提供推理内容
        except (KeyError, IndexError):
            raise ValueError("Invalid Google response format")

        return {
            "text": text.strip(),
            "tokens_used": tokens_used,
            "model": model,
            "reasoning_content": reasoning_content,
            "raw_response": response
        }

    @staticmethod
    def _format_openai(response: dict) -> dict:
        """格式化 OpenAI API 响应"""
        try:
            text = response["choices"][0]["message"]["content"]
            tokens_used = response["usage"]["total_tokens"]
            model = response.get("model", "unknown")
            reasoning_content = response["choices"][0].get("reasoning_content", "")
        except (KeyError, IndexError):
            raise ValueError("Invalid OpenAI response format")

        return {
            "text": text.strip(),
            "tokens_used": tokens_used,
            "model": model,
            "reasoning_content": reasoning_content.strip(),
            "raw_response": response
        }

    @staticmethod
    def _format_deepseek(response: dict) -> dict:
        """格式化 DeepSeek AI 响应"""
        try:
            text = response["choices"][0]["message"]["content"]
            tokens_used = response["usage"]["total_tokens"]
            model = response.get("model", "unknown")
            reasoning_content = response["choices"][0].get("reasoning_content", "")
        except (KeyError, IndexError):
            raise ValueError("Invalid DeepSeek response format")

        return {
            "text": text.strip(),
            "tokens_used": tokens_used,
            "model": model,
            "reasoning_content": reasoning_content.strip(),
            "raw_response": response
        }