import sys
import time
from src.Motor import Motor
from BuildHat import BuildHat as  Serial
from src.Robot import Robot
from MotorSpeed import MotorSpeed
from sshkeyboard import listen_keyboard
import signal

count = 0


ser = Serial()
ser.start()
left_motor = Motor('C',ser,-1)
right_motor = Motor('D',ser)
left_motor_s = MotorSpeed(left_motor)
right_motor_s = MotorSpeed(right_motor)
left_motor_s.start()
right_motor_s.start()

def signal_handler(sig, frame):
    print('you pressed Ctrl+C')
    robot.pause()
    time.sleep(1)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



robot = Robot(left_motor_s,right_motor_s)

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




   

    
    
    
  
    