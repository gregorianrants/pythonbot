from src.BuildHat import BuildHat as Serial
from src.Motor import Motor
from src.Robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard

with (
    Serial() as serial,
    Motor("C", serial, -1) as left_motor,
    Motor("D", serial, 1) as right_motor,
):
    try:
        robot = Robot(left_motor, right_motor)

        def press(key):
            print(f"'{key}' pressed")
            if key == "k":
                robot.forward()
            if key == "m":
                robot.back()
            if key == "z":
                robot.left()
            if key == "x":
                robot.right()
            if key == "space":
                robot.pause()

        def release(key):
            print(f"'{key}' released")

        listen_keyboard(
            on_press=press,
            on_release=release,
        )
    except KeyboardInterrupt:
        print("you pressed control c")
