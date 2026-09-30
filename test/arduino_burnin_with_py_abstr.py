from fastrakSerialDriver.fastrakPosition import FastrakPostion

from slasd.commands.support import LedColor
from slasd.fastrakAnimator import FastrakAnimationDevice

if __name__ == '__main__':
    COMport = '/dev/ttyACM0'
    print('init and connect')
    fad = FastrakAnimationDevice(COMport)
    print('setup data')
    ft = FastrakPostion(x=0, y=0, z=0, psi=180, theta=0, phi=0)
    col = LedColor(red=126, green=126, blue=126)
    print('set state')
    fad.compNSndState(posData=ft, angleToLight=5, zeroLED=0, color=col)
    ...
