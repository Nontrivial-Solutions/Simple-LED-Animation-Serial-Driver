"""Collection of serial command interfaces."""

from time import sleep
from typing import Protocol

import serial

from slasd.commands.support import ACK_STR


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

    def send(self, ser: serial.Serial, ackCheck: bool = True) -> None:
        """Send a single serial command to the Arduino.

        Parameters
        ----------
        ser : serial.Serial
            Serial connection to send the frame on.


        """
        cmdBytes = bytes(self._commandId, 'ASCII')
        ser.write(cmdBytes + self._payload)
        ser.flush()
        if ackCheck:
            resp = ser.readline()
            if resp[:-2] != ACK_STR:
                print(resp)
                raise Exception('an error occurred')  # TODO: Add specific Exception


class SerialCommandWithResponse(SerialCommand):
    """Interface describing a generic serial command to a Fastrak with a response."""

    _readLen: int
    _resp: bytes | None

    def parsedResp(self) -> object:
        """Parse the response data into a meaningful object.

        Returns
        -------
        object
            A meaningful object representation of the response data.


        """
        raise NotImplementedError

    def sendRespLine(self, ser: serial.Serial) -> bytes:
        r"""Send a single serial command to a Fastrak. Read a single `\n` terminated line.

        Parameters
        ----------
        ser : serial.Serial
            Serial connection to send the frame on.

        Returns
        -------
        bytes
            Response data from Fastrak.


        """
        self.send(ser, ackCheck=False)
        self._resp = ser.readline()
        return self._resp

    def sendResp(self, ser: serial.Serial) -> bytes:
        """Send a single serial command to a Fastrak. Read $n$ bytes from the serial interface.

        Parameters
        ----------
        ser : serial.Serial
            Serial connection to send the frame on.

        Returns
        -------
        bytes
            Response data from Fastrak.


        """
        self.send(ser, ackCheck=False)
        self._resp = ser.read(self._readLen)
        return self._resp
