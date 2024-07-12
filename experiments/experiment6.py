from src.BuildHat import BuildHat as Serial
from src.Motor import Motor
from src.Robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard
from robonet.Publisher import Publisher
import zmq
from dotenv import load_dotenv
import os

load_dotenv()


PI_IP = os.getenv("PI_IP")

context = zmq.Context()
publisher = Publisher(
    context=context, address=f"tcp://{PI_IP}", node="motor", topic="motor-data"
)


serial = Serial()
left_motor = Motor("C", serial, -1)


left_motor.add_listener(publisher.send_json)


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    left_motor.run(0)
    time.sleep(1)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


print("setting speed")
left_motor.run(400)
time.sleep(30)
print("stopping")
left_motor.clean_up()
