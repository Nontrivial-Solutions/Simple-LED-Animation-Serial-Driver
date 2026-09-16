"""Fastrak serial commands with a response path."""

from .command import SerialCommandWithResponse
from .support import (
    FastrakStations,
    MacroFilter,
    StationState,
    SyncMode,
    TestBitNumbers,
)


class HemisphereOfOper(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        x : float | None

        y : float | None

        z : float | None


        """
        self._commandId = 'H'
        self._payload = f'{station.value}'
        if x is None and y is None and z is None:
            return
        else:
            self._payload += ','
            if x:
                self._payload += f'{x:+3.2f}'
            self._payload += ','
            if y:
                self._payload += f'{y:+3.2f}'
            self._payload += ','
            if z:
                self._payload += f'{z:+3.2f}'
        self._payload += '\n'


class SetSyncMode(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        sMode: SyncMode | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        sMode : SyncMode | None


        """
        self._commandId = 'x'
        self._payload = ''
        if sMode is not None:
            self._payload += f'{sMode.value}'
        self._payload += '\n'


class PositionEnvelop(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        xMax: float | None = None,
        yMax: float | None = None,
        zMax: float | None = None,
        xMin: float | None = None,
        yMin: float | None = None,
        zMin: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        xMax : float | None

        yMax : float | None

        zMax : float | None

        xMin : float | None

        yMin : float | None

        zMin : float | None


        """
        self._commandId = 'V'
        self._payload = f'{station.value}'
        if (
            xMax is None
            and xMin is None
            and yMax is None
            and yMin is None
            and zMax is None
            and zMin is None
        ):
            return
        else:
            self._payload += ','
            if xMax:
                self._payload += f'{xMax:+3.3f}'
            self._payload += ','
            if yMax:
                self._payload += f'{yMax:+3.3f}'
            self._payload += ','
            if zMax:
                self._payload += f'{zMax:+3.3f}'
            self._payload += ','
            if xMin:
                self._payload += f'{xMin:+3.3f}'
            self._payload += ','
            if yMin:
                self._payload += f'{yMin:+3.3f}'
            self._payload += ','
            if zMin:
                self._payload += f'{zMin:+3.3f}'
        self._payload += '\n'


class AttitudeFilterParam(SerialCommandWithResponse):
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
        self._commandId = 'v'
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


class BuiltInTestInfo(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(self, bit: TestBitNumbers, clear: bool) -> None:
        """Class constructor.

        Parameters
        ----------
        bit : TestBitNumbers

        clear : bool


        """
        self._commandId = 'T'
        self._payload = f'{bit.value}'
        if clear:
            self._payload += f',{0}'
        self._payload += '\n'


class SystemStatusRecord(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'S'
        self._payload = ''


class TransmitterMountingFrame(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        a: float | None = None,
        e: float | None = None,
        r: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        a : float | None

        e : float | None

        r : float | None


        """
        self._commandId = 'r'
        self._payload = f'{station.value}'
        if a is None and e is None and r is None:
            return
        else:
            self._payload += ','
            if a:
                self._payload += f'{a:+3.3f}'
            self._payload += ','
            if e:
                self._payload += f'{e:+3.3f}'
            self._payload += ','
            if r:
                self._payload += f'{r:+3.3f}'
        self._payload += '\n'


class AngularEnvelop(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        azMax: float | None = None,
        elMax: float | None = None,
        rlMax: float | None = None,
        azMin: float | None = None,
        elMin: float | None = None,
        rlMin: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        azMax : float | None

        elMax : float | None

        rlMax : float | None

        azMin : float | None

        elMin : float | None

        rlMin : float | None


        """
        self._commandId = 'Q'
        self._payload = f'{station.value}'
        if (
            azMax is None
            and azMin is None
            and elMax is None
            and elMin is None
            and rlMax is None
            and rlMin is None
        ):
            return
        else:
            self._payload += ','
            if azMax:
                self._payload += f'{azMax:+3.3f}'
            self._payload += ','
            if elMax:
                self._payload += f'{elMax:+3.3f}'
            self._payload += ','
            if rlMax:
                self._payload += f'{rlMax:+3.3f}'
            self._payload += ','
            if azMin:
                self._payload += f'{azMin:+3.3f}'
            self._payload += ','
            if elMin:
                self._payload += f'{elMin:+3.3f}'
            self._payload += ','
            if rlMin:
                self._payload += f'{rlMin:+3.3f}'
        self._payload += '\n'


class SingleDataRecord(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
    ) -> None:
        """Class constructor."""
        self._commandId = 'P'
        self._payload = ''


class DefTipOffset(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        xOff: float | None = None,
        yOff: float | None = None,
        zOff: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        xOff : float | None

        yOff : float | None

        zOff : float | None


        """
        self._commandId = 'N'
        self._payload = f'{station.value}'
        if xOff is None and yOff is None and zOff is None:
            return
        elif xOff and yOff and zOff:
            self._payload += f',{xOff:+3.2f}'
            self._payload += f',{yOff:+3.2f}'
            self._payload += f',{zOff:+3.2f}'
        else:
            raise Exception('an error occurred')
        self._payload += '\n'


class ActiveStnState(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        state: StationState | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        state : StationState | None


        """
        self._commandId = 'l'
        self._payload = f'{station.value}'
        if state:
            self._payload += f',{state.value}'
        self._payload += '\n'


class DefineInc(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        distance: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        distance : float | None


        """
        self._commandId = 'I'
        if distance:
            self._payload = f'{station.value},{distance:+3.2f}'
        else:
            self._payload = f'{station.value}'
        self._payload += '\n'


class BoresightRefAng(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        azRef: float | None = None,
        elRef: float | None = None,
        rlRef: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        azRef : float | None

        elRef : float | None

        rlRef : float | None


        """
        self._commandId = 'G'
        self._payload = f'{station.value}'
        if azRef is None and elRef is None and rlRef is None:
            return
        else:
            self._payload += ','
            if azRef:
                self._payload += f'{azRef:+3.2f}'
            self._payload += ','
            if elRef:
                self._payload += f'{elRef:+3.2f}'
            self._payload += ','
            if rlRef:
                self._payload += f'{rlRef:+3.2f}'
        self._payload += '\n'


class AlignRefFrm(SerialCommandWithResponse):
    """Info in Fastrak manual."""

    def __init__(
        self,
        station: FastrakStations,
        Ox: float | None = None,
        Oy: float | None = None,
        Oz: float | None = None,
        Xx: float | None = None,
        Xy: float | None = None,
        Xz: float | None = None,
        Yx: float | None = None,
        Yy: float | None = None,
        Yz: float | None = None,
    ) -> None:
        """Class constructor.

        Parameters
        ----------
        station : FastrakStations

        Ox : float | None

        Oy : float | None

        Oz : float | None

        Xx : float | None

        Xy : float | None

        Xz : float | None

        Yx : float | None

        Yy : float | None

        Yz : float | None


        """
        self._commandId = 'A'
        self._payload = f'{station.value}'
        if (
            Ox is None
            and Oy is None
            and Oz is None
            and Xx is None
            and Xy is None
            and Xz is None
            and Yx is None
            and Yy is None
            and Yz is None
        ):
            return
        else:
            self._payload += ','
            if Ox:
                self._payload += f'{Ox:+3.2f}'
            self._payload += ','
            if Oy:
                self._payload += f'{Oy:+3.2f}'
            self._payload += ','
            if Oz:
                self._payload += f'{Oz:+3.2f}'
            self._payload += ','
            if Xx:
                self._payload += f'{Xx:+3.2f}'
            self._payload += ','
            if Xy:
                self._payload += f'{Xy:+3.2f}'
            self._payload += ','
            if Xz:
                self._payload += f'{Xz:+3.2f}'
            self._payload += ','
            if Yx:
                self._payload += f'{Yx:+3.2f}'
            self._payload += ','
            if Yy:
                self._payload += f'{Yy:+3.2f}'
            self._payload += ','
            if Yz:
                self._payload += f'{Yz:+3.2f}'
        self._payload += '\n'
