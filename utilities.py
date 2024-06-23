import math

def clamp(num):
    math.copysign(1,num)*abs(num)-math.floor(abs(num))
    
    
print(clamp())