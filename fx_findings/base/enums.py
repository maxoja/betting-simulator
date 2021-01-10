from enum import Enum, auto

class Timeframe(str, Enum):
    D1 = 'D1'
    H4 = 'H4'
    H1 = 'H1'
    M5 = 'M5'

class Quote(str, Enum):
    AUDCAD = 'AUDCAD'
    EURCHF = 'EURCHF'
    EURUSD = 'EURUSD'

class Col(str, Enum):
    DATETIME = '<DATETIME>'
    OPEN = '<OPEN>'
    CLOSE = '<CLOSE>'
    HIGH = '<HIGH>'
    LOW = '<LOW>'
    VOL = '<VOL>'
    SPREAD = '<SPREAD>'

class Broker(str, Enum):
    PEPPER = 'pepper'
    XM = 'xm'

class PosType(Enum):
    SHORT = auto()
    LONG = auto()