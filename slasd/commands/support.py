"""Collection of supporting classes."""

import struct
from dataclasses import dataclass


@dataclass()
class LedColor:
    """Describes an LED [RGB](https://en.wikipedia.org/wiki/RGB_color_model) color and supporting
    methods.

    Attributes
    ----------
    red : int
        Red component of the RGB model.
    green : int
        Green component of the RGB model.
    blue : int
        Blue component of the RGB model.

    """

    red: int = 0
    green: int = 0
    blue: int = 0

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, LedColor):
            return (
                self.red == other.red
                and self.green == other.green
                and self.blue == other.blue
            )
        return False

    def to_ascii(self) -> bytearray:
        """Compute the three byte representation of the RGB model.

        Returns
        -------
        bytearray
            A three byte array of the R, G, and B bytes.


        """
        ledBy_R = str(self.red)
        ledBy_G = str(self.green)
        ledBy_B = str(self.blue)
        return bytearray(ledBy_R + ':' + ledBy_G + ':' + ledBy_B, 'ASCII')

    def to_bytes(self) -> bytearray:
        """Compute the three byte representation of the RGB model.

        Returns
        -------
        bytearray
            A three byte array of the R, G, and B bytes.


        """
        ledBy_R = struct.pack('<B', self.red)
        ledBy_G = struct.pack('<B', self.green)
        ledBy_B = struct.pack('<B', self.blue)
        return bytearray(ledBy_R + ledBy_G + ledBy_B)
