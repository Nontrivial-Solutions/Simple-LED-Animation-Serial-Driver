from fastrakSerialDriver.fastrakPosition import FastrakPostion

from slasd.commands.support import LedColor
from slasd.fastrakAnimator import FastrakAnimationDevice

LED_COUNT = 1000
LED_IDX = 874
LED_COLOR = 126
if __name__ == '__main__':
    COMport = '/dev/ttyACM0'
    print('init and connect')
    col = LedColor(red=LED_COLOR, green=LED_COLOR, blue=LED_COLOR)
    fad = FastrakAnimationDevice(COMport, ledCount=LED_COUNT, color=col)
    print('setup data')
    ft = FastrakPostion(x=0, y=0, z=0, psi=180, theta=0, phi=0)
    print('set state')
    fad.compNSndState(posData=ft, angleToLight=5, zeroLED=0)
    print('Done!')
    ...
