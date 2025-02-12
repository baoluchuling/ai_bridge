from abc import ABC, abstractmethod

class ProviderStrategy(ABC):
    def __init__(self, provider=None, api_key=None, base_url=None, base_model=None):
        self.provider = provider or ""
        self.api_key = api_key or ""
        self.base_url = base_url or ""
        self.base_model = base_model or ""
        self.deployer = ""

    @abstractmethod
    async def ask_single(self, model: str, prompt: str, format: str = "text") -> str:
        pass

    @abstractmethod
    async def ask(self, model: str, messages: list[dict], format: str = "text") -> str:
        pass