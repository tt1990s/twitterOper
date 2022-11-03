import subprocess
import time

NUM_TIME = 1000

for idx in range(NUM_TIME):
    print("Start: ", str(idx))
    subprocess.call("python unfav.py")
    print("End: ", str(idx))
    time.sleep(10)