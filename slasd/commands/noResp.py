"""Fastrak serial commands with no response path."""

from .command import SerialCommand
from .support import (
    BtnModes,
    FastrakStations,
    MacroFilter,
    OutputData,
    SerialBaudrates,
    SerialBits,
    SerialParities,
)


class ConfigControlData(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
        data: str | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        data : str | None

        """
        self._commandId = 'X'
        self._payload = ''
        if data is None:
            return
        else:
            if len(data) <= 32:
                self._payload = data
            else:
                raise Exception('an error occurred')
        self._payload += '\n'


class PositionFilterParam(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
        n: MacroFilter | None = None,
        sensitivity: float | None = None,
        fLow: float | None = None,
        fHigh: float | None = None,
        factor: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        n : MacroFilter | None

        sensitivity : float | None

        fLow : float | None

        fHigh : float | None

        factor : float | None


        """
        self._commandId = 'x'
        self._payload = ''
        if sensitivity is None and fLow is None and fHigh is None and factor is None:
            if n is None:
                return
            else:
                self._payload = f'{n}'
        else:
            if sensitivity and 0 < sensitivity and sensitivity < 1:  # noqa: SIM300
                self._payload += f'{sensitivity:+3.3f}'
            else:
                raise Exception('an error occurred')
            self._payload += ','
            if fLow and 0 < fLow and fLow < 1:  # noqa: SIM300
                if fHigh and fHigh < fLow:
                    raise Exception('an error occurred')
                self._payload += f'{fLow:+1.3f}'
            self._payload += ','
            if fHigh and 0 < fHigh and fHigh < 1:  # noqa: SIM300
                if fLow and fHigh < fLow:
                    raise Exception('an error occurred')
                self._payload += f'{fLow:+1.3f}'
            self._payload += ','
            if factor and 0 < factor and factor < 1:  # noqa: SIM300
                self._payload += f'{factor:+1.3f}'
        self._payload += '\n'


class MetricUnits(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'u'
        self._payload = ''


class EnglishUnits(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'U'
        self._payload = ''


class ResetAlignmentFrame(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations


        """
        self._commandId = 'R'
        self._payload = f'{station.value}'
        self._payload += '\n'


class OutputDataList(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self, station: FastrakStations, dataList: list[OutputData]) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        dataList : list[OutputData]


        """
        self._commandId = 'O'
        self._payload = f'{station.value},'
        if (
            len(dataList) > 32
            and sum([it.value.sizeAscii for it in dataList]) > 254
            and sum([it.value.sizeByte for it in dataList]) > 254
        ):
            raise Exception('an error occurred')
        self._payload += ','.join([str(it.value.symbol) for it in dataList])
        self._payload += '\n'


class SetOutputPort(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self, orate: SerialBaudrates, parity: SerialParities, bits: SerialBits
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        orate : SerialBaudrates

        parity : SerialParities

        bits : SerialBits


        """
        self._commandId = 'o'
        self._payload = f'{orate.value},{parity.value},{bits.value},0'
        self._payload += '\n'


class EnableAsciiOut(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'F'
        self._payload = ''


class EnableBinOut(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'f'
        self._payload = ''


class DefStylusBtnFun(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self, station: FastrakStations, btnMode: BtnModes) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        btnMode : BtnModes


        """
        self._commandId = 'e'
        if btnMode == BtnModes.MOUSE:
            self._payload = f'{station.value},0'
        elif btnMode == BtnModes.POINTER:
            self._payload = f'{station.value},1'
        self._payload += '\n'


class DisableFxdMtlComp(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self) -> None:
        """Class constructor."""
        self._commandId = 'd'
        self._payload = ''


class EnableFxdMtlComp(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self) -> None:
        """Class constructor."""
        self._commandId = 'D'
        self._payload = ''


class ReinitializeSys(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self) -> None:
        """Class constructor."""
        self._commandId = chr(25)
        self._payload = ''


class SuspendDataTrans(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self) -> None:
        """Class constructor."""
        self._commandId = chr(23)
        self._payload = ''


class ResumeDataTrans(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self) -> None:
        """Class constructor."""
        self._commandId = chr(17)
        self._payload = ''


class SaveConfig(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self) -> None:
        """Class constructor."""
        self._commandId = chr(11)
        self._payload = ''


class EnableContMd(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'C'
        self._payload = ''


class DisableContMd(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(self) -> None:
        self._commandId = 'c'
        self._payload = ''


class Boresight(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations


        """
        self._commandId = 'B'
        self._payload = f'{station.value}'
        self._payload += '\n'


class UnBoresight(SerialCommand):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations


        """
        self._commandId = 'b'
        self._payload = f'{station.value}'
        self._payload += '\n'
