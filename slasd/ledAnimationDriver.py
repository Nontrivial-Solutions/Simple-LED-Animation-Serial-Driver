"""Base class for an LED animation driver."""

from time import sleep

import serial
from serial import Serial

from slasd.commands.support import LedColor

from .commands.noResp import SetLedCount
from .commands.withResp import SetLedState


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

    """

    _ser: Serial | None
    _COMport: str
    _baud: int
    _timeout: int
    _ledCount: int
    _color: LedColor

    def __init__(
        self,
        COMport: str = 'COM1',
        baud: int = 9600,
        timeout: int = 1,
        ledCount: int = 1000,
        setup: bool = True,
        color: LedColor = LedColor(red=0, blue=0, green=0),
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
            while res != b'READY!\r\n':
                res = self._ser.readline()
            self._ser.readline()
            sleep(0.01)
            SetLedCount(self._ledCount).send(self._ser)

    def _computeState(self, **kwargs) -> tuple[list[SetLedState], int]:
        """State computation interface.

        Parameters
        ----------
        **kwargs: dict
            Collection of keyword arguments. Unique to each animation class.


        Returns
        -------
        tuple[list[SetLedState], int]
            A tuple containing first a collection of commands to send (in order) to the Arduino.
            Second the [CRC32](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) of the new
            state of the LED array.
        """
        raise NotImplementedError

    def compNSndState(self, **kwargs) -> None:
        """Compute and set the state of the LED array.

        Parameters
        ----------
        **kwargs : dict
            Collection of keyword arguments. Unique to each animation class.

        """
        if self._ser is None:
            raise TypeError

        commands, crc = self._computeState(**kwargs)

        for command in commands[:-1]:
            command.send(self._ser)

        commands[-1].sendRespLine(self._ser)
        crcFromDev = commands[-1].parsedResp()

        if crc != crcFromDev:
            raise Exception('an error occurred')  # TODO: Add specific Exception
