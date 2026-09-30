"""Fastrak serial commands with no response path."""

import struct

from .command import SerialCommand


class SetLedCount(SerialCommand):
    """Send a command to the Arduino to set the LED array state."""

    def __init__(
        self,
        count: int,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        data : bytearray
            The data payload to provide to the Arduino.

        """
        self._commandId = 'C'
        self._payload = bytearray()
        self._payload += struct.pack('<H', count)
        self._payload += b'\n'
