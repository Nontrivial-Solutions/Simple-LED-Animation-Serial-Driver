"""Contains the FastrakDevice class."""

import threading
import time

from serial import Serial, SerialException

from .commands.noResp import (
    Boresight,
    DisableContMd,
    EnableAsciiOut,
    EnableBinOut,
    EnableContMd,
    OutputDataList,
    UnBoresight,
)
from .commands.support import FastrakStations, OutputData, SerialBaudrates
from .commands.withResp import ActiveStnState, SingleDataRecord, StationState
from .fastrakPosition import FastrakPostion


class FastrakDevice:
    """Defines interface for connecting, setting up, and streaming from a Fastrak.

    Attributes
    ----------
    _ser : Serial | None
        Serial connection to a Fastrak.

    _station : FastrakStations
        Station index on the Fastrak.

    _thread : threading.Thread
        Child thread for non blocking data retrieval.

    _thread :#️⃣_PollingThread | None
        Thread for polling Fastrak data.

    _COMport :
        String representing the COM port to be connected to.

    _baud : SerialBaudrates
        Baudrate for the serial connection.

    _station : FastrakStations
        Station on the Fastrak to use.

    _timeout : int, default: 1second
        Serial timeout for the connection.

    _pollingRate : float
        The polling rate for streaming mode.

    _isBinary : bool
        Should the device be configured for ASCII or binary mode.


    """

    _ser: Serial | None
    _station: FastrakStations
    _thread: '_PollingThread | None'
    _COMport: str
    _baud: SerialBaudrates
    _station: FastrakStations
    _timeout: int
    _pollingRate: float
    _isBinary: bool

    class _PollingThread(threading.Thread):
        """Defines a polling class for reading from a Fastrak.

        Attributes
        ----------
        _ser : Serial
            Serial connection to a Fastrak.
        _data : bytearray
            Data from last streaming session.
        _pollRate : float
            The rate to poll the Fastrak.
        """

        _ser: Serial
        _data: bytearray
        _pollRate: float
        _lastPosition: FastrakPostion | None
        _isBinary: bool

        def __init__(self, serial: Serial, pollRate: float, isBinary: bool):
            """Construct a _PollingThread class.

            Parameters
            ----------
            serial : Serial
                Serial connection to a Fastrak.
            pollRate : float
                The rate to pool the Fastrak.
            """
            super().__init__()
            self._ser = serial
            self._stop_event = threading.Event()
            self._data = bytearray()
            self._pollRate = pollRate
            self._lastPosition = None
            self._isBinary = isBinary

        @property
        def lastPosition(self) -> FastrakPostion | None:
            return self._lastPosition

        @property
        def data(self) -> bytes:
            """Contains the byte data from the last/current streaming session.

            Returns
            -------
            bytearray
                Contains the byte data from the last/current streaming session.

            """
            return bytes(self._data)

        def _getLastPos(self):
            """Get the last tracking position from the buffer."""
            if self._isBinary and self._data:
                data = self._data[-52:]
                lines = data.splitlines()
                if len(lines) == 1:  # Handle the first packet
                    self._lastPosition = FastrakPostion.parseValidPosition(
                        bytes(lines[0])
                    )
                else:
                    self._lastPosition = FastrakPostion.parseValidPosition(
                        bytes(lines[1])
                    )

        def run(self):
            """Run the polling process."""
            EnableContMd().send(self._ser)
            while True:
                try:
                    data = self._ser.read(self._ser.in_waiting)
                    self._data.extend(data)
                    self._getLastPos()
                    is_stopped = self._stop_event.wait(self._pollRate)
                    if is_stopped:
                        break

                except SerialException:
                    break  # TODO: Add Error flag
            DisableContMd().send(self._ser)
            self._ser.read(self._ser.in_waiting)
            self._ser.reset_input_buffer()

        def stop(self):
            """Stop the thread."""
            self._stop_event.set()
            start_time = time.time()
            while self.is_alive():
                if (time.time() - start_time) > 10:
                    raise Exception('an error occurred')  # TODO: Add specific Exception
                time.sleep(0.01)

        def clearBuffer(self) -> None:
            """Clear the streaming buffer."""
            self._data.clear()

    @property
    def streaming(self) -> bool:
        """Reports the streaming status of the device.

        Returns
        -------
        bool
            True when streaming False otherwise.

        """
        if self._thread is not None:
            return self._thread.is_alive()
        return False

    @property
    def data(self) -> bytes | None:
        """Contains the byte data from the last/current streaming session.

        Returns
        -------
        bytearray
            Contains the byte data from the last/current streaming session.

        """
        if self._thread is not None:
            return self._thread.data
        return None

    def __eq__(self, other: object):
        """@@@TODO."""
        return bool(
            isinstance(other, FastrakDevice) and other._COMport == self._COMport
        )

    def __init__(
        self,
        COMport: str = 'COM3',
        baud: SerialBaudrates = SerialBaudrates.BAUD_115200,
        station: FastrakStations = FastrakStations.STATION_2,
        timeout: int = 1,
        setup: bool = True,
        isBinary: bool = True,
        pollingRate: float = 0.001,
    ) -> None:
        """Construct a FastrakDevice class.

        Parameters
        ----------
        COMport : str
            String representing the COM port to be connected to.

        baud : SerialBaudrates
            Baudrate for the serial connection.

        station : FastrakStations, default: STATION_1
            Station on the Fastrak to use.

        timeout : int, default: 1second
            Serial timeout for the connection.

        setup : bool, default: True
            Flag indicating if basic setup should not run.

        isBinary : bool
            Should the device be configured for ASCII or binary mode.

        pollingRate : float
            The polling rate for streaming.

        """
        self._ser = None
        self._COMport = COMport
        self._baud = baud
        self._timeout = timeout
        self._station = station
        self._thread = None
        self._pollingRate = pollingRate
        self._isBinary = isBinary

        if setup:
            self.connect()
            self.basicSetup()

    @classmethod
    def create_valid_device(
        cls,
        COMport: str = 'COM3',
        baud: SerialBaudrates = SerialBaudrates.BAUD_115200,
        station: FastrakStations = FastrakStations.STATION_2,
        timeout: int = 1,
        setup: bool = True,
        isBinary: bool = True,
        pollingRate: float = 0.001,
    ) -> 'None | FastrakDevice':
        """Construct a FastrakDevice class, or return None if conditions are not met.

        Parameters
        ----------
        COMport : str
            String representing the COM port to be connected to.

        baud : SerialBaudrates
            Baudrate for the serial connection.

        station : FastrakStations, default: STATION_1
            Station on the Fastrak to use.

        timeout : int, default: 1second
            Serial timeout for the connection.

        setup : bool, default: True
            Flag indicating if basic setup should not run.

        isBinary : bool
            Should the device be configured for ASCII or binary mode.

        pollingRate : float
            The polling rate for streaming.

        Returns
        -------
        'None | FastrakDevice'
            None if conditions are not and a FastrakDevice otherwise.

        """
        if not (
            COMport
            and baud
            and station
            and timeout
            and pollingRate
            and isBinary is not None
            and setup is not None
            and pollingRate > 0
        ):
            return None
        return cls(COMport, baud, station, timeout, setup, isBinary, pollingRate)

    @property
    def lastPosition(self) -> FastrakPostion | None:
        """Contains the byte data from the last/current streaming session.

        Returns
        -------
        bytearray
            Contains the byte data from the last/current streaming session.

        """
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception
        if not self._isBinary:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if not self.streaming:
            return FastrakPostion.parseValidPosition(self.readLine())
        else:
            if self._thread is None:
                raise Exception('an error occurred')  # TODO: Add specific Exception
            return self._thread.lastPosition

    def clearBuffer(self) -> None:
        """Clear the streaming buffer."""
        if self._ser is None or not self._ser.is_open or self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception
        if self._thread is not None:
            self._thread.clearBuffer()

    def connect(self) -> None:
        """Connect to the serial device."""
        if self._ser is not None:
            if not self._ser.is_open:
                self._ser.open()
        else:
            self._ser = Serial(
                self._COMport, self._baud.value * 100, timeout=self._timeout
            )

    def enableStream(self) -> None:
        """Enable streaming on the Fastrak.

        Set up streaming on the Fastrak by creating a thread where the serial stream is polled.

        """
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception
        if not self._ser.is_open:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if self._thread is not None and self._thread.is_alive():
            self._thread.stop()
            self._thread.join()

        self._thread = self._PollingThread(self._ser, self._pollingRate, self._isBinary)

        if not self._thread.is_alive():
            self._thread.start()

    def disableStream(self) -> None:
        """Disable streaming on the Fastrak.

        Close the streaming on the Fastrak and join thread where the serial stream was polled.

        """
        if not self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if self._thread is not None and self._thread.is_alive():
            self._thread.stop()
            self._thread.join()

    def readLine(self) -> bytes:
        """Request a single data frame from the Fastrak."""
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception
        if not self._ser.is_open:
            raise Exception('an error occurred')  # TODO: Add specific Exception
        if self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        return SingleDataRecord().sendResp(self._ser).strip()

    def boresight(self) -> None:
        """Set the zero position for the station."""
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if not self._ser.is_open or self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        UnBoresight(self._station).send(self._ser)
        Boresight(self._station).send(self._ser)

    def basicSetup(self) -> None:
        """Complete the basic setup of a Fastrak."""
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if not self._ser.is_open or self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        DisableContMd().send(self._ser)

        ActiveStnState(FastrakStations.STATION_1, StationState.OFF).send(self._ser)
        ActiveStnState(FastrakStations.STATION_2, StationState.OFF).send(self._ser)
        ActiveStnState(FastrakStations.STATION_3, StationState.OFF).send(self._ser)
        ActiveStnState(FastrakStations.STATION_4, StationState.OFF).send(self._ser)

        ActiveStnState(self._station, StationState.ON).send(self._ser)

        if self._isBinary:
            EnableBinOut().send(self._ser)
        else:
            EnableAsciiOut().send(self._ser)

        OutputDataList(
            self._station,
            [
                OutputData.CART_COORDS,
                OutputData.AER_EULER_ANGLE,
                OutputData.CARRIAGE_RETURN,
            ],
        ).send(self._ser)
        self._ser.read(self._ser.in_waiting)
        self._ser.reset_input_buffer()
