"""Base class for an LED animation driver."""

from serial import Serial

from .commands.noResp import SetLedState


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

    """

    _ser: Serial | None
    _COMport: str
    _baud: int
    _timeout: int
    _ledCount: int

    def __init__(
        self,
        COMport: str = 'COM1',
        baud: int = 115200,
        timeout: int = 1,
        ledCount: int = 100,
        setup: bool = True,
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

        """
        self._ser = None
        self._COMport = COMport
        self._baud = baud
        self._timeout = timeout
        self._ledCount = ledCount
        if setup:
            self.connect()

    def connect(self) -> None:
        """Connect to the serial device."""
        if self._ser is not None:
            if not self._ser.is_open:
                self._ser.open()
        else:
            self._ser = Serial(self._COMport, self._baud, timeout=self._timeout)

    def _sendState(self, data: bytearray) -> None:
        """Send state data to the serial device.

        Parameters
        ----------
        data : bytearray
            LED array state data to send to the device.


        """
        if self._ser is not None:
            SetLedState(data).send(self._ser)

    def _computeState(self, **kwargs) -> bytearray:
        """State computation interface.

        Parameters
        ----------
        **kwargs: dict
            Collection of keyword arguments. Unique to each animation class.


        Returns
        -------
        bytearray
            The computed state of the LED array.


        """
        raise NotImplementedError

    def compNSndState(self, **kwargs) -> None:
        """Compute and set the state of the LED array.

        Parameters
        ----------
        **kwargs : dict
            Collection of keyword arguments. Unique to each animation class.

        """
        payload = self._computeState(**kwargs)
        self._sendState(payload)
