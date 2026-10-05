import binascii
import struct
from curses import baudrate
from operator import pos

from serial import Serial, SerialException

from slasd.commands.noResp import SetLedCount
from slasd.commands.support import LedColor
from slasd.commands.withResp import SetLedState

LED_COUNT = 1000
LED_IDX = 874
LED_COLOR = 126
if __name__ == '__main__':
    COMport = '/dev/ttyACM0'
    ser = Serial(port=COMport, baudrate=9600, timeout=1)
    res = ser.readline()
    while res != b'READY!\r\n':
        res = ser.readline()
        print('Not ready.')
        ...
    print(res)
    print(ser.readline())
    SetLedCount(LED_COUNT).send(ser)
    color = LedColor(red=LED_COLOR, green=LED_COLOR, blue=LED_COLOR)
    stateCmd = SetLedState(LED_IDX, color)
    stateCmd.sendRespLine(ser)
    crc = stateCmd.parsedResp()

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
