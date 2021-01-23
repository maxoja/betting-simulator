from enum import Enum, auto

class Timeframe(str, Enum):
    D1 = 'D1'
    H4 = 'H4'
    H1 = 'H1'
    M5 = 'M5'
    M15 = 'M15'
    M20 = 'M20'

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
    RISE = 'RISE'
    FALL = 'FALL'
    BODY = 'BODY'
    WICK_T = 'WICK_T'
    WICK_B = 'WICK_B'

class Broker(str, Enum):
    PEPPER = 'pepper'
    XM = 'xm'
    XM_LOW = 'xm-low'

class PosType(Enum):
    SHORT = auto()
    LONG = auto()