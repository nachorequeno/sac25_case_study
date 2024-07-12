from typing import List
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def signals2prsignal_old(output_signal: str, input_signals: List[str]) -> None:
    df_output_signal = pd.DataFrame()
    # mean
    for input_signal in input_signals:
        # Read CSV file
        df_input_signal = pd.read_csv(input_signal, names=["time", "signal"], index_col=0)
        df_output_signal = df_output_signal.add(df_input_signal, fill_value=0)

    n = len(input_signals)
    df_output_signal["mean"] = df_output_signal["signal"] / n
    df_output_signal["signal"] = 0

    print(f"Number of signals: {n}")
    df_output_signal.head()

    # stdev
    for input_signal in input_signals:
        # Read CSV file
        df_input_signal = pd.read_csv(input_signal, names=["time", "signal"], index_col=0)
        df_output_signal = df_output_signal.add(df_input_signal * df_input_signal, fill_value=0)

    # stdev = sqrt(dev) where dev = [sum(x[i]**2 for i in range(n))/n - pow(sum(x for i in range(n))/n, 2)]
    df_output_signal["stdev"] = (df_output_signal["signal"] / n) - pow(df_output_signal["mean"], 2)
    df_output_signal["stdev"] = np.sqrt(df_output_signal["stdev"])
    df_output_signal = df_output_signal.drop(columns=["signal"])

    # Dump to output file
    print(df_output_signal)
    df_output_signal.to_csv(output_signal, header=False)


def signals2prsignal_opt(output_signal: str, input_signals: List[str]) -> None:
    df_output_signal = pd.DataFrame()
    df_mean_signal = pd.DataFrame()
    df_stdev_signal = pd.DataFrame()

    df_mean_signal["signal"] = 0.0
    df_stdev_signal["signal"] = 0.0

    for i, input_signal in enumerate(input_signals, start=1):
        # Read CSV file
        df_input_signal = pd.read_csv(input_signal, names=["time", "signal"], index_col=0)
        # mean
        # mean_increment = df_input_signal - df_mean_signal
        mean_increment = df_input_signal.add(-df_mean_signal, fill_value=0)
        df_mean_signal = df_mean_signal.add(mean_increment/i, fill_value=0)
        # stdev
        # stdev_increment = df_input_signal - df_mean_signal
        # stdev_increment = df_input_signal.add(-df_mean_signal, fill_value=0)
        # df_stdev_signal = df_stdev_signal.add(mean_increment * stdev_increment, fill_value=0)
        stdev_increment = pow(mean_increment, 2) * (i - 1)/i
        df_stdev_signal = df_stdev_signal.add(stdev_increment, fill_value=0)

    n = len(input_signals)
    df_output_signal["mean"] = df_mean_signal["signal"]
    df_output_signal["stdev"] = np.sqrt(df_stdev_signal["signal"]/n)

    print(f"Number of signals: {n}")
    print(df_output_signal.head())

    # Dump to output file
    print(df_output_signal)
    df_output_signal.to_csv(output_signal, header=False)


def signals2prsignal(output_signal: str, input_signals: List[str]) -> None:
    df_aggregated_signals = pd.DataFrame()

    i = 0
    for input_signal in input_signals:
        # Read CSV file
        df_input_signal = pd.read_csv(input_signal, names=["time", f"signal_{i}"], index_col=0)
        df_aggregated_signals = df_aggregated_signals.add(df_input_signal, fill_value=0)
        i = i + 1

    # print(f"Number of signals: {i}")
    # print(df_aggregated_signals.head())

    df_output_signal = pd.DataFrame()
    df_output_signal["mean"] = df_aggregated_signals.mean(axis=1)
    df_output_signal["stdev"] = df_aggregated_signals.std(axis=1, ddof=1)

    # Dump to output file
    print(df_output_signal)
    df_output_signal.to_csv(output_signal, header=False)


def plot_prsignal(output_signal: str, input_signals: List[str]) -> None:
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

    sns.lineplot(data=df_aggregated_signals, x="time", y="signal")
    plt.ylim(0, 2.75)
    # plt.show()
    plt.savefig(fname=output_signal, format='svg')


if __name__ == '__main__':
    output_signal = sys.argv[1]
    input_signals = sys.argv[2:]
    # signals2prsignal_old(output_signal, input_signals)
    # signals2prsignal_opt(output_signal, input_signals)
    signals2prsignal(f"{output_signal}.csv", input_signals)
    plot_prsignal(f"{output_signal}.svg", input_signals)
