"""Singleton class for serial number management of command models"""

from __future__ import annotations


class SerialNumber:
    """"""

    _instance = None

    def __new__(cls) -> SerialNumber:
        """__new__."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.serial_number = -1  # type: ignore[has-type]
        return cls._instance

    def __init__(self) -> None:
        """init."""
        self.serial_number = self.serial_number + 1  # type: ignore[has-type]
        self.serial_number = self.serial_number & 0xFFFF

    @property
    def hex(self) -> str:
        """hex."""
        return int.to_bytes(self.serial_number, byteorder="little", length=2).hex()

    @property
    def value(self) -> int:
        """value."""
        return int(self.serial_number)
