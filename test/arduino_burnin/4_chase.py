from fastrakSerialDriver.fastrakPosition import FastrakPostion
from tqdm import tqdm

from slasd.commands.support import LedColor
from slasd.fastrakAnimator import FastrakAnimationDevice

LED_COUNT = 500
LED_IDX = 874
LED_COLOR = 126
if __name__ == '__main__':
    COMport = '/dev/ttyACM0'
    print('init and connect')
    col = LedColor(red=LED_COLOR, green=LED_COLOR, blue=LED_COLOR)
    fad = FastrakAnimationDevice(COMport, ledCount=LED_COUNT, color=col)
    for i in tqdm(range(1, LED_COUNT)):
        for j in tqdm(range(380), leave=False):
            ft = FastrakPostion(x=0, y=0, z=0, psi=i, theta=0, phi=0)
            fad.compNSndState(posData=ft, angleToLight=j, zeroLED=0)
            ...
