
from enum import Enum

class EnumChoices(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]