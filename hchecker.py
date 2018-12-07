#!/usr/bin/env python3

from __future__ import print_function

import argparse
import datetime
import json
import psutil
import time

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

METRICS = {}

def main(ticks, delay):

    global METRICS
    for _ in range(ticks):
        now = datetime.datetime.now()
        temps = psutil.sensors_temperatures()
        for name in temps.keys():
            if name in temps:
                for entry in temps[name]:
                    label = entry.label or name
                    temp = entry.current
                    elem = {
                        "current": entry.current,
                        "time": now
                    }
                    if METRICS.get(label):
                        METRICS[label].append(elem)
                    else:
                        METRICS[label] = [elem]
        time.sleep(delay)
    labels = METRICS.keys()
    metrics = METRICS.values()
    ax = plt.subplot()
    for label, metric in zip(labels, metrics):
        xs = [m['time'] for m in metric]
        ys = [m['current'] for m in metric]

        ax.plot(xs, ys, label=label)
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%M:%S"))
    ax.legend(loc="lower left", shadow=False, fontsize="xx-small")
    plt.show()


PARSER = argparse.ArgumentParser(description='Meansure core temps.')
PARSER.add_argument('--ticks', nargs='?', default=10, type=int,
                    help='Count of checks.')
PARSER.add_argument('--delay', nargs='?', default=1, type=float,
                    help='Delay between checks.')


if __name__ == '__main__':
    ARGS = PARSER.parse_args()
    main(ARGS.ticks, ARGS.delay)
