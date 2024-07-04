from BuildHat import BuildHat as Serial
from Motor import Motor
from Robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard
from Publisher import Publisher
import zmq

# context = zmq.Context()
# publisher = Publisher(
#     context=context, address="tcp://192.168.178.26", node="motor", topic="odometry"
# )


serial = Serial()
left_motor = Motor("C", serial, -1)


# left_motor.add_listener(publisher.send_json)


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    left_motor.run(0)
    time.sleep(1)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


print("setting speed")
left_motor.run(300)
time.sleep(30)
print("stopping")
left_motor.clean_up()

