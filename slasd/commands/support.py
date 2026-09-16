"""Collection of supporting classes."""

from dataclasses import dataclass
from enum import Enum


class SerialBaudrates(Enum):
    """Serial baudrate supported by the Fastrak.

    Attributes
    ----------
    BAUD_2400 : int
        2.4k baud
    BAUD_4800 : int
        4.8k baud
    BAUD_9600 : int
        9.6k baud
    BAUD_19200 : int
        19.2k baud
    BAUD_38400 : int
        38.4k baud
    BAUD_57600 : int
        57.6k baud
    BAUD_115200 : int
        115.2k baud

    """

    BAUD_2400 = 24
    BAUD_4800 = 48
    BAUD_9600 = 96
    BAUD_19200 = 192
    BAUD_38400 = 384
    BAUD_57600 = 576
    BAUD_115200 = 1152


class SerialParities(Enum):
    """Parities options for the Fastrak serial connection.

    Attributes
    ----------
    NONE : str
        No parity
    ODD : str
        Parity is ODD number of bits
    EVEN : str
        Parity is EVEN number of bits

    """

    NONE = 'N'
    ODD = 'O'
    EVEN = 'E'


class SerialBits(Enum):
    """Bits per character.

    Attributes
    ----------
    SEVEN : int
        Seven bits per character.
    EIGHT : int
        Eight bits per character.

    """

    SEVEN = 7
    EIGHT = 8


class FastrakStations(Enum):
    """Station ID for the Fastrak.

    A transmitter receiver pair. Usually a single transmitter with up to four receivers labeled 1 to 4.

    Attributes
    ----------
    STATION_1 : int
        Station one
    STATION_2 : int
        Station two
    STATION_3 : int
        Station three
    STATION_4 : int
        Station four
    """

    STATION_1 = 1
    STATION_2 = 2
    STATION_3 = 3
    STATION_4 = 4


class StationState(Enum):
    """State of a Fastrak station.

    Attributes
    ----------
    ON : int
        Station on state.
    OFF : int
        Station off state
    """

    OFF = 0
    ON = 1


class MacroFilter(Enum):
    """Filter types.

    Details in Fastrak manual.

    Attributes
    ----------
    NO_FILTER : int
    LOW_FILTER : int
    MEDIUM_FILTER : int
    HEAVY_FILTER : int

    """

    NO_FILTER = 2
    LOW_FILTER = 3
    MEDIUM_FILTER = 4
    HEAVY_FILTER = 5


@dataclass
class _OutputDataConfigInfo:
    """Local class defining output data config info.

    Each configurable output entry requires three pieces of information. These three allow validation of total frame size and commanding configuration of the data.

    Attributes
    ----------
    symbol : int
        Symbol representing the output data info.
    sizeAscii : int
        Size of the data represented as ASCII.
    sizeByte : int
        Size of the data represented as binary data.

    """

    symbol: int
    sizeAscii: int
    sizeByte: int

    def __hash__(self):
        """Hash function allowing use in an Enum."""
        hash(self.symbol)


class OutputData(Enum):
    """Configurable output data for a Fastrak data frame.

    Details in Fastrak manual.

    Attributes
    ----------
    SPACE_CHAR : _OutputDataConfigInfo
    CARRIAGE_RETURN :_OutputDataConfigInfo
    CART_COORDS :_OutputDataConfigInfo
    RELATIVE_MOVEMENT :_OutputDataConfigInfo
    AER_EULER_ANGLE :_OutputDataConfigInfo
    X_COSINES :_OutputDataConfigInfo
    Y_COSINES :_OutputDataConfigInfo
    Z_COSINES :_OutputDataConfigInfo
    ORIENTATION_QUATERNION :_OutputDataConfigInfo
    STYLUS_SWITCH_STATUS :_OutputDataConfigInfo
    PRECISE_CART_COORDS :_OutputDataConfigInfo
    PRECISE_RELATIVE_MOVEMENT :_OutputDataConfigInfo
    PRECISE_AER_EULER_ANGLE :_OutputDataConfigInfo
    PRECISE_X_COSINES :_OutputDataConfigInfo
    PRECISE_Y_COSINES :_OutputDataConfigInfo
    PRECISE_Z_COSINES :_OutputDataConfigInfo
    PRECISE_ORIENTATION_QUATERNION :_OutputDataConfigInfo
    PRECISE_STYLUS_SWITCH_STATUS :_OutputDataConfigInfo

    """

    SPACE_CHAR = _OutputDataConfigInfo(0, 1, 1)
    CARRIAGE_RETURN = _OutputDataConfigInfo(1, 1, 1)
    CART_COORDS = _OutputDataConfigInfo(2, 3 * 7, 3 * 4)
    RELATIVE_MOVEMENT = _OutputDataConfigInfo(3, 3 * 7, 3 * 4)
    AER_EULER_ANGLE = _OutputDataConfigInfo(4, 3 * 7, 3 * 4)
    X_COSINES = _OutputDataConfigInfo(5, 3 * 7, 3 * 4)
    Y_COSINES = _OutputDataConfigInfo(6, 3 * 7, 3 * 4)
    Z_COSINES = _OutputDataConfigInfo(7, 3 * 7, 3 * 4)
    ORIENTATION_QUATERNION = _OutputDataConfigInfo(11, 4 * 7, 4 * 4)
    STYLUS_SWITCH_STATUS = _OutputDataConfigInfo(16, 1, 1)

    PRECISE_CART_COORDS = _OutputDataConfigInfo(52, 3 * 13, 3 * 4)
    PRECISE_RELATIVE_MOVEMENT = _OutputDataConfigInfo(53, 3 * 13, 3 * 4)
    PRECISE_AER_EULER_ANGLE = _OutputDataConfigInfo(54, 3 * 13, 3 * 4)
    PRECISE_X_COSINES = _OutputDataConfigInfo(55, 3 * 13, 3 * 4)
    PRECISE_Y_COSINES = _OutputDataConfigInfo(56, 3 * 13, 3 * 4)
    PRECISE_Z_COSINES = _OutputDataConfigInfo(57, 3 * 13, 3 * 4)
    PRECISE_ORIENTATION_QUATERNION = _OutputDataConfigInfo(61, 4 * 13, 4 * 4)
    PRECISE_STYLUS_SWITCH_STATUS = _OutputDataConfigInfo(66, 1, 1)


class BtnModes(Enum):
    """Mode options for the Fastrak stylus.

    Attributes
    ----------
    MOUSE : int
        Behave as a mouse.
    POINTER : int
        Behave as a pointer.

    """

    MOUSE = 0
    POINTER = 1


class SyncMode(Enum):
    """The possible time sync sources for a Fastrak.

    Attributes
    ----------
    INTERNAL_SYNC : int
        Internal clock
    EXTERNAL_SYNC : int
        External clock
    VIDEO_SYNC : int
        Sense and sync to a CRT up to 2 feet away from the receiver.

    """

    INTERNAL_SYNC = 0
    EXTERNAL_SYNC = 1
    VIDEO_SYNC = 2


class TestBitNumbers(Enum):
    """Bit mapping for test bits.

    Details in Fastrak manual.

    Attributes
    ----------
    X_DRIVER_LINEARITY : int
    Y_DRIVER_LINEARITY : int
    Z_DRIVER_LINEARITY : int
    X_GAIN_LINEARITY : int
    Y_GAIN_LINEARITY : int
    Z_GAIN_LINEARITY : int
    X_DRIVER_LINEARITY_SLOPE : int
    Y_DRIVER_LINEARITY_SLOPE : int
    Z_DRIVER_LINEARITY_SLOPE : int
    X_COIL_SLOPE : int
    Y_COIL_SLOPE : int
    Z_COIL_SLOPE : int
    REC_PROM_ERROR : int
    TRANS_PROM_ERROR : int
    REC_PROM_CIRC_ERROR : int
    TRANS_PROM_CIRC_ERROR : int
    DRIVER_CHAR_VALIDITY : int
    REC_CHAR_VALIDITY : int
    REC_COIL_VALIDITY : int
    X_DRIVER_LIMITS_CAL : int
    Y_DRIVER_LIMITS_CAL : int
    Z_DRIVER_LIMITS_CAL : int
    X_GAIN_LIMITS_CAL : int
    Y_GAIN_LIMITS_CAL : int
    Z_GAIN_LIMITS_CAL : int
    COIL_LIMITS_CAL : int
    A_SIGNAL_SATURATION : int
    A_LOW_SIGNAL : int
    A_MAX_SINGAL_ELEMENT_ZERO : int
    EEPROM_VALIDITY_CSUM : int
    UNIT_NORMAL_POSITION_RESET : int
    COMPENSATION_STRUCT_ERRORS : int
    COMPENSATION_POINT_OUT_OF_BOUNDS : int
    NO_CRT_SYNC : int
    EEPROM_WRITE_ERROR : int
    REC_OUT_OF_BOX : int
    EULER_ANGLE_OUTSIDE_ENVELOPE : int

    """

    X_DRIVER_LINEARITY = 65
    Y_DRIVER_LINEARITY = 66
    Z_DRIVER_LINEARITY = 67
    X_GAIN_LINEARITY = 68
    Y_GAIN_LINEARITY = 69
    Z_GAIN_LINEARITY = 70
    X_DRIVER_LINEARITY_SLOPE = 71
    Y_DRIVER_LINEARITY_SLOPE = 72
    Z_DRIVER_LINEARITY_SLOPE = 73
    X_COIL_SLOPE = 74
    Y_COIL_SLOPE = 75
    Z_COIL_SLOPE = 76

    REC_PROM_ERROR = 84
    TRANS_PROM_ERROR = 85
    REC_PROM_CIRC_ERROR = 86
    TRANS_PROM_CIRC_ERROR = 87
    DRIVER_CHAR_VALIDITY = 88
    REC_CHAR_VALIDITY = 89
    REC_COIL_VALIDITY = 90

    X_DRIVER_LIMITS_CAL = 97
    Y_DRIVER_LIMITS_CAL = 98
    Z_DRIVER_LIMITS_CAL = 99
    X_GAIN_LIMITS_CAL = 100
    Y_GAIN_LIMITS_CAL = 101
    Z_GAIN_LIMITS_CAL = 102
    COIL_LIMITS_CAL = 103

    A_SIGNAL_SATURATION = 106
    A_LOW_SIGNAL = 107
    A_MAX_SINGAL_ELEMENT_ZERO = 108

    EEPROM_VALIDITY_CSUM = 109

    UNIT_NORMAL_POSITION_RESET = 115

    COMPENSATION_STRUCT_ERRORS = 116
    COMPENSATION_POINT_OUT_OF_BOUNDS = 117
    NO_CRT_SYNC = 118
    EEPROM_WRITE_ERROR = 119
    REC_OUT_OF_BOX = 120
    EULER_ANGLE_OUTSIDE_ENVELOPE = 121
