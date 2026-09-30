"""Collection of serial command interfaces."""

from time import sleep
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
        print(cmdBytes + self._payload)


class SerialCommandWithResponse(SerialCommand):
    """Interface describing a generic serial command to a Fastrak with a response."""

    _readLen: int
    _resp: bytes | None

    def parsedResp(self):
        raise NotImplementedError

    def sendRespLine(self, ser: serial.Serial) -> bytes:
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
        self.send(ser)
        self._resp = ser.readline()
        while self._resp == b'':
            self._resp = ser.readline()
        return self._resp

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
        self.send(ser)
        self._resp = ser.read(self._readLen)
        return self._resp
