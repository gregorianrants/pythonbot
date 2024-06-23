import math

class Motor():
    PORTS = ['A','B','C','D']
    def __init__(self,port,ser,direction=1):
        self.port_letter = port
        self.port_index = self.PORTS.index(port)
        self.mode = 0
        self.ser = ser
        self.ser.add_motor(self)
        self.set_combi_mode()
        self.set_bias()
        self.set_plimit()
        self.listener = lambda speed: 0
        self.count = 0
        self.direction = direction
        self.wheel_diameter = 276 #mm
        
    def write(self,message):
        full_message = f'port {self.port_index}; {message}'
        self.ser.write(full_message)
        
    def set_combi_mode(self):
        self.write(f'select 0; selrate 10')
        
    def set_plimit(self):
        self.write(f'plimit 1')
        
    def set_bias(self):
        self.write(f'bias 0.4')
        
    def set_power(self,power=0.2):
        pass
        #self.write(f'set {power}')
        
    def pwm(self,pwm):
        pwm = (pwm * self.direction)/100
        if(pwm>1 or pwm<-1):
          print('pwm must be between -1 and 1')
          pwm=math.copysign(1,pwm)*1
        data = f'set {pwm};'
        self.write(data)
        
    def getSpeed(self,aSpeed):
         speed =  (aSpeed/36)*self.wheel_diameter
         return speed
    
    def getDistance(self,pos):
         distance = pos/360*self.wheel_diameter
         return distance
     
    def add_listener(self,listener):
        self.listener = listener
        
    def remove_listener(self):
        self.listener = lambda speed: 0
        
    def handle_data(self,speed,pos,apos):
        self.count = (self.count+1)%100
        if self.count==1:
            sentence = f'port: {self.port_letter}, speed_10deg/sec: {speed}, speed_mm/s: {speed*(1/36)*276.401},pos: {pos}, apos: {apos}'
            print(sentence)
        speed = self.direction * self.getSpeed(speed)
        self.listener(speed)
        
    def __str__(self):
        return f'Motor PortIndex:{self.port_index}, Port: {self.port_letter}'
