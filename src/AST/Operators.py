
from enum import Enum


class Operators(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    INCR = '++'
    DECR = '--'
    EXP = '**'
    ASSIGN = '='
    GE = '>='
    LE = '<='
    NEQ = '!='
    EQ = '=='
    GT = '>'
    LT = '<'
    LOG_AND = '&&'
    LOG_OR = '||'
