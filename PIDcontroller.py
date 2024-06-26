# class PIController:
#     def __init__(self, proportional_constant=0, integral_constant=0,derivative_constant=0):
#         self.proportional_constant = proportional_constant
#         self.integral_constant = integral_constant
#         self.derivative_constant = derivative_constant
#         # Running sums
#         self.integral_sum = 0
#         self.previous = 0
        
#     def handle_proportional(self,error):
#       return self.proportional_constant * error
  
#     def handle_integral(self,error):
#       self.integral_sum += error
#       return self.integral_constant * error
  
#     def handle_derivative(self,error):
#        derivative = self.derivative_constant*(error - self.previous)
#        self.previous = error
#        return derivative

#     def get_value(self,error):
#       p=self.handle_proportional(error)
#       i=self.handle_integral(error)
#       d= self.handle_derivative(error)
#       return p+i+d

# class MotorSpeed:
#    def __init__(self,motor,set_point=0):
#       self.motor = motor
#       self.p = 0.001
#       self.k = 0
#       self.d = 0.002
#       self.pid = PIController(self.p,self.k,self.d)
#       ##power should probably be passed by previouse behaviour
#       self.power=0
#       self.errors = []
#       self.set_point = set_point
#       self.running = False

#    def update(self,speed):
#       if(self.set_point==0):
#          self.power = 0
#          self.motor.pwm(0)
#          return
#       error = speed-self.set_point
#       self.errors.append(error)
#       adjustment = self.pid.get_value(error)
#       self.power = self.power-adjustment
#       self.motor.pwm(self.power)
      
#    def set_speed(self,speed):
#       self.set_point = speed

#    def start(self):
#       self.running = True
#       self.motor.pwm(self.power)
#       self.motor.add_listener(self.update)

#    def stop(self):
#       self.motor.remove_listener()
#       self.motor.pwm(0)


class PIDController:
   def __init__(self, 
                 proportional_constant=0, 
                 integral_constant=0,
                 derivative_constant=0,
                 process_variable=0,
                 power=0):
       
      self.proportional_constant = proportional_constant
      self.integral_constant = integral_constant
      self.derivative_constant = derivative_constant
      # Running sums
      self.integral_sum = 0
      self.previous = 0
      self.process_variable = process_variable
      self.power = power
      self.set_point = 0
        
   def handle_proportional(self,error):
      return self.proportional_constant * error
  
   def handle_integral(self,error):
      self.integral_sum += error
      return self.integral_constant * error
  
   def handle_derivative(self,error):
      derivative = self.derivative_constant*(error - self.previous)
      self.previous = error
      return derivative

   def get_value(self,error):
      p=self.handle_proportional(error)
      i=self.handle_integral(error)
      d= self.handle_derivative(error)
      return p+i+d
   
   def update(self,speed):
      if(self.set_point==0):
         self.power = 0
         print('hello')
         return self.power
      error = speed-self.set_point
      adjustment = self.get_value(error)
      self.power = self.power-adjustment
      return self.power
   
   def set_point(self,set_point):
      self.set_point = set_point
      
      
   
   

