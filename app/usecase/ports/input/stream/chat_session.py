from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class StepInput:
    id: str
    question: str
    answer: str
    created_at: datetime

@dataclass
class ChatSessionInput:
    chat_id: str
    is_first: bool
    title: Optional[str]
    current_question: str
    steps: list[StepInput]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

@dataclass
class StepOutput:
    id: str
    question: str
    answer: str
    created_at: datetime

@dataclass
class ChatSessionOutput:
    chat_id: str
    answer: str
    title: str
    steps: list[StepOutput]
    created_at: datetime
    updated_at: datetime

class ChatSessionInputPort(ABC):
    @abstractmethod
    def execute(self, input: ChatSessionInput) -> ChatSessionOutput:
        pass