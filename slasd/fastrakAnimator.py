"""Contains the Fastrak device angular illuminator class."""

import binascii
import struct
from math import floor
from typing import TypedDict

from fastrakSerialDriver.fastrakPosition import FastrakPostion
from typing_extensions import Unpack

from slasd.commands.withResp import SetLedState

from .commands.support import LedColor
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
                         OOOOOZOOOOO
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
                         XXXXXTXXXXX
        ```

    zeroLED: int
        The LED that serves as the "zero point" for the LED circle. In the example above `T`
        indicates the "true" zero (first physical LED on the strand) and `Z` indicates the offset
        zero.
    """

    posData: FastrakPostion
    angleToLight: int
    zeroLED: int


class FastrakAnimationDevice(LedAnimationDevice):
    """Implements LedAnimationDevice for the Fastrak look position use case."""

    def _computeState(
        self, **kwargs: Unpack[FastrakParams]
    ) -> tuple[list[SetLedState], int]:  # ty:ignore[invalid-method-override]
        """Compute the state array for the LED in the Fastrak look position use case.

        Parameters
        ----------
         **kwargs : Unpack[FastrakParams]
            Collection of key word arguments for the Fastrak look position use case.

        Returns
        -------
        tuple[list[SetLedState], int]
            A tuple containing first a collection of commands to send (in order) to the Arduino.
            Second the [CRC32](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) of the new
            state of the LED array.

        """
        if (
            kwargs is None
            or 'posData' not in kwargs
            or 'angleToLight' not in kwargs
            or 'zeroLED' not in kwargs
            or type(kwargs['posData']) is not FastrakPostion
            or type(kwargs['angleToLight']) is not int
            or type(kwargs['zeroLED']) is not int
        ):
            raise TypeError

        pos = kwargs['posData']
        lightAngle = kwargs['angleToLight']
        zeroLED = kwargs['zeroLED']
        litCenterLed = floor((self._ledCount / 360) * pos.psi)
        lookAngleCnt = floor((self._ledCount / 360) * lightAngle)

        commands = []
        crcComp = 0

        for _ in range(
            floor(litCenterLed - (lookAngleCnt / 2)),
        ):
            crcComp = binascii.crc32(b'\x00\x00\x00', crcComp)

        for i in range(
            floor(litCenterLed - (lookAngleCnt / 2)),
            floor(litCenterLed + (lookAngleCnt / 2)) + 1,
        ):
            colorBytes = self._color.to_bytes()
            commands.append(SetLedState((i + zeroLED) % self._ledCount, self._color))
            crcComp = binascii.crc32(colorBytes, crcComp)

        for _ in range(floor(litCenterLed + (lookAngleCnt / 2)) + 1, self._ledCount):
            crcComp = binascii.crc32(b'\x00\x00\x00', crcComp)

        return commands, crcComp
