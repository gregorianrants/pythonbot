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

I was noticing that robot wasnt going straight when motors given same speed after a pivot manouver (one wheel going back one going forward) i guesses that adding some integral might get rid of this as it would iron out differences between the wheels due to correcting for accumulated differences. adding an integral value of 0.003 seems to make it go more straight and speed control mostly seems good. it may have a bit of kick when starting from 0.

# need to deal with

1. does the pid controller need a reset method. when we go from high speed to 0 or a very different speed there may be some values that hangover from previous speed and have a detrimental effect
   e.g. if we are going at 100 then switch to -100 +ve integral sum values wont be helpfull
   this is less of a problem for smooth changes which we will be doing more often
   i have put something dirty in an if conditional in the update method of PID, may need something more elegant though.
2. remove some comments that i put in when refactoring pid
3. remove the function i used to adjust pid values when refactoring PID.update
4. rename some variables i.e. you have speed variables that refer to multiple things: target_speed and measured_speed be more explicit.
5. need to stop hat emiting data on shutdown

# while working on uploading the firmware to the hat

there is a bug with the hat, when first asked to start emitting data it outputs speed as 0 for a while even when wheels are moving, after initializing the motors need to put a sleep in. I have noticed that when we start a program early on there is an Error message sent by the buildhat. it is difficult to know what this is as there is not more message than "Error". 

the hat has a "debug <debugcode>" command but there is no info in the docs about the parameter debugcode. it seems as though this error has something to do with it emitting 0 speed when moving, the delay i have put in waits for this error message to comeup before getting the motor to do anything. 

found source of the bug, i was using the command 'bias 0.4', the bias command has been deprecated from the firmware there are some comments on this on the github python page.  
https://github.com/RaspberryPiFoundation/python-build-hat/pull/190
there are a few other new commands may want to run the serial 'help' command to the build hat to see the updated commands, there are commands that there is no mention of in the docs.

there is also another one of the sleeps that are important on initialization but i cant remember which.
