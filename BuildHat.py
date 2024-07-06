import serial
import sys
import time
import re
import threading
from dataclasses import dataclass
import asyncio
import serial_asyncio


class BuildHat:
    FIRMWARE = "Firmware version: "
    BOOT_LOADER = "BuildHAT bootloader version"

    def __init__(self):
        self.reader, self.writer = (None, None)
        self.motors = [None, None, None, None]
        # self.thread = threading.Thread(target=self.listener, args=(), daemon=True)
        # self.initialise_hat()
        # time.sleep(8)
        # self.thread.start()
        # self.count = 0

    # methods used when state of hat is unknown, to check if firmware is loaded and load it if it isnt.

    async def start(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(
            url="/dev/serial0", baudrate=115200
        )
        await self.initialise_hat()
        return asyncio.create_task(self.listener())

    async def initialise_hat(self):
        if await self.check_if_firmware_loaded():
            return
        await self.load_firmware()
        if not await self.check_if_firmware_loaded():
            raise Exception("there was a problem initializing the hat")

    async def check_if_firmware_loaded(self):
        self.write_and_log("version")
        line = await self.look_for_lines([self.FIRMWARE, self.BOOT_LOADER], 50)
        if line == self.FIRMWARE:
            print("firmware is loaded")
            return True
        if line == self.BOOT_LOADER:
            return False
        raise Exception("got an unexpected response from version command")

    """although we will be using the logging module there are some cases where we dont even want 
    to call it although it doesn't print anything, write will sometimes get called 100 times per second i dont want any unnecessary code in it.  
    """

    def write_and_log(self, message):
        print(f"writing: {message}")
        self.writer.write(f"{message}\r".encode())

    def write_bytes(self, bytes):
        print("writing: <some bytes>")
        self.writer.write(bytes)

    async def read(self):
        line = await self.reader.readuntil(b"\r\n")
        print(line)
        line = line.decode()
        if len(line) < 150:
            print(f"reading: {line}")
        else:
            print("reading: <long line>")
        return line

    async def look_for_lines(self, expected_lines, max_lines=10):
        """takes an array of expected_lines and keeps checking the lines returned
          by serial port till one of them
        matches one of the expected lines, then returns that expected line or false
        if not found my the time num lines checked = max_lines have been check
        """
        print("looking for:", expected_lines)
        for i in range(max_lines):
            received_line = await self.read()
            print(received_line)
            for expected_line in expected_lines:
                if re.search(r"" + expected_line + "", received_line):
                    print("found:", expected_line)
                    return expected_line
        print("line wasnt found within expected number of line reads")
        return False

    async def get_prompt(self):
        found_line = await self.look_for_lines(["BHBL>"])
        return found_line

    def checksum(self, data):
        """Calculate checksum from data

        :param data: Data to calculate the checksum from
        :return: Checksum that has been calculated
        """
        u = 1
        for i in range(0, len(data)):
            if (u & 0x80000000) != 0:
                u = (u << 1) ^ 0x1D872B41
            else:
                u = u << 1
            u = (u ^ data[i]) & 0xFFFFFFFF
        return u

    async def load_firmware(self):
        with open("data/firmware.bin", "rb") as f:
            firm = f.read()
        with open("data/signature.bin", "rb") as f:
            sig = f.read()
        print("loading firmware")
        await asyncio.sleep(1)
        # await self.get_prompt()
        self.write_and_log("clear")
        await self.get_prompt()
        await asyncio.sleep(0.1)
        self.write_and_log(f"load {len(firm)} {self.checksum(firm)}")
        await asyncio.sleep(0.1)
        self.write_bytes(b"\x02")
        self.write_bytes(firm)
        self.write_bytes(b"\x03")
        await self.get_prompt()
        self.write_and_log(f"signature {len(sig)}")
        await asyncio.sleep(0.1)
        self.write_bytes(b"\x02")
        self.write_bytes(sig)
        self.write_bytes(b"\x03")
        await self.get_prompt()
        self.write_and_log("verify")
        line = await self.look_for_lines(["Image verifed OK"], 15)
        if line == "Image verifed OK":
            self.write_and_log("reboot")
        await asyncio.sleep(5)

    # methods used in firmware_loaded state

    async def listener(self):
        while True:
            line = (await self.reader.readuntil(b"\r\n")).decode()
            self.handle_data(line)

    def handle_data(self, line):
        # self.count = (self.count + 1) % 100
        # if self.count == 1:
        #     print("line:", line)
        words = line.split()
        if not len(words) > 0:
            return
        if not re.search(r"P\dC0", words[0]):
            print(line)
            return
        port_index = int(words[0][1])
        speed, pos, apos = [int(word) for word in words[1:]]

        if self.motors[port_index]:
            self.motors[port_index].handle_data(speed, pos, apos)

    # methods which are part of the interface in firmware loaded state

    def add_motor(self, motor):
        self.motors[motor.port_index] = motor

    def write(self, message):
        self.writer.write(f"{message}\r".encode())
