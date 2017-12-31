#!/usr/bin/env python3

import orm
from orm import Trial
import config
import matplotlib.pyplot as plt


def duration_against_time(start, end, times):
    data = []
    fig, ax = plt.subplots(figsize=(24, 18))
    for time in times:
        data.append(list(trial.duration/60.0 for trial in
                         Trial.select(Trial.duration)
                         .where((Trial.start == start) &
                                (Trial.end == end) &
                                (Trial.scheduledtime == time))))
    ax.boxplot(data, labels=times)
    ax.set_title("{} to {}".format(start, end))
    fig.savefig("{} to {}.png".format(start, end))


def duration_against_day(start, end, time):
    data = []
    fig, ax = plt.subplots(figsize=(12, 8))
    for dayidx, day in enumerate(orm.days_of_week):
        data.append(list(trial.duration/60.0 for trial in
                         Trial.select(Trial.duration)
                         .where((Trial.start == start) &
                                (Trial.end == end) &
                                (Trial.scheduledtime == time) &
                                (Trial.weekday == dayidx))))
    ax.boxplot(data, labels=orm.days_of_week)
    ax.set_title("Duration against day of week, {} to {}, {}".format(
        start, end, time))
    fig.savefig("DOW {} to {} at {}.png".format(start, end, time))


if __name__ == "__main__":
    # Display a box-plot of duration against time for each commute
    for commute in config.commutes:
        duration_against_time(commute[0], commute[1], config.out_times)
        duration_against_time(commute[1], commute[0], config.return_times)

    # Display a box-plot of duration against day-of-week at a particular time
    for commute in config.commutes:
        duration_against_day(commute[0], commute[1], "08:30")
        duration_against_day(commute[1], commute[0], "17:20")
