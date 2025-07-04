class Answer:
    def __init__(self, value: str):
        self._value = value

    def equals(self, other: 'Answer') -> bool:
        return self._value == other._value
    
    def value(self) -> str:
        return self._value
    
def create_answer(value: str) -> Answer:
    return Answer(value)