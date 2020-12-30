import pandas as pd
from ..base.utils import EntryIndices, IndexRange
from ..base.enums import PosType, Col
from ..base.plotting import plot_lines_unblock, show_plot, plot_histogram_unblock, plot_centered_cumulative_histogram, plot_for_stoploss

def slice_reset_index(df, col:Col, irange:IndexRange):
    return irange.sliced_of(df[Col.LOW]).reset_index(drop=True)

def analyse(df, entries:EntryIndices, holding_period=5):

    # loss_lines_long = []
    # loss_lines_short = []
    # prof_lines_long = []
    # prof_lines_short = []

    profits = []
    drawdowns = []

    for i in range(entries.size()):
        entry_type, entry_i = entries[i]
        irange = IndexRange(entry_i.glob, entry_i.glob+holding_period+1)

        highs = slice_reset_index(df, Col.HIGH, irange)
        lows = slice_reset_index(df, Col.LOW, irange)
        closes = slice_reset_index(df, Col.CLOSE, irange)

        entry_price = closes[0]
        rel_highs = [h - entry_price for h in highs]
        rel_lows = [l - entry_price for l in lows]
        rel_closes = [c - entry_price for c in closes]
        if entry_type == PosType.LONG:
            profits.append(rel_closes[-1])
            dd = min(rel_lows)
        else:
            profits.append(-1*rel_closes[-1])
            dd = -max(rel_highs)

        drawdowns.append(dd)
        
    # plot_histogram_unblock(drawdowns, title=f"Holding Drawdowns ({holding_period} bars holding)")
    plot_for_stoploss(drawdowns, profits, center_val=1, title=f"Stoploss Analysis from DD ({holding_period} bars) ({entries.size()} entries)")
        # plot_histogram_unblock(drawdowns, title=f"Holding Drawdowns ({holding_period} bars holding)")
        # if entry_type == PosType.LONG:
        #     loss_win = df[Col.LOW]
        #     loss_win = irange.sliced_of(loss_win).reset_index(drop=True)
        #     loss_win = [p - loss_win[0] for p in loss_win]
        #     loss_lines_long.append(loss_win)
        #     prof_win = df[Col.HIGH]
        #     prof_win = irange.sliced_of(prof_win).reset_index(drop=True)
        #     prof_win = [p - prof_win[0] for p in prof_win]
        #     prof_lines_long.append(prof_win)
        # else:
        #     loss_win = df[Col.HIGH]
        #     loss_win = irange.sliced_of(loss_win).reset_index(drop=True)
        #     loss_win = [p - loss_win[0] for p in loss_win]
        #     loss_lines_short.append(loss_win)
            
        #     prof_win = df[Col.LOW]
        #     prof_win = irange.sliced_of(prof_win).reset_index(drop=True)
        #     prof_win = [p - prof_win[0] for p in prof_win]
        #     prof_lines_short.append(prof_win)

    # dd_long = [min(l) for l in loss_lines_long]
    # dd_short = [max(l) for l in loss_lines_short]
    # du_long = [max(l) for l in prof_lines_long]
    # du_short = [min(l) for l in prof_lines_short]
    # plot_lines_unblock(loss_lines_long, title="result long")
    # plot_lines_unblock(loss_lines_short, title="result short")
    # plot_histogram_unblock(dd_long+du_long, title="dd du long")
    # plot_histogram_unblock(dd_short+du_short, title="dd du short")
    # plot_centered_cumulative_histogram(dd_long, title="dd long")
    # plot_centered_cumulative_histogram(dd_short, title="dd short")
    
    
    show_plot()
        