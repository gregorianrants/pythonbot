## commit: refactored so that Motor.run() takes a speed in degrees_per_second in…

prior to this the pid values were 
p,i,d = 0.001,0,0.02

i then wanted to change the units that speed was set on motor in via Motor.run from mm/second
to degrees per second

basically PIDcontroller is now sent speed in degrees per second so it is as though the proccess variable has been multiplied by a factor call it 'a' that does this we then need to multiply the pid values by its inverse 
inverse(a) to make the math work out

i used a function to do this but will remove this later and hard code it.


## commit: hardcoded the new pid values
the new pid values are now hardcoded  

## commit: changed integral value in PIDcontroller instance creation in Motor
I was noticing that robot wasnt going straight when motors given same speed after a pivot manouver (one wheel going back one going forward) i guesses that adding some integral might get rid of this as it would iron out differences between the wheels due to correcting for accumulated differences.  adding an integral value of 0.003 seems to make it go more straight and speed control mostly seems good. it may have a bit of kick when starting from 0.


# need to deal with

1. does the pid controller need a reset method. when we go from high speed to 0 or a very different speed there may be some values that hangover from previous speed and have a detrimental effect
e.g. if we are going at 100 then switch to -100 +ve integral sum values wont be helpfull
this is less of a problem for smooth changes which we will be doing more often
i have put something dirty in an if conditional in the update method of PID, may need something more elegant though.
2.  remove some comments that i put in when refactoring pid
3. remove the function i used to adjust pid values when refactoring PID.update
4. rename some variables i.e. you have speed variables that refer to multiple things: target_speed and measured_speed be more explicit.