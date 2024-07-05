import asyncio
import serial_asyncio


async def main(loop):
    # "/dev/serial0", 115200
    reader, writer = await serial_asyncio.open_serial_connection(
        url="/dev/serial0", baudrate=115200
    )
    # print("Reader created")
    # _,  = await serial_asyncio.open_serial_connection(
    #     url="/dev/serial0", baudrate=115200
    # )
    sent = await send(writer, b"version\r")
    for i in range(50):
        await recv(reader)


async def send(w, msg):
    w.write(msg)
    print(f"sent: {msg}")
    # await asyncio.sleep(0.5)
    print("Done sending")


async def recv(r):
    msg = await r.readuntil(b"\n")
    print(f"received: {msg}")
    return msg


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
