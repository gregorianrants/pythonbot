from src.BuildHat import BuildHat as Serial
from src.Motor import Motor
from src.Robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard

with Serial() as serial:
    left_motor = Motor("C", serial, -1)
    right_motor = Motor("D", serial, 1)

    left_motor.add_listener(print)

    def signal_handler(sig, frame):
        print("You pressed Ctrl+C!")
        left_motor.clean_up()
        right_motor.clean_up()
        time.sleep(1)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

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
