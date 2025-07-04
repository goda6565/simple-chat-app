from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def generate_response(self, question: str, prompt: str) -> str:
        pass