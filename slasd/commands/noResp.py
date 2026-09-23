"""Fastrak serial commands with no response path."""

from .command import SerialCommand


class SetLedState(SerialCommand):
    """Send a command to the Arduino to set the LED array state."""

    def __init__(
        self,
        data: bytearray,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        data : bytearray
            The data payload to provide to the Arduino.

        """
        self._commandId = 'S'
        self._payload = bytearray()
        self._payload = data
        self._payload += b'\n'
