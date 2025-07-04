MAX_TITLE_LENGTH = 255
MIN_TITLE_LENGTH = 3


class Title:
    def __init__(self, value: str):
        if len(value) < MIN_TITLE_LENGTH:
            raise ValueError(f"Title must be at least {MIN_TITLE_LENGTH} characters long")
        if len(value) > MAX_TITLE_LENGTH:
            raise ValueError(f"Title must be less than {MAX_TITLE_LENGTH} characters long")
        self._value = value

    def equals(self, other: 'Title') -> bool:
        return self._value == other._value
    
    def value(self) -> str:
        return self._value
    
def create_title(value: str) -> Title:
    return Title(value)