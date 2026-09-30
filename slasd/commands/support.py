"""Collection of supporting classes."""

import struct
from dataclasses import dataclass


@dataclass()
class LedColor:
    red: int = 0
    green: int = 0
    blue: int = 0

    def to_bytes(self) -> bytearray:
        ledBy_R = struct.pack('<B', self.red)
        ledBy_G = struct.pack('<B', self.green)
        ledBy_B = struct.pack('<B', self.blue)
        return bytearray(ledBy_R + ledBy_G + ledBy_B)
