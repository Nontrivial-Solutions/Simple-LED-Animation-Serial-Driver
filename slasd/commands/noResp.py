"""Fastrak serial commands with no response path."""

import struct

from slasd.commands.support import LedColor

from .command import SerialCommand


class SetLedCount(SerialCommand):
    """Send a command to the Arduino to set the count for number of LED."""

    def __init__(
        self,
        count: int,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        count : int
            The number of LED in the array.

        """
        self._commandId = 'C'
        self._payload = bytearray(str(count), 'utf-8')
        self._payload += b'\n'


class CmdShow(SerialCommand):
    """Send a command to the Arduino to command every LED off."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'H'
        self._payload = bytearray()
        self._payload += b'\n'


class SetLedOff(SerialCommand):
    """Send a command to the Arduino to command every LED off."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'O'
        self._payload = bytearray()
        self._payload += b'\n'


class SetLedState(SerialCommand):
    """Send a command to the Arduino to set the LED array state."""

    def __init__(
        self,
        idx: int,
        color: LedColor,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        data : bytearray
            The data payload to provide to the Arduino.

        """
        self._commandId = 'S'
        self._readLen = 34
        self._payload = bytearray(str(idx), 'ASCII')
        self._payload += b':'
        self._payload += color.to_ascii()
        self._payload += b'\n'
        self._resp = None
