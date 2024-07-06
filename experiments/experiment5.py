import serial
import time

ser = serial.Serial("/dev/serial0",115200,timeout=1)


ser.write(f'port 2; select\r'.encode())
ser.write(f'port 3; select\r'.encode())
ser.write(f'version\r'.encode())

time.sleep(1)


before = time.time()
ser.write(f'selonce 0\r'.encode())
line = ser.readline()
after = time.time()
print(line)
print(after-before)

# for i in range(100):
#     line = ser.readline()
#     print(line)