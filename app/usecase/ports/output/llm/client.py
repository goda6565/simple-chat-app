from abc import ABC, abstractmethod
from typing import Optional

class LLMClient(ABC):
    @abstractmethod
    def generate_response(self, question: str, prompt: str, chat_history: Optional[str]) -> str:
        pass 