from sys import argv
from fx_findings.base.enums import *
from fx_findings import reversal_analysis

reversal_analysis.run_wick(
    Timeframe(argv[1]),
    Quote(argv[2]),
    PosType(int(argv[3]))
)