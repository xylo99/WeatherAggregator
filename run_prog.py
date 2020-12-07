#!/usr/bin/env python3
import subprocess
import signal
import sys
import os

def config_srvr():
    # generate secret key.
    skey = subprocess.run(["cat /dev/urandom | base64 | head -c50"], shell=True, stdout=subprocess.PIPE).stdout.decode()[:-1]

    with open("WeatherAggregator/settings.py", "r") as f:
        sdata = f.readlines()

    sdata[12] = "SECRET_KEY='" + skey + "'\n"

    with open("WeatherAggregator/settings.py", "w") as f:
        f.writelines(sdata)


if __name__ == '__main__':
    config_srvr()
    # start containerized database and run the application.
    r = subprocess.Popen(["./launch_db.sh"], shell=True, preexec_fn=os.setsid)

