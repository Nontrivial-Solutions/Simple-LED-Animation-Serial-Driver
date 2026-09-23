"""Collection of serial command interfaces."""

from typing import Protocol

import serial


class SerialCommand(Protocol):
    """Interface describing a generic serial command to the Arduino.

    Attributes
    ----------
    _commandId : str
        ID of the command. Usually a single ASCII char.
    _payload : bytearray
        Data payload to send with command.

    """

    _commandId: str
    _payload: bytearray

    def send(self, ser: serial.Serial) -> None:
        """Send a single serial command to the Arduino.

        Parameters
        ----------
        ser : serial.Serial
            Serial connection to send the frame on.


        """
        cmdBytes = bytes(self._commandId, 'ASCII')
        ser.write(cmdBytes + self._payload)
