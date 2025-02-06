from abc import ABC, abstractmethod

class ProviderStrategy(ABC):
    @abstractmethod
    async def ask(self, prompt: str, **kwargs) -> str:
        pass