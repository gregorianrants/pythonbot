from BuildHat import BuildHat as Serial
from Motor import Motor
from Robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard

serial = Serial()
left_motor = Motor('C',serial,-1)
right_motor = Motor('D',serial,1)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    left_motor.run(0)
    right_motor.run(0)
    time.sleep(1)
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

robot = Robot(left_motor,right_motor)


    
def press(key):
    print(f"'{key}' pressed")
    if key=='k':
        robot.forward()
    if key=='m':
        robot.back()
    if key=='z':
        robot.left()
    if key=='x':
        robot.right()
    if key=='space':
        robot.pause()

def release(key):
    print(f"'{key}' released")

listen_keyboard(
    on_press=press,
    on_release=release,
)
