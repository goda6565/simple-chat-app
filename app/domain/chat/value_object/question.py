MAX_QUESTION_LENGTH = 255

class Question:
    def __init__(self, value: str):
        if len(value) > MAX_QUESTION_LENGTH:
            raise ValueError(f"Question must be less than {MAX_QUESTION_LENGTH} characters long")
        self._value = value

    def equals(self, other: 'Question') -> bool:
        return self._value == other._value
    
    def value(self) -> str:
        return self._value
    
def create_question(value: str) -> Question:
    return Question(value)