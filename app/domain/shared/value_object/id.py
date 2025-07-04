import uuid

class Id:
    def __init__(self, value: str):
        if not uuid.UUID(value):
            raise ValueError("Id must be a valid UUID")
        self._value = value

    def equals(self, other: 'Id') -> bool:
        return self._value == other._value
    
    def value(self) -> str:
        return self._value
    
def create_id(value: str) -> Id:
    return Id(value)