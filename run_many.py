import subprocess
import threading
import os
from time import sleep

def run_it():
    p = subprocess.run('python3 io_rpg_bot1.py', shell=True)

threads = []
for i in range(20):
    t = threading.Thread(target=run_it)
    t.daemon = True
    t.start()
    threads.append(t)

while True:
    sleep(1)
