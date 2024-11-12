
from enum import Enum


class KeysAndFlags(Enum):
    JSON = {
        '-j', '-json', 'j', '-j'
    }
    TEXT = 'text'

    FLAG_GET_STATE = '?'

class AvailabelsControllers(Enum):
    PEEK = 'Peek'
    SWARCO = 'Swarco'
    POTOK_S = 'Поток (S)'
    POTOK_P = 'Поток'