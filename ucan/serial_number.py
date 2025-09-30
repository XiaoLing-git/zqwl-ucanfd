"""Singleton class for serial number management of command models"""

from __future__ import annotations

from ucan.models.base_model import FilterFrame


class SerialNumber:
    """"""

    _instance = None

    def __new__(cls, *args, **kwargs) -> SerialNumber:  # type: ignore[no-untyped-def]
        """__new__."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.serial_number = -1  # type: ignore[has-type]
        return cls._instance

    def __init__(self, frame: FilterFrame = FilterFrame.standard) -> None:
        """init."""
        self.serial_number = self.serial_number + 1  # type: ignore[has-type]
        self.frame = frame
        if self.frame is FilterFrame.standard:
            self.serial_number = self.serial_number & 0x000007FF
        else:
            self.serial_number = self.serial_number & 0x1FFFFFFF

    @property
    def hex(self) -> str:
        """hex."""
        if self.frame is FilterFrame.standard:
            return "0000" + int.to_bytes(self.serial_number, byteorder="little", length=2).hex()
        else:
            return int.to_bytes(self.serial_number, byteorder="big", length=4).hex()

    @property
    def value(self) -> int:
        """value."""
        return int(self.serial_number)
