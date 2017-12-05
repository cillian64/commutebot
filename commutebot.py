#!/usr/bin/env python3

import googlemaps
import sys
import schedule
from datetime import datetime
import time
from orm import Trial


try:
    import config
except ImportError:
    print("You need to create a config file at config.py")
    print("Use config.example.py as an example.")
    sys.exit(1)

# Check we won't exceed free quota:
numtrials = len(config.commutes) * (len(config.out_times) +
                                    len(config.return_times))
print("Number of trials to run each day: {}/2500".format(numtrials))

# Will produce a meaningful error if apikey is left as None
gmaps = googlemaps.Client(config.apikey)


def trial(direction, scheduledtime):
    for commute in config.commutes:
        if direction == "out":
            start, end = commute[0], commute[1]
        elif direction == "return":
            start, end = commute[1], commute[0]
        else:
            raise ValueError("Invalid direction")

        timestamp = datetime.now()

        routes = gmaps.directions(
            start, end, mode="driving", region=config.region,
            departure_time="now", traffic_model="best_guess")
        duration = routes[0]["legs"][0]["duration_in_traffic"]["value"]

        # Log timestamp, duration, scheduledtime, start, end
        trial = Trial(timestamp=timestamp, duration=duration,
                      scheduledtime=scheduledtime, start=start, end=end)
        trial.save()


for out_time in config.out_times:
    schedule.every().day.at(out_time).do(trial, "out", out_time)
for return_time in config.return_times:
    schedule.every().day.at(return_time).do(trial, "return", return_time)

while True:
    schedule.run_pending()
    time.sleep(1)
