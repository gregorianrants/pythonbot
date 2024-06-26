from Serial import Serial
from Motor import Motor
import time
import signal
import sys

serial = Serial()
left_motor = Motor('C',serial,-1)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    left_motor.run(0)
    time.sleep(1)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
left_motor.run(521)
time.sleep(10)
left_motor.run(0)
time.sleep(1)
sys.exit(0)