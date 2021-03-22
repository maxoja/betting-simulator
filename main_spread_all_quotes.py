from sys import argv
from fx_findings.base.enums import *
from fx_findings import spread_analysis

spread_analysis.run_all(Timeframe(argv[1]), Broker(argv[2]))