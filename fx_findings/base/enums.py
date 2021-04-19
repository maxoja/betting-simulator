from enum import Enum, auto, IntEnum

class Timeframe(str, Enum):
    D3 = 'D3'
    D2 = 'D2'
    D1 = 'D1'
    H4 = 'H4'
    H1 = 'H1'
    M5 = 'M5'
    M15 = 'M15'
    M20 = 'M20'

class Quote(str, Enum):
    AUDCAD = 'AUDCAD'
    AUDCHF = 'AUDCHF'
    AUDJPY = 'AUDJPY'
    AUDNZD = 'AUDNZD'
    AUDUSD = 'AUDUSD'
    CADCHF = 'CADCHF'
    CADJPY = 'CADJPY'
    CHFJPY = 'CHFJPY'
    EURAUD = 'EURAUD'
    EURCAD = 'EURCAD'
    EURCHF = 'EURCHF'
    EURGBP = 'EURGBP'
    EURJPY = 'EURJPY'
    EURNZD = 'EURNZD'
    EURUSD = 'EURUSD'
    GBPAUD = 'GBPAUD'
    GBPCAD = 'GBPCAD'
    GBPCHF = 'GBPCHF'
    GBPJPY = 'GBPJPY'
    GBPNZD = 'GBPNZD'
    GBPUSD = 'GBPUSD'
    NZDCAD = 'NZDCAD'
    NZDCHF = 'NZDCHF'
    NZDJPY = 'NZDJPY'
    NZDUSD = 'NZDUSD'
    USDCAD = 'USDCAD'
    USDCHF = 'USDCHF'
    USDJPY = 'USDJPY'

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
    HEIGHT = 'HEIGHT'

class Broker(str, Enum):
    PEPPER = 'pepper'
    XM = 'xm'
    XM_LOW = 'xm-low'

class PosType(IntEnum):
    SHORT = -1
    LONG = 1

class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()

class Clr(str, Enum):
    LIGHT_RED = '#ffe7e6'
    LIGHT_BLUE = '#e6e7ff'
    DEFAULT_BLUE = '#1f77b4'
    RED = 'red'
    ROSE = 'pink'
    LAVENDER = 'purple'