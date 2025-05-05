from enum import Enum, auto

class TokenType(Enum):
    COMMAND = auto()
    DIRECTION = auto()
    ACTION = auto()
    WEAPON = auto()
    ITEM = auto()
    SPELL = auto()
    TARGET = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    KEYWORD = auto()
    COMMENT = auto()
    EOF = auto()
