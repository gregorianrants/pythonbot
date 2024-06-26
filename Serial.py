import serial
import sys
import time
import re
import threading

class Serial():
    def __init__(self):
        self.ser = serial.Serial("/dev/serial0",115200,timeout=1)
        self.motors = [None,None,None,None]
        self.thread = threading.Thread(target=self.listener,args=(),daemon=True)
        self.thread.start()
        
    def listener(self):
        while True:
            line = self.ser.read_until(b'\r\n').decode()
            #print(line.rstrip())
            self.handle_data(line)
            
    def add_motor(self,motor):
        self.motors[motor.port_index]=motor
        
    def write(self,message):
        self.ser.write(f'{message}\r'.encode())
        
    def handle_data(self,line):
        words = line.split()
        if not len(words)>0:
            return
        if not re.search(r"P\dC0",words[0]):
            return 
        port_index = int(words[0][1])
        speed,pos,apos = [int(word) for word in words[1:]]
        
        if(self.motors[port_index]):
            self.motors[port_index].handle_data(speed,pos,apos)
        
        
        
                
                

