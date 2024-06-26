## commit notes

commit: refactored so that Motor.run() takes a speed in degrees_per_second in…

prior to this the pid values were 
p,i,d = 0.001,0,0.02

i then wanted to change the units that speed was set on motor in via Motor.run from mm/second
to degrees per second

basically PIDcontroller is now sent speed in degrees per second so it is as though the proccess variable has been multiplied by a factor call it 'a' that does this we then need to multiply the pid values by its inverse 
inverse(a) to make the math work out

i used a function to do this but will remove this later and hard code it.
