"""Fastrak serial commands with no response path."""

import struct

from .command import SerialCommandWithResponse
from .support import LedColor


class SetLedState(SerialCommandWithResponse):
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
        self._payload = bytearray(struct.pack('<H', idx))
        self._payload += color.to_bytes()
        self._payload += b'\n'
        self._resp = None

    def parsedResp(self) -> int | None:
        """Parse the response into an integer
        [CRC32](https://en.wikipedia.org/wiki/Cyclic_redundancy_check).

        Returns
        -------
        int | None
            When the response exists an int. Otherwise, response is None.


        """
        if self._resp is None or self._resp == b'':
            return None
        return int(self._resp[:-2])
