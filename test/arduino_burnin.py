import binascii
import struct
from curses import baudrate
from operator import pos

from serial import Serial, SerialException

LED_COUNT = 1000
LED_IDX = 874
LED_COLOR = 126
if __name__ == '__main__':
    COMport = '/dev/ttyACM0'
    size = struct.pack('<H', LED_COUNT)
    idx = struct.pack('<H', LED_IDX)
    led = bytearray(struct.pack('<B', LED_COLOR)) * 3
    countCmd = b'C' + size
    setCmd = b'S' + idx + led
    print(
        '####################################################################################'
    )
    print(countCmd)
    print(setCmd)
    print(
        '####################################################################################'
    )

    ser = Serial(port=COMport, baudrate=9600, timeout=1)
    res = ser.readline()
    while res != b'READY!\r\n':
        res = ser.readline()
        print('Not ready.')
        ...
    print(res)
    print(ser.readline())
    print(
        '####################################################################################'
    )
    # print('send count command')
    # print(ser.write(countCmd))
    # print('get count command result')
    # print(ser.readline())
    # print(ser.readline())
    # print(ser.readline())
    ser.write(countCmd)
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())

    print(
        '####################################################################################'
    )
    print('send set command')
    print(ser.write(setCmd))
    print('get set command result')
    crc = ser.read(34)[:-2]
    crc = int(crc)
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())

    crcComp = 0
    for i in range(LED_IDX):
        crcComp = binascii.crc32(b'\x00\x00\x00', crcComp)
    crcComp = binascii.crc32(b'\x7e\x7e\x7e', crcComp)
    for i in range(LED_IDX + 1, LED_COUNT):
        crcComp = binascii.crc32(b'\x00\x00\x00', crcComp)
    print(
        f'CRC is {crc} and computed as {crcComp} they {"" if crc == crcComp else "dont "}match.'
    )
    # ...
