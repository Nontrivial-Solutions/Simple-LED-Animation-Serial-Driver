"""Contains the FastrakDevice class unit tests."""

import pytest
from pytest_mock.plugin import MockerFixture

from fastrakSerialDriver.commands.support import FastrakStations, SerialBaudrates
from fastrakSerialDriver.fastrakDevice import FastrakDevice

# =================================================================================================
# =================================================================================================
# =================================================================================================
#   Tests
# =================================================================================================
# =================================================================================================
# =================================================================================================

# =================================================================================================
# =================================================================================================
# Constructor Tests
# =================================================================================================
# =================================================================================================


def test_default_constructor(serialStub, mocker: MockerFixture):
    """[TestDevice_ID_001][TestDevice_ID_001]."""
    mocker.patch('fastrakSerialDriver.fastrakDevice.Serial', serialStub)
    device = FastrakDevice.create_valid_device()
    assert device is not None


@pytest.mark.parametrize('COMport', ['COM1'])
@pytest.mark.parametrize(
    'baud',
    [
        SerialBaudrates.BAUD_2400,
        SerialBaudrates.BAUD_4800,
        SerialBaudrates.BAUD_9600,
        SerialBaudrates.BAUD_19200,
        SerialBaudrates.BAUD_38400,
        SerialBaudrates.BAUD_57600,
        SerialBaudrates.BAUD_115200,
    ],
)
@pytest.mark.parametrize(
    'station',
    [
        FastrakStations.STATION_1,
        FastrakStations.STATION_2,
        FastrakStations.STATION_3,
        FastrakStations.STATION_4,
    ],
)
@pytest.mark.parametrize('timeout', [2])
@pytest.mark.parametrize('doSetup', [True, False])
@pytest.mark.parametrize('bin', [True, False])
@pytest.mark.parametrize('polling', [0.1, 1])
def test_constructor(
    COMport,
    baud,
    station,
    timeout,
    doSetup,
    bin,
    polling,
    serialStub,
    mocker: MockerFixture,
):
    """[TestDevice_ID_001][TestDevice_ID_001]."""
    mocker.patch('fastrakSerialDriver.fastrakDevice.Serial', serialStub)
    assert (
        FastrakDevice.create_valid_device(
            COMport, baud, station, timeout, doSetup, bin, polling
        )
        is not None
    )


# =================================================================================================
# =================================================================================================
# Connect Method Tests
# =================================================================================================
# =================================================================================================


def test_connect(setupDevice: FastrakDevice):
    """[TestDevice_ID_002][TestDevice_ID_002]."""
    assert setupDevice is not None
    setupDevice.connect()
    assert setupDevice._ser.is_open  # ty: ignore


def test_already_connected(setupDevice: FastrakDevice):
    """[TestDevice_ID_003][TestDevice_ID_003]."""
    assert setupDevice is not None
    setupDevice.connect()
    assert setupDevice._ser.is_open  # ty: ignore
    setupDevice.connect()
    assert setupDevice._ser.is_open  # ty: ignore


# =================================================================================================
# =================================================================================================
# Start Stream Method Tests
# =================================================================================================
# =================================================================================================


def test_streamConnect(setupDevice: FastrakDevice):
    """[TestDevice_ID_004][TestDevice_ID_004]."""
    setupDevice.enableStream()
    assert setupDevice.streaming


def test_double_stream(setupDevice: FastrakDevice):
    """[TestDevice_ID_005][TestDevice_ID_005]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    setupDevice.enableStream()
    assert setupDevice.streaming


def test_double_stream_after_complete(setupDevice: FastrakDevice):
    """[TestDevice_ID_025][TestDevice_ID_025]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    setupDevice.disableStream()
    assert not setupDevice.streaming
    setupDevice.enableStream()
    assert setupDevice.streaming


def test_unhappy_streamConnect(setupDevice: FastrakDevice):
    """[TestDevice_ID_006][TestDevice_ID_006]."""
    setupDevice._ser = None
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.enableStream()


# =================================================================================================
# =================================================================================================
# End Stream Method Tests
# =================================================================================================
# =================================================================================================


def test_EndStream(setupDevice: FastrakDevice):
    """[TestDevice_ID_007][TestDevice_ID_007]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    setupDevice.disableStream()
    assert not setupDevice.streaming


def test_unhappy_streamDisconnect(setupDevice: FastrakDevice):
    """[TestDevice_ID_008][TestDevice_ID_008]."""
    setupDevice._ser = None
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.disableStream()


# =================================================================================================
# =================================================================================================
# Read Line Method Tests
# =================================================================================================
# =================================================================================================


def test_readLine_notstreaming(setupDevice: FastrakDevice, posBuff):
    """[TestDevice_ID_009][TestDevice_ID_009]."""
    assert not setupDevice.streaming
    line = setupDevice.readLine()
    assert line == posBuff[setupDevice._ser._counter - 1][0].strip()


def test_unhappy_readLine_streaming(setupDevice: FastrakDevice):
    """[TestDevice_ID_010][TestDevice_ID_010]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.readLine()


def test_unhappy_readLine(setupDevice: FastrakDevice):
    """[TestDevice_ID_011][TestDevice_ID_011]."""
    setupDevice._ser = None
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.readLine()


# =================================================================================================
# =================================================================================================
# Boresight Method Tests
# =================================================================================================
# =================================================================================================


def test_boresight(setupDevice: FastrakDevice):
    """[TestDevice_ID_012][TestDevice_ID_012]."""
    assert not setupDevice.streaming
    setupDevice.boresight()


def test_unhappy_borseight_isStreaming(setupDevice: FastrakDevice):
    """[TestDevice_ID_013][TestDevice_ID_013]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.boresight()


def test_unhappy_boresight_noSerial(setupDevice: FastrakDevice):
    """[TestDevice_ID_014][TestDevice_ID_014]."""
    setupDevice._ser = None
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.boresight()


# =================================================================================================
# =================================================================================================
# Basic Setup Method Tests
# =================================================================================================
# =================================================================================================


def test_basicSetup(setupDevice: FastrakDevice):
    """[TestDevice_ID_015][TestDevice_ID_015]."""
    assert not setupDevice.streaming
    setupDevice.basicSetup()


def test_unhappy_basicSetup_isStreaming(setupDevice: FastrakDevice):
    """[TestDevice_ID_016][TestDevice_ID_016]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.basicSetup()


def test_unhappy_basicSetup_noSerial(setupDevice: FastrakDevice):
    """[TestDevice_ID_017][TestDevice_ID_017]."""
    setupDevice._ser = None
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.basicSetup()


# =================================================================================================
# =================================================================================================
# lastPosition Member Tests
# =================================================================================================
# =================================================================================================


def test_lastPosition_isStreaming(setupDevice: FastrakDevice, posBuff):
    """[TestDevice_ID_018][TestDevice_ID_018]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    lp = setupDevice.lastPosition
    assert lp is not None
    assert lp.posTuple == pytest.approx(
        posBuff[setupDevice._ser._counter - 1][1], 0.00001
    )


def test_lastPosition_NotStreaming(setupDevice: FastrakDevice, posBuff):
    """[TestDevice_ID_019][TestDevice_ID_019]."""
    assert not setupDevice.streaming
    lp = setupDevice.lastPosition
    assert lp is not None
    assert lp.posTuple == pytest.approx(
        posBuff[setupDevice._ser._counter - 1][1], 0.00001
    )


def test_unhappy_lastPosition_noSerial(setupDevice: FastrakDevice, posBuff):
    """[TestDevice_ID_020][TestDevice_ID_020]."""
    setupDevice._ser = None
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        lp = setupDevice.lastPosition


def test_unhappy_lastPosition_ASCII(setupDeviceAscii: FastrakDevice, posBuff):
    """[TestDevice_ID_021][TestDevice_ID_021]."""
    assert not setupDeviceAscii.streaming
    with pytest.raises(Exception):  # TODO: Add specific Exception
        lp = setupDeviceAscii.lastPosition


# =================================================================================================
# =================================================================================================
# Clear Buffer Tests
# =================================================================================================
# =================================================================================================


def test_clearBuffer_isNotStreaming(setupDevice: FastrakDevice, posBuff):
    """[TestDevice_ID_022][TestDevice_ID_022]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    setupDevice.disableStream()
    assert not setupDevice.streaming
    assert setupDevice.data != b''
    setupDevice.clearBuffer()
    assert setupDevice.data == b''
    setupDevice.clearBuffer()
    assert setupDevice.data == b''


def test_unhappy_clearBuffer_isStreaming(setupDevice: FastrakDevice, posBuff):
    """[TestDevice_ID_023][TestDevice_ID_023]."""
    setupDevice.enableStream()
    assert setupDevice.streaming
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        setupDevice.clearBuffer()


def test_unhappy_clearBuffer_noSerial(setupDevice: FastrakDevice, posBuff):
    """[TestDevice_ID_024][TestDevice_ID_024]."""
    setupDevice._ser = None
    # ruff: disable[B017]
    with pytest.raises(Exception):  # TODO: Add specific Exception
        lp = setupDevice.lastPosition
