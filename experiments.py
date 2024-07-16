import sys

import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from ParetoLib.TRE.TRE import TimedrelInterface
from signals2prsignal import plot_zones, plot_prsignal_with_zones


def create_temporary_trace_file(input_signals: list[str], trace_file: str) -> None:
    pass

def plot_prsignal(input_signals: list[str], fig: Figure = None) -> Figure:
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

    print(f"Pivot: {i}")
    signals_wide = df_aggregated_signals.pivot(index="id", columns="time", values="signal")
    print(signals_wide.head())

    sns.lineplot(data=df_aggregated_signals, x="time", y="signal", ax=ax)
    plt.ylim(0, 2.75)
    return plt.gcf()

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


if __name__=="__main__":
    attack = sys.argv[1]
    input_signals = sys.argv[2:]

    prec = 1

    expression_file = f"./tre/{attack}.txt"
    # expression = "(low ; high) [3 : 4]"
    expression = read_expression(expression_file)

    trace_file = f"./csv/{attack}.csv"
    create_temporary_trace_file(input_signals, trace_file)
    # tre_expression: str, trace_file: str, precision: float, dtype: str, query_preds
    tre_engine = TimedrelInterface(tre_expression=expression, trace_file=trace_file, precision=prec, dtype="float",
                                   query_preds={'lower': lower, 'low': low, 'medium': medium, 'high': high,
                                                'higher': higher},)

    zones = tre_engine.run()
    print(zones)

    plot_zones(zones)
    plot_prsignal_with_zones(input_signals, zones)
