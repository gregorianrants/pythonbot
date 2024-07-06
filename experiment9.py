from BuildHat import BuildHat as Serial
from Motor import Motor
from Robot import Robot
import time
import signal
import sys
import asyncio

import os


# class Cancel:
#     def __init__(self, motor):
#         self.motor = motor

#     async def cancel(self, sif, frame):
#         print("You pressed Ctrl+C!")
#         self.motor.run(0)
#         await asyncio.sleep(1)
#         sys.exit(0)


async def main():
    serial = Serial()
    task1 = await serial.start()
    motor = Motor("C", serial)
    # cancel = Cancel(motor)
    # signal.signal(signal.SIGINT, cancel.cancel)
    motor.run(400)
    await asyncio.sleep(10)
    await motor.clean_up()


asyncio.run(main())
