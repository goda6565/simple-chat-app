from app.domain.chat.repository.chat import ChatRepository
from app.domain.chat.entity.chat import Chat
from app.domain.shared.value_object.id import Id

class ChatRepositoryMemoryImpl(ChatRepository):
    def __init__(self):
        self._chats: list[Chat] = []

    def create(self, chat: Chat) -> Chat:
        self._chats.append(chat)
        return chat
    
    def update(self, chat: Chat) -> Chat:
        self._chats = [chat for chat in self._chats if chat.get_id() != chat.get_id()]
        self._chats.append(chat)
        return chat
    
    def delete(self, id: Id) -> None:
        self._chats = [chat for chat in self._chats if chat.get_id() != id]
    
    def find_by_id(self, id: Id) -> Chat:
        chat = next((chat for chat in self._chats if chat.get_id() == id), None)
        if chat is None:
            raise ValueError(f"Chat with id {id} not found")
        return chat
    
    def find_all(self) -> list[Chat]:
        return self._chats
    
def create_chat_repository() -> ChatRepository:
    return ChatRepositoryMemoryImpl()