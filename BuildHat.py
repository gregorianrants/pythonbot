import serial
import sys
import time
import re
import threading
from dataclasses import dataclass


class BuildHat():
    FIRMWARE = "Firmware version: "
    BOOT_LOADER = "BuildHAT bootloader version"
    
    def __init__(self):
        self.ser = serial.Serial("/dev/serial0",115200,timeout=1)
        self.motors = [None,None,None,None]
        self.thread = threading.Thread(target=self.listener,args=(),daemon=True)
        self.initialise_hat()
        time.sleep(8)
        self.thread.start()
        
      #methods used when state of hat is unknown, to check if firmware is loaded and load it if it isnt.  
      
    def initialise_hat(self):
        if self.check_if_firmware_loaded():
            return
        self.load_firmware()
        if not self.check_if_firmware_loaded():
            raise Exception('there was a problem initializing the hat')
            
    def check_if_firmware_loaded(self):
        self.write('version')
        line = self.look_for_lines([self.FIRMWARE,
                                    self.BOOT_LOADER],50)
        if line==self.FIRMWARE:
            print('firmware is loaded')
            return True
        if line==self.BOOT_LOADER:
            return False
        raise Exception('got an unexpected response from version command')
            
   
    
    """although we will be using the logging module there are some cases where we dont even want 
    to call it although it doesn't print anything, write will sometimes get called 100 times per second i dont want any unnecessary code in it.  
    """
    def write_and_log(self,message):
        print(f'writing: {message}')
        self.ser.write(f'{message}\r'.encode()) 
        
    def write_bytes(self,bytes):
        print('writing: <some bytes>')
        self.ser.write(bytes)
        
    def read(self):
        line = self.ser.read_until(b'\r\n').decode()
        if len(line)<150: 
            print(f'reading: {line}')
        else:
            print('reading: <long line>')
        return line
    
    def look_for_lines(self,expected_lines,max_lines=10):
        """takes an array of expected_lines and keeps checking the lines returned 
          by serial port till one of them
        matches one of the expected lines, then returns that expected line or false 
        if not found my the time num lines checked = max_lines have been check
        """
        print('looking for:',expected_lines)
        for i in range(max_lines):
            received_line = self.read()
            for expected_line in expected_lines:
                if re.search(r''+expected_line+'',received_line):
                    print('found:', expected_line)
                    return expected_line
        print('line wasnt found within expected number of line reads')
        return False
        
    def get_prompt(self):
        return self.look_for_lines(["BHBL>"])
    
    def checksum(self, data):
        """Calculate checksum from data

        :param data: Data to calculate the checksum from
        :return: Checksum that has been calculated
        """
        u = 1
        for i in range(0, len(data)):
            if (u & 0x80000000) != 0:
                u = (u << 1) ^ 0x1d872b41
            else:
                u = u << 1
            u = (u ^ data[i]) & 0xFFFFFFFF
        return u
        
    def load_firmware(self):
        with open('data/firmware.bin', "rb") as f:
            firm = f.read()
        with open('data/signature.bin', "rb") as f:
            sig = f.read()
        self.get_prompt()
        self.write_and_log('clear')
        self.get_prompt()
        time.sleep(0.1)
        self.write_and_log(f"load {len(firm)} {self.checksum(firm)}")
        time.sleep(0.1)
        self.write_bytes(b'\x02')
        self.write_bytes(firm)
        self.write_bytes(b'\x03')
        self.get_prompt()
        self.write_and_log(f"signature {len(sig)}")
        time.sleep(0.1)
        self.write_bytes(b'\x02')
        self.write_bytes(sig)
        self.write_bytes(b'\x03')
        self.get_prompt()
        self.write_and_log('verify')
        line = self.look_for_lines(['Image verifed OK'],15)
        if line=='Image verifed OK':
            self.write_and_log('reboot')
        time.sleep(5)
        
    #methods used in firmware_loaded state 
      
    def listener(self):
        while True:
            line = self.ser.read_until(b'\r\n').decode()
            #print(line.rstrip())
            self.handle_data(line)
            
    def handle_data(self,line):
        words = line.split()
        if not len(words)>0:
            return
        if not re.search(r"P\dC0",words[0]):
            print(line)
            return 
        port_index = int(words[0][1])
        speed,pos,apos = [int(word) for word in words[1:]]
        
        if(self.motors[port_index]):
            self.motors[port_index].handle_data(speed,pos,apos)
            
    #methods which are part of the interface in firmware loaded state
            
    def add_motor(self,motor):
        self.motors[motor.port_index]=motor
        
    def write(self,message):
        self.ser.write(f'{message}\r'.encode()) 



        
        
    
        
        
   


                
                

