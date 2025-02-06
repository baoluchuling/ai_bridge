import json

class AIResponseFormatter:
    @staticmethod
    def format(provider, response):
        try:
            if not response or not isinstance(response, dict):
                return AIResponseFormatter._error_response(provider, "Invalid or empty response")

            if "error" in response:
                return AIResponseFormatter._error_response(
                    provider,
                    response.get("error", {}).get("message", "Unknown API error"),
                    code=response.get("error", {}).get("code", "unknown")
                )

            if provider == "openai":
                return AIResponseFormatter._format_openai(provider, response)
            elif provider == "deepseek":
                return AIResponseFormatter._format_deepseek(provider, response)
            elif provider == "google":
                return AIResponseFormatter._format_google(provider, response)
            else:
                return AIResponseFormatter._error_response(provider, "Unsupported provider", 500)
        except Exception as e:
            return AIResponseFormatter._error_response(provider, f"Error formatting response: {str(e)}", 500)

    @staticmethod
    def _error_response(provider, message, code):
        return {
            "status_code": code,
            "provider": provider,
            "message": message,
        }
    
    @staticmethod
    def _format_google(provider, response: dict) -> dict:
        try:
            text = response["candidates"][0]["content"]["parts"][0]["text"]
            tokens_used = response["usageMetadata"]["totalTokenCount"]
            model = response.get("modelVersion", "unknown")
            reasoning_content = ""
        except (KeyError, IndexError):
            raise ValueError("Invalid Google response format")

        return {
            "status_code": 200, 
            "provider": provider,
            "response": {
                "text": text.strip(),
                "tokens_used": tokens_used,
                "model": model,
                "reasoning_content": reasoning_content.strip(),
                "raw_response": response
            }
        }

    @staticmethod
    def _format_openai(provider, response: dict) -> dict:
        try:
            text = response["choices"][0]["message"]["content"]
            tokens_used = response["usage"]["total_tokens"]
            model = response.get("model", "unknown")
            reasoning_content = response["choices"][0].get("reasoning_content", "")
        except (KeyError, IndexError):
            raise ValueError("Invalid OpenAI response format")

        return {
            "status_code": 200,
            "provider": provider, 
            "response": {
                "text": text.strip(),
                "tokens_used": tokens_used,
                "model": model,
                "reasoning_content": reasoning_content.strip(),
                "raw_response": response
            }
        }

    @staticmethod
    def _format_deepseek(provider, response: dict) -> dict:
        try:
            text = response["choices"][0]["message"]["content"]
            tokens_used = response["usage"]["total_tokens"]
            model = response.get("model", "unknown")
            reasoning_content = response["choices"][0].get("reasoning_content", "")
        except (KeyError, IndexError):
            raise ValueError("Invalid DeepSeek response format")

        return {
            "status_code": 200,
            "provider": provider,
            "response": {
                "text": text.strip(),
                "tokens_used": tokens_used,
                "model": model,
                "reasoning_content": reasoning_content.strip(),
                "raw_response": response
            }
        }