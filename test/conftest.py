"""Support file."""

import pytest
from pytest_mock.plugin import MockerFixture

from fastrakSerialDriver.fastrakDevice import FastrakDevice

# =================================================================================================
# =================================================================================================
# =================================================================================================
#  Support
# =================================================================================================
# =================================================================================================
# =================================================================================================

POSITION_BUFFER: list[tuple[bytes, list[float]]] = [
    (
        b'02 \x00\x00\x00\x00'
        + b'\x00\x00\x00\x00'
        + b'\x00\x00\x00\x00'
        + b'\x00\x00\x00\x00'
        + b'\x00\x00\x00\x00'
        + b'\x00\x00\x00\x00\r\n',
        [0, 0, 0, 0, 0, 0],
    ),
    (
        b'02 \x00\x00\x80\x3f'
        + b'\x00\x00\x80\x3f'
        + b'\x00\x00\x80\x3f'
        + b'\x00\x00\x80\x3f'
        + b'\x00\x00\x80\x3f'
        + b'\x00\x00\x80\x3f\r\n',
        [1, 1, 1, 1, 1, 1],
    ),
    (
        b'02 \x00\x00\x80\xbf'
        + b'\x00\x00\x80\xbf'
        + b'\x00\x00\x80\xbf'
        + b'\x00\x00\x80\xbf'
        + b'\x00\x00\x80\xbf'
        + b'\x00\x00\x80\xbf\r\n',
        [-1, -1, -1, -1, -1, -1],
    ),
    (
        b'02 \x00\x00\x80\x3f'
        + b'\x00\x00\x80\xbf'
        + b'\x00\x00\x80\x3f'
        + b'\x00\x00\x80\xbf'
        + b'\x00\x00\x80\x3f'
        + b'\x00\x00\x80\xbf\r\n',
        [1, -1, 1, -1, 1, -1],
    ),
    (
        b'02 \x00\x00\x80\x3f'
        + b'\x00\x00\x00\x40'
        + b'\x00\x00\x40\x40'
        + b'\x00\x00\x80\x40'
        + b'\x00\x00\xa0\x40'
        + b'\x00\x00\xc0\x40\r\n',
        [1, 2, 3, 4, 5, 6],
    ),
    (
        b'02 \xcd\xcc\xcc\x3d'
        + b'\xcd\xcc\xcc\x3d'
        + b'\xcd\xcc\xcc\x3d'
        + b'\xcd\xcc\xcc\x3d'
        + b'\xcd\xcc\xcc\x3d'
        + b'\xcd\xcc\xcc\x3d\r\n',
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    ),
    (
        b'02 \xcd\xcc\x8c\x3f'
        + b'\xcd\xcc\x8c\x3f'
        + b'\xcd\xcc\x8c\x3f'
        + b'\xcd\xcc\x8c\x3f'
        + b'\xcd\xcc\x8c\x3f'
        + b'\xcd\xcc\x8c\x3f\r\n',
        [1.1, 1.1, 1.1, 1.1, 1.1, 1.1],
    ),
]

# =================================================================================================
# =================================================================================================
# Stub and Mock Classes
# =================================================================================================
# =================================================================================================


# ruff: disable[D103]
class _SerialStub:
    """Stub of a pyserial interface."""

    _is_open: bool
    _in_waiting: int
    _counter: int

    def __init__(self, *args, **kwargs):
        self._is_open = True
        self._in_waiting = 1
        self._counter = 0
        pass

    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def in_waiting(self) -> int:
        return self._is_open

    def open(self):
        self._is_open = True
        pass

    def close(self):
        self._is_open = False
        pass

    def read(self, size=1) -> bytes:

        idx = self._counter % len(POSITION_BUFFER)
        self._counter += 1
        return POSITION_BUFFER[idx][0]

    def write(self, data):
        pass

    def readline(self):
        idx = self._counter % len(POSITION_BUFFER)
        self._counter += 1
        return POSITION_BUFFER[idx][0]

    def reset_input_buffer(self):
        pass


# ruff: enable[D103]


# =================================================================================================
# =================================================================================================
# Fixtures
# =================================================================================================
# =================================================================================================
@pytest.fixture
def setupDevice(mocker: MockerFixture):
    """Fixture for setting up a FastrakDevice with a mocked serial interface.

    ----------
    mocker : MockerFixture
        Mocking tooling fixture.
    """
    mocker.patch('fastrakSerialDriver.fastrakDevice.Serial', _SerialStub)
    device = FastrakDevice.create_valid_device()
    assert device is not None
    assert device._ser.is_open  # ty: ignore

    yield device

    if device._thread is not None and device._thread.is_alive():
        device._thread.stop()
        device._thread.join()


@pytest.fixture
def setupDeviceAscii(mocker: MockerFixture):
    """Fixture for setting up a FastrakDevice with a mocked serial interface.

    ----------
    mocker : MockerFixture
        Mocking tooling fixture.
    """
    mocker.patch('fastrakSerialDriver.fastrakDevice.Serial', _SerialStub)
    device = FastrakDevice.create_valid_device(isBinary=False)
    assert device is not None
    assert device._ser.is_open  # ty: ignore

    yield device

    if device._thread is not None and device._thread is not None:
        device._thread.stop()


@pytest.fixture
def serialStub():
    """@@@TODO"""

    yield _SerialStub


@pytest.fixture
def posBuff():
    """@@@TODO"""

    yield POSITION_BUFFER
