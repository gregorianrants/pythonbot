import time

class Robot():
    def __init__(self,left_motor_speed,right_motor_speed):
        self.left_motor_speed = left_motor_speed
        self.right_motor_speed = right_motor_speed
        
    def forward(self,speed=500):
        self.pause()
        time.sleep(0.5)
        self.left_motor_speed.set_speed(speed)
        self.right_motor_speed.set_speed(speed)
        
    def back(self,speed=500):
        self.pause()
        time.sleep(0.5)
        self.forward(-speed)
        
    def left(self,speed=300):
        self.pause()
        time.sleep(0.5)
        self.left_motor_speed.set_speed(-speed)
        self.right_motor_speed.set_speed(speed)
        
    def right(self,speed=300):
        self.pause()
        time.sleep(0.5)
        self.left_motor_speed.set_speed(speed)
        self.right_motor_speed.set_speed(-speed)
        
    def pause(self):
        self.left_motor_speed.set_speed(0)
        self.right_motor_speed.set_speed(0)