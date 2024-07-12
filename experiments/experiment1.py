from Serial import Serial
from src.Motor import Motor
from MotorSpeed import MotorSpeed
import time


serial = Serial()
left_motor = Motor('C',serial,-1)
motor_speed = MotorSpeed(left_motor)
motor_speed.start()
serial.start()
time.sleep(10)
motor_speed.stop()

