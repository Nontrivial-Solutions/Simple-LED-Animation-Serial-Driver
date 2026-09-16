"""Collection of serial command interfaces."""

from typing import Protocol

import serial


class SerialCommand(Protocol):
    """Interface describing a generic serial command to a Fastrak.

    Attributes
    ----------
    _commandId : str
        ID of the command. Usually a single ASCII char.
    _payload : str
        Data payload to send with command.

    """

    _commandId: str
    _payload: str

    def send(self, ser: serial.Serial) -> None:
        """Send a single serial command to a Fastrak.

        Parameters
        ----------
        ser : serial.Serial
            Serial connection to send the frame on.


        """
        ser.write(f'{self._commandId}{self._payload}'.encode(encoding='ASCII'))


class SerialCommandWithResponse(SerialCommand):
    """Interface describing a generic serial command to a Fastrak with a response."""

    def sendResp(self, ser: serial.Serial) -> bytes:
        """Send a single serial command to a Fastrak.

        Parameters
        ----------
        ser : serial.Serial
            Serial connection to send the frame on.

        Returns
        -------
        bytes
            Response data from Fastrak.


        """
        ser.write(f'{self._commandId}{self._payload}'.encode(encoding='ASCII'))
        return ser.readline()
