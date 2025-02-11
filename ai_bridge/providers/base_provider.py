from abc import ABC, abstractmethod

class ProviderStrategy(ABC):
    @abstractmethod
    async def ask_single(self, model: str, prompt: str, format: str = "text") -> str:
        pass

    @abstractmethod
    async def ask(self, model: str, messages: list[dict], format: str = "text") -> str:
        pass