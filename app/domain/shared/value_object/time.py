from datetime import datetime

class Time:
    def __init__(self, value: datetime):
        self._value = value

    def equals(self, other: 'Time') -> bool:
        return self._value == other._value
    
    def value(self) -> datetime:
        return self._value
    
def create_time(value: datetime) -> Time:
    return Time(value)