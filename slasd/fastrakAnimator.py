"""Contains the Fastrak device angular illuminator class."""

import struct
from math import floor
from typing import TypedDict

from fastrakSerialDriver.fastrakPosition import FastrakPostion
from typing_extensions import Unpack

from .ledAnimationDriver import LedAnimationDevice


class FastrakParams(TypedDict):
    r"""Describe the typing of the kwargs for the Fastrak animation state computation.

    Attributes
    ----------
    posData : FastrakPostion
        A position reported by a Fastrak hardware device.
    angleToLight : int
        The angular range $\\theta$, in degrees, to light up. In the example below the `O`
        correspond to lit LED and `X` to unlit LED.
        ```ascii
                         OOOOOOOOOOO
                    OOOOO           OOOOO
                  OO                     OO
                XO           θ           .'XX
               X  `.      -------      .'    X
              X     `.  /         \  .'       X
             X        `.            /          X
            X           `.        .'            X
           X                ,-. .'               X
           X              _(*_*)_                X
           X             (_  o  _)               X
           X               / o \                 X
           X              (_/ \_)                X
            X                                   X
             X                                 X
              X                               X
               X                             X
                XX                         XX
                  XX                     XX
                    XXXXX           XXXXX
                         XXXXXXXXXXX
        ```

    colorR : int
        The red component of the LED lit color.
    colorG : int
        The green component of the LED lit color.
    colorB : int
        The blue component of the LED lit color.
    """

    posData: FastrakPostion
    angleToLight: int
    colorR: int
    colorG: int
    colorB: int


class FastrakAnimationDevice(LedAnimationDevice):
    """Implements LedAnimationDevice for the Fastrak look position use case."""

    def _computeState(self, **kwargs: Unpack[FastrakParams]) -> bytearray:  # ty:ignore[invalid-method-override]
        """Compute the state array for the LED in the Fastrak look position use case.

        Parameters
        ----------
         **kwargs : Unpack[FastrakParams]
            Collection of key word arguments for the Fastrak look position use case.

        Returns
        -------
        bytearray
            The on/off and color state for each LED in the array.


        """
        if (
            kwargs is None
            or 'posData' not in kwargs
            or 'angleToLight' not in kwargs
            or 'colorR' not in kwargs
            or 'colorG' not in kwargs
            or 'colorB' not in kwargs
            or type(kwargs['posData']) is not FastrakPostion
            or type(kwargs['angleToLight']) is not int
            or type(kwargs['colorR']) is not int
            or type(kwargs['colorG']) is not int
            or type(kwargs['colorB']) is not int
        ):
            raise TypeError

        if kwargs['colorR'] < 0 or kwargs['colorR'] > 255:
            raise TypeError
        if kwargs['colorG'] < 0 or kwargs['colorG'] > 255:
            raise TypeError
        if kwargs['colorB'] < 0 or kwargs['colorB'] > 255:
            raise TypeError

        byteCr = struct.pack('<B', kwargs['colorR'])
        byteCg = struct.pack('<B', kwargs['colorG'])
        byteCb = struct.pack('<B', kwargs['colorB'])

        if len(byteCb) != 1 or len(byteCg) != 1 or len(byteCr) != 1:
            raise TypeError

        pos = kwargs['posData']
        lightAngle = kwargs['angleToLight']
        litCenterLed = floor((self._ledCount / 360) * pos.psi)
        lookAngleCnt = floor((self._ledCount / 360) * lightAngle)
        payload = bytearray(b'\0' * (3 * self._ledCount))

        for i in range(
            floor(litCenterLed - (lookAngleCnt / 2)),
            litCenterLed,
            3,
        ):
            payload[i] = byteCr[0]
            payload[i + 1] = byteCg[0]
            payload[i + 2] = byteCb[0]

        for i in range(
            litCenterLed,
            floor(litCenterLed + (lookAngleCnt / 2)) + 1,
            3,
        ):
            payload[i] = byteCr[0]
            payload[i + 1] = byteCg[0]
            payload[i + 2] = byteCb[0]

        return payload
