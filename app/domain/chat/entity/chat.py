from app.domain.shared.value_object.id import Id
from app.domain.shared.value_object.time import Time
from app.domain.chat.value_object.title import Title
from app.domain.chat.value_object.question import Question
from app.domain.chat.value_object.answer import Answer

class Step:
    def __init__(self, id: Id, chat_id: Id, question: Question, answer: Answer, created_at: Time):
        self._id = id
        self._chat_id = chat_id
        self._question = question
        self._answer = answer
        self._created_at = created_at
        
    def get_id(self) -> Id:
        return self._id
    
    def get_chat_id(self) -> Id:
        return self._chat_id
    
    def get_question(self) -> Question:
        return self._question
    
    def get_answer(self) -> Answer:
        return self._answer
    
    def get_created_at(self) -> Time:
        return self._created_at
    
    def equals(self, other: 'Step') -> bool:
        return self._id.equals(other._id)
    
def create_step(id: Id, chat_id: Id, question: Question, answer: Answer, created_at: Time) -> Step:
    return Step(id, chat_id, question, answer, created_at)
        

class Chat:
    def __init__(self, id: Id, title: Title, steps: list[Step], created_at: Time, updated_at: Time):
        self._id = id
        self._title = title
        self._steps = steps
        self._created_at = created_at
        self._updated_at = updated_at

    def get_id(self) -> Id:
        return self._id
    
    def get_title(self) -> Title:
        return self._title
    
    def get_steps(self) -> list[Step]:
        return self._steps
    
    def get_created_at(self) -> Time:
        return self._created_at
    
    def get_updated_at(self) -> Time:
        return self._updated_at
    
    def add_step(self, step: Step):
        self._steps.append(step)
    
    def remove_step(self, step: Step):
        self._steps.remove(step)

    def update_updated_at(self, updated_at: Time):
        self._updated_at = updated_at

    def equals(self, other: 'Chat') -> bool:
        return self._id.equals(other._id)
    
def create_chat(id: Id, title: Title, steps: list[Step], created_at: Time, updated_at: Time) -> Chat:
    return Chat(id, title, steps, created_at, updated_at)
    