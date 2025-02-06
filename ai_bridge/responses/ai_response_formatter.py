from typing import Any, Optional

class AIResponse:
    def __init__(self, text: str, tokens_used: int, model: str, reasoning_content: str, raw_response: Any):
        self.text = text
        self.tokens_used = tokens_used
        self.model = model
        self.reasoning_content = reasoning_content
        self.raw_response = raw_response

    def to_dict(self):
        """ 转换为字典 """
        return {
            "text": self.text,
            "tokens_used": self.tokens_used,
            "model": self.model,
            "reasoning_content": self.reasoning_content,
            "raw_response": self.raw_response,
        }

    def __repr__(self):
        return f"AIResponse(text={self.text}, tokens_used={self.tokens_used}, model={self.model}, reasoning_content={self.reasoning_content}, raw_response={self.raw_response})"

class ResponseModel:
    def __init__(self, status_code: int, vendor: str, message: str, response: Optional[AIResponse] = None):
        self.status_code = status_code
        self.vendor = vendor
        self.message = message
        self.response = response

    def to_dict(self):
        """ 转换为字典 """
        return {
            "status_code": self.status_code,
            "vendor": self.vendor,
            "message": self.message,
            "response": self.response,
        }

    def __repr__(self):
        return f"ResponseModel(status_code={self.status_code}, vendor={self.vendor}, message={self.message}, response={self.response})"

class AIResponseFormatter:
    @staticmethod
    def format(vendor, response):
        try:
            if not response or not isinstance(response, dict):
                return AIResponseFormatter._error_response(vendor, "Invalid or empty response")

            if "error" in response:
                return AIResponseFormatter._error_response(
                    vendor,
                    response.get("error", {}).get("message", "Unknown API error"),
                    code=response.get("error", {}).get("code", "unknown")
                )

            if vendor == "openai":
                return AIResponseFormatter._format_openai(vendor, response)
            elif vendor == "deepseek":
                return AIResponseFormatter._format_deepseek(vendor, response)
            elif vendor == "google":
                return AIResponseFormatter._format_google(vendor, response)
            else:
                return AIResponseFormatter._error_response(vendor, "Unsupported provider", 500)
        except Exception as e:
            return AIResponseFormatter._error_response(vendor, f"Error formatting response: {str(e)}", 500)

    @staticmethod
    def _error_response(vendor, message, code):
        return ResponseModel(
            code,
            vendor,
            message
        )
    
    @staticmethod
    def _format_google(vendor, response: dict) -> dict:
        try:
            text = response["candidates"][0]["content"]["parts"][0]["text"]
            tokens_used = response["usageMetadata"]["totalTokenCount"]
            model = response.get("modelVersion", "unknown")
            reasoning_content = ""
        except (KeyError, IndexError):
            raise ValueError("Invalid Google response format")
        
        return ResponseModel(
            200,
            vendor,
            AIResponse(
                text.strip(),
                tokens_used,
                model,
                reasoning_content.strip(),
                response
            )
        )

    @staticmethod
    def _format_openai(vendor, response: dict) -> dict:
        try:
            text = response["choices"][0]["message"]["content"]
            tokens_used = response["usage"]["total_tokens"]
            model = response.get("model", "unknown")
            reasoning_content = response["choices"][0].get("reasoning_content", "")
        except (KeyError, IndexError):
            raise ValueError("Invalid OpenAI response format")

        return ResponseModel(
            200,
            vendor,
            AIResponse(
                text.strip(),
                tokens_used,
                model,
                reasoning_content.strip(),
                response
            )
        )

    @staticmethod
    def _format_deepseek(vendor, response: dict) -> dict:
        try:
            text = response["choices"][0]["message"]["content"]
            tokens_used = response["usage"]["total_tokens"]
            model = response.get("model", "unknown")
            reasoning_content = response["choices"][0].get("reasoning_content", "")
        except (KeyError, IndexError):
            raise ValueError("Invalid DeepSeek response format")

        return ResponseModel(
            200,
            vendor,
            AIResponse(
                text.strip(),
                tokens_used,
                model,
                reasoning_content.strip(),
                response
            )
        )