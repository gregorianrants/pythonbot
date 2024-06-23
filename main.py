from buildhat import Motor
import time


print('imports done')
left = Motor('C')
right = Motor('D')

right.start(0.2)
left.start(0.2)


time.sleep(1)

right.stop()
left.stop()