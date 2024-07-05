from BuildHat import BuildHat as Serial
from Motor import Motor
from Robot import Robot
import time
import signal
import sys
import asyncio

import os


async def main():
    serial = Serial()
    await serial.start()


asyncio.run(main())
