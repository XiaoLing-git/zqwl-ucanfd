""""""

from __future__ import annotations

from pydantic import BaseModel

from ucan.models.base_model import ArbitrationBaudRate, Channel, CustomBaud, DataFieldBaudRate, FunctionCode, Motion


class CanSetupResponse(BaseModel):  # type: ignore[misc]
    """Can Setup Command"""

    channel: Channel
    custom_baud: CustomBaud = CustomBaud.disable
    arbitration_baud: ArbitrationBaudRate
    data_field_baud: DataFieldBaudRate

    @classmethod
    def parse(cls, data: bytes) -> CanSetupResponse:
        """parse"""
        return cls(
            channel=Channel.map_obj(data[0]),
            custom_baud=CustomBaud.map_obj(data[1]),
            arbitration_baud=ArbitrationBaudRate.map_obj(data[2]),
            data_field_baud=DataFieldBaudRate.map_obj(data[2]),
        )

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("
            f"channel = {self.channel}, "
            f"custom_baud = {self.custom_baud}, "
            f"arbitration_baud = {self.arbitration_baud}, "
            f"data_field_baud = {self.data_field_baud}"
            f")"
        )
