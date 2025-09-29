""""""

from __future__ import annotations

from pydantic import BaseModel

from ucan.models.base_model import Status


class SystemControlResponse(BaseModel):  # type: ignore[misc]
    """System Control Command"""

    flash: Status = Status.off
    reset: Status = Status.off
    can0: Status = Status.off
    can1: Status = Status.off
    can2: Status = Status.off
    can3: Status = Status.off

    @classmethod
    def parse(cls, data: bytes) -> SystemControlResponse:
        """parse"""
        return cls(
            flash=Status.map_obj(data[0]),
            reset=Status.map_obj(data[1]),
            can0=Status.map_obj(data[2]),
            can1=Status.map_obj(data[3]),
            can2=Status.map_obj(data[4]),
            can3=Status.map_obj(data[5]),
        )

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("
            f"flash = {self.flash}, "
            f"reset = {self.reset}, "
            f"can0 = {self.can0}, "
            f"can1 = {self.can1}, "
            f"can2 = {self.can2}, "
            f"can3 = {self.can3}"
            f")"
        )
