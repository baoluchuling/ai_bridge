import openai

class OpenAIProvider:
    def __init__(self, api_key=None):
        self.api_key = api_key or "your-default-openai-key"
        openai.api_key = self.api_key

    async def ask(self, prompt, **kwargs):
        response = await openai.Completion.create(
            model=kwargs.get("model", "gpt-3.5-turbo"),
            prompt=prompt,
            max_tokens=kwargs.get("max_tokens", 150)
        )
        return response.choices[0].text.strip()