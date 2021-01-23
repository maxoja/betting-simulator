from sys import argv
from fx_findings.base.enums import *
from fx_findings import spread_analysis

spread_analysis.run(Timeframe(argv[1]), Quote(argv[2]), Broker(argv[3]))