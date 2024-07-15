import sys

import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
from ParetoLib.Geometry.Rectangle import Rectangle
from ParetoLib.Geometry.Zone import Zone
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ParetoLib.TRE.TRE import TimedrelInterface

def read_expression(filename: str) -> str:
    f = open(filename, "r")
    expression = f.read()
    f.close()
    return expression

def lower(x):
    None

def low(x):
    return 0.0 <= x[2] < 0.71

def medium(x):
    return 0.71 <= x[2] < 1.42

def high(x):
    return x[2] > 1.42

def higher(x):
    None

def plot_zones(zones: list[Zone]) -> None:
    f: Figure = plt.figure()
    ax1 = f.add_subplot(111)
    ax1.set_xlim(0, 48)
    ax1.set_ylim(0, 48)
    for zone in zones:
        zone.plot_2D(fig=f)

    plt.show()

def plot_prsignal(output_signal: str, input_signals: list[str], fig: Figure = None) -> Figure:
    if fig is None:
        # fig = plt.figure()
        fig, ax = plt.subplots()
    else:
        axes = fig.get_axes()
        ax = axes[0]

    df_aggregated_signals = pd.DataFrame()

    i = 0
    for input_signal in input_signals:
        # Read CSV file
        df_input_signal = pd.read_csv(input_signal, names=["time", "signal"], index_col=0)
        df_input_signal["id"] = i
        df_input_signal = df_input_signal.reset_index()

        df_aggregated_signals = pd.concat([df_aggregated_signals, df_input_signal])
        i = i + 1

    # print(f"Number of signals: {i}")
    # print(df_aggregated_signals)

    print(f"Pivot: {i}")
    signals_wide = df_aggregated_signals.pivot(index="id", columns="time", values="signal")
    print(signals_wide.head())

    sns.lineplot(data=df_aggregated_signals, x="time", y="signal", ax=ax)
    plt.ylim(0, 2.75)
    # plt.show()
    plt.savefig(fname=output_signal, format='svg')
    return plt.gcf()


def overlay(zone: Zone, fig: Figure = None) -> Figure:
    def _plot_rectangle(min_corner: tuple[float, float], max_corner: tuple[float, float], ax: Axes) -> None:
        r = Rectangle(min_corner, max_corner)
        vertices = r.vertices()
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        ax.fill(xs, ys, color='grey', alpha=0.25)

    if fig is None:
        # fig = plt.figure()
        fig, ax = plt.subplots()
    else:
        axes = fig.get_axes()
        ax = axes[0]
        # ax = axes

    b, bp = zone.bmin[0], zone.bmax[0]
    e, ep = zone.emin[0], zone.emax[0]
    d, dp = zone.dmin[0], zone.dmax[0]

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    # p1 = (b, e)
    # p2 = (b, b + dp)
    # p3 = (ep - dp, ep)
    # p4 = (bp, ep)
    # p5 = (bp, bp + d)
    # p6 = (e - d, e)

    # Begin
    ax.vlines(x=b, ymin=ymin, ymax=ymax, color='g', linestyle='-')
    ax.vlines(x=bp, ymin=ymin, ymax=ymax, color='g', linestyle='--')

    # End
    ax.vlines(x=e, ymin=ymin, ymax=ymax, color='r', linestyle='-')
    ax.vlines(x=ep, ymin=ymin, ymax=ymax, color='r', linestyle='--')

    ax.fill_betweenx(y=[ymin, ymax], x1=b, x2=e, facecolor='grey', alpha=0.25)
    # ax.fill((b, b, e, e), (ymin, ymax, ymax, ymin), color='grey', alpha=0.25)
    # _plot_rectangle((b, ymin), (e, ymax), ax)
    ax.fill_betweenx(y=[ymin, ymax], x1=b, x2=b + dp, facecolor='grey', alpha=0.25)
    # ax.fill((b, b, b + dp, b + dp), (ymin, ymax, ymax, ymin), color='grey', alpha=0.25)
    # _plot_rectangle((b, ymin), (b + dp, ymax), ax)
    ax.fill_betweenx(y=[ymin, ymax], x1=bp, x2=ep, facecolor='grey', alpha=0.25)
    # ax.fill((bp, bp, ep, ep), (ymin, ymax, ymax, ymin), color='grey', alpha=0.25)
    # _plot_rectangle((bp, ymin), (ep, ymax), ax)
    ax.fill_betweenx(y=[ymin, ymax], x1=bp, x2=bp + d, facecolor='grey', alpha=0.25)
    # ax.fill((bp, bp, bp + d, bp + d), (ymin, ymax, ymax, ymin), color='grey', alpha=0.25)
    # _plot_rectangle((bp, ymin), (bp + dp, ymax), ax)
    ax.fill_betweenx(y=[ymin, ymax], x1=ep - dp, x2=ep, facecolor='grey', alpha=0.25)
    # ax.fill((ep-dp, ep-dp, ep, ep), (ymin, ymax, ymax, ymin), color='grey', alpha=0.25)
    # _plot_rectangle((ep-dp, ymin), (ep, ymax), ax)
    ax.fill_betweenx(y=[ymin, ymax], x1=e - d, x2=e, facecolor='grey', alpha=0.25)
    # ax.fill((e-d, e-d, e, e), (ymin, ymax, ymax, ymin), color='grey', alpha=0.25)
    # _plot_rectangle((e - d, ymin), (e, ymax), ax)

    # plt.show()

    return fig
    # return plt.gcf()


if __name__=="__main__":
    attack = sys.argv[1]
    input_signals = sys.argv[2:]

    prec = 1

    expression_file = f"./tre/{attack}.txt"
    # expression = "(low ; high) [3 : 4]"
    expression = read_expression(expression_file)


    trace_file = f"./csv/{attack}.csv"
    # tre_expression: str, trace_file: str, precision: float, dtype: str, query_preds
    tre_engine = TimedrelInterface(tre_expression=expression, trace_file=trace_file, precision=prec, dtype="float",
                                   query_preds={'lower': lower, 'low': low, 'medium': medium, 'high': high,
                                                'higher': higher},)

    zones = tre_engine.run()
    print(zones)

    plot_zones(zones)

    f = plot_prsignal("temp", input_signals)
    for zone in zones:
        f = overlay(zone, f)

    plt.show()
