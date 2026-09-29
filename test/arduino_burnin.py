import struct
from curses import baudrate
from operator import pos

from serial import Serial, SerialException

LED_COUNT = 255

if __name__ == '__main__':
    COMport = '/dev/ttyACM0'
    commandId = b'S'
    size = struct.pack('<H', LED_COUNT)
    idx = struct.pack('<H', 10)
    led = bytearray(struct.pack('<B', 255)) * 3
    countCmd = b'C' + size
    setCmd = commandId + idx + led
    print(
        '####################################################################################'
    )
    print(setCmd)
    print(countCmd)
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
    print('send count command')
    print(ser.write(countCmd))
    print('get count command result')
    print(ser.readline())
    print(ser.readline())
    print('send set command')
    print(ser.write(setCmd))
    print('get set command result')
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    print(ser.readline())
    ...
