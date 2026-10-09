import binascii
import struct
from operator import pos

from serial import Serial, SerialException

LED_COUNT = 1000
LED_IDX = 874
LED_COLOR = 126
if __name__ == '__main__':
    COMport = '/dev/ttyACM0'
    size = bytearray(str(LED_COUNT), 'ASCII')
    idx = bytearray(str(LED_IDX), 'ASCII')
    led = bytearray(str(LED_COLOR), 'ASCII')
    countCmd = b'C' + size
    crcCmd = b'R'
    showCmd = b'H'
    setCmd = b'S' + idx + b':' + led + b':' + led + b':' + led
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
    while res != b'ACK\r\n':
        res = ser.readline()
        print('Not ready.')
        ...
    print(res)
    print(ser.readline())
    print(
        '####################################################################################'
    )
    ser.write(countCmd)

    print(
        '####################################################################################'
    )
    print('send set command')
    ser.write(setCmd)
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())

    print('get set command result')
    ser.write(crcCmd)
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    crc = ser.readline()
    while crc == b'':
        crc = ser.readline()
        ...
    print(crc)

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
