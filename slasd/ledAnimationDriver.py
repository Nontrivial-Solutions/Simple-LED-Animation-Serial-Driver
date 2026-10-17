"""Base class for an LED animation driver."""

import binascii
from time import sleep

from serial import Serial

from slasd.commands.support import LedColor

from .commands.noResp import CmdShow, SetLedCount, SetLedOff, SetLedState
from .commands.support import ACK_STR
from .commands.withResp import GetCrc


class LedAnimationDevice:
    """Defines interface for connecting, setting up, and streaming from a Fastrak.

    Attributes
    ----------
    _ser : Serial | None
        Serial connection to an Arduino.

    _COMport :
        String representing the COM port to be connected to.

    _baud : SerialBaudrates
        Baudrate for the serial connection.

    _timeout : int, default: 1second
        Serial timeout for the connection.

    _ledCount: int
        The number of LED in the array.

    _color : LedColor
        The color of a lit LED.

    _ledMirror: list[LedColor]
        A mirror of the LED array used for computing CRC32.

    """

    _ser: Serial | None
    _COMport: str
    _baud: int
    _timeout: int
    _ledCount: int
    _color: LedColor
    _ledMirror: list[LedColor]

    def __init__(
        self,
        COMport: str = 'COM4',
        baud: int = 9600,
        timeout: int = 1,
        ledCount: int = 1000,
        setup: bool = True,
        color: LedColor | None = None,
    ) -> None:
        """Construct a LedAnimationDevice class.

        Parameters
        ----------
        COMport : str
            String representing the COM port to be connected to.

        baud : int, default: 1115200
            Baudrate for the serial connection.

        timeout : int, default: 1second
            Serial timeout for the connection.

        ledCount: int, defualt: 100
            The number of LED in the array.

        setup : int, default: True
            Flag indicating if the device should connect to the serial interface.

        color : LedColor, default: #000000
            The color to command a lit LED to be.

        """
        if color is None:
            color = LedColor(red=0, blue=0, green=0)

        self._ser = None
        self._COMport = COMport
        self._baud = baud
        self._timeout = timeout
        self._ledCount = ledCount
        self._color = color

        if setup:
            self.connect()

    def connect(self) -> None:
        """Connect to the serial device."""
        if self._ser is not None:
            if not self._ser.is_open:
                self._ser.open()
        else:
            self._ser = Serial(self._COMport, self._baud, timeout=self._timeout)
            res = self._ser.readline()
            while res[:-2] != ACK_STR:
                res = self._ser.readline()
            self._ser.readline()
            sleep(0.1)
            SetLedCount(self._ledCount).send(self._ser)
            sleep(0.1)
            self._ledMirror = [LedColor(0, 0, 0)] * self._ledCount

    def _compCrc(self) -> int:
        """Compute the CRC32 of the led array mirror.

        Returns
        -------
        int
            The [CRC32](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) of the new
            state of the LED array.
        """
        crcComp = 0

        for led in self._ledMirror:
            colorBytes = led.to_bytes()
            crcComp = binascii.crc32(colorBytes, crcComp)
        return crcComp

    def _computeState(self, **kwargs) -> list[SetLedState]:
        """State computation interface.

        Parameters
        ----------
        **kwargs: dict
            Collection of keyword arguments. Unique to each animation class.


        Returns
        -------
        list[SetLedState]
            The collection of commands to send (in order) to the Arduino.
        """
        raise NotImplementedError

    def setOff(self):
        """Set the LED array off."""
        if self._ser is None:
            raise TypeError
        SetLedOff().send(self._ser)
        self._ledMirror = [LedColor(0, 0, 0)] * self._ledCount

        crcFromDev = GetCrc()
        crcFromDev.sendRespLine(self._ser)

        if self._compCrc() != crcFromDev.parsedResp():
            print(crcFromDev._resp)
            raise Exception('an error occurred')  # TODO: Add specific Exception
        CmdShow().send(self._ser)

    def compNSndState(self, **kwargs) -> None:
        """Compute and set the state of the LED array.

        Parameters
        ----------
        **kwargs : dict
            Collection of keyword arguments. Unique to each animation class.

        """
        if self._ser is None:
            raise TypeError

        commands = self._computeState(**kwargs)

        for command in commands:
            command.send(self._ser)

        crcFromDev = GetCrc()
        crcFromDev.sendRespLine(self._ser)

        if self._compCrc() != crcFromDev.parsedResp():
            print(crcFromDev._resp)
            raise Exception('an error occurred')  # TODO: Add specific Exception
        CmdShow().send(self._ser)
