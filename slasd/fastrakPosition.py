"""Contains position class for a Fastrak position sextuple."""

import struct
from dataclasses import dataclass


@dataclass
class FastrakPostion:
    r"""A six degree of freedom position.

    Attributes
    ----------
    x : float
        The $x$ position.
    y : float
        The $x$ position.
    z : float
        The $x$ position.
    psi : float
        The $\psi$ position. Also called azimuth.
    theta : float
        The $\theta$ position. Also called elevation.
    phi : float
        The $\varphi$ position. Also called roll.

    """

    x: float
    y: float
    z: float
    phi: float
    psi: float
    theta: float

    @classmethod
    def parseValidPosition(cls, packet: bytes) -> 'FastrakPostion | None':
        r"""Parse a byte packet into a position object sextuple.

        The Fastrak uses an IEEE 754-1985 LSB float.

        Parameters
        ----------
        packet : bytes

            The packet has the following form:

            | MSB | 0          | 1    | 2-5 | 6-9  | 10-13 | 14-17  | 18-21    | 22-25     | 26   | 27   | LSB |
            | --- | ---------- | ---- | --- | ---- | ----- | ------ | -------- | --------- | ---- | ---- | --- |
            |     | Station ID | `\s` | x   | y    | z     | $\psi$ | $\theta$ | $\varphi$ | `\r` | `\n` |     |

            Where the position bytes are of the form:

            | MSB | 2       | 3       | 4       | 5       | 6       | 7       | 8       | 9       | 10      | 15      | 16      | 17      | 18           | 19           | 20           | 21           | 22             | 23             | 24             | 25             | 26              | 27              | 28              | 29              | LSB |
            | --- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------------ | ------------ | ------------ | ------------ | -------------- | -------------- | -------------- | -------------- | --------------- | --------------- | --------------- | --------------- | --- |
            |     | Float x | Float x | Float x | Float x | Float y | Float y | Float y | Float y | Float z | Float z | Float z | Float z | Float $\psi$ | Float $\psi$ | Float $\psi$ | Float $\psi$ | Float $\theta$ | Float $\theta$ | Float $\theta$ | Float $\theta$ | Float $\varphi$ | Float $\varphi$ | Float $\varphi$ | Float $\varphi$ |     |
            |     | Byte 0  | Byte 1  | Byte 2  | Byte 3  | Byte 0  | Byte 1  | Byte 2  | Byte 3  | Byte 0  | Byte 1  | Byte 2  | Byte 3  | Byte 0       | Byte 1       | Byte 2       | Byte 3       | Byte 0         | Byte 1         | Byte 2         | Byte 3         | Byte 0          | Byte 1          | Byte 2          | Byte 3          |     |

        Returns
        -------
            FastrakPostion | None
               - None when packet is invalid.
               - A FastrakPostion instance when packet is valid.
        """
        if not packet:
            return None
        packet = packet.strip()
        packet = packet[3:]
        if len(packet) != 4 * 6:
            return None
        positions = struct.unpack('<ffffff', packet)
        return cls(
            x=positions[0],
            y=positions[1],
            z=positions[2],
            psi=positions[3],
            theta=positions[4],
            phi=positions[5],
        )

    @property
    def posTuple(self) -> tuple[float, float, float, float, float, float]:
        """A sextuple of the positional data."""
        return (self.x, self.y, self.z, self.psi, self.theta, self.phi)
