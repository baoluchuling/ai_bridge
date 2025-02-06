import json

class AIResponseFormatter:
    """统一 AI API 响应数据格式"""

    @staticmethod
    def format(response: dict, provider: str) -> dict:
        """
        解析不同 AI API 返回的 JSON，转换为标准格式。

        :param response: AI API 的原始 JSON 响应
        :param provider: AI 提供商名称 (如 "openai", "deepseek", "google")
        :return: 统一格式的字典
        """
        if provider == "google":
            return AIResponseFormatter._format_google(response)
        elif provider == "openai":
            return AIResponseFormatter._format_openai(response)
        elif provider == "deepseek":
            return AIResponseFormatter._format_deepseek(response)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

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