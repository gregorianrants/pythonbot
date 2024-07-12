from src.BuildHat import BuildHat as Serial
from src.Motor import Motor
from src.Robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard

from robonet.src.Publisher import Publisher
import zmq
from dotenv import load_dotenv
import os
import functools

load_dotenv()


PI_IP = os.getenv("PI_IP")

context = zmq.Context()
publisher = Publisher(
    context=context,
    address=f"tcp://{PI_IP}",
    node="robot",
    topics=["motor-data", "speed-recorder-command"],
)


serial = Serial()


left_motor = Motor("C", serial, -1)
right_motor = Motor("D", serial, 1)

listener = functools.partial(publisher.send_json, "motor-data")

right_motor.add_listener(listener)


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    left_motor.run(0)
    right_motor.run(0)
    time.sleep(1)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

robot = Robot(left_motor, right_motor)


def press(key):
    print(f"'{key}' pressed")
    if key == "k":
        publisher.send_json("speed-recorder-command", {"command": "start"})
        robot.forward()
    if key == "m":
        robot.back()
    if key == "z":
        robot.left()
    if key == "x":
        robot.right()
    if key == "space":
        publisher.send_json("speed-recorder-command", {"command": "stop"})
        right_motor.listeners = []
        robot.pause()


def release(key):
    print(f"'{key}' released")


listen_keyboard(
    on_press=press,
    on_release=release,
)
