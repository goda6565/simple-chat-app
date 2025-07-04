from abc import ABC, abstractmethod
from app.domain.shared.value_object.id import Id
from app.domain.chat.entity.chat import Chat

class ChatRepository(ABC):
    @abstractmethod
    def create(self, chat: Chat) -> Chat:
        pass

    @abstractmethod
    def update(self, chat: Chat) -> Chat:
        pass

    @abstractmethod
    def delete(self, id: Id) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: Id) -> Chat:
        pass
    
    @abstractmethod
    def find_all(self) -> list[Chat]:
        pass
