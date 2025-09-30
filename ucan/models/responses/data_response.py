""""""

from __future__ import annotations

from pydantic import BaseModel

from ucan.models.base_model import Channel, DataSendType, FilterFrame, FrameType, ProtocolType, Status


class DataResponse(BaseModel):  # type: ignore[misc]
    """Data Command"""

    dlc: int
    # send_type: DataSendType
    filter_frame: FilterFrame
    frame_type: FrameType
    accelerate: Status = Status.on
    can_id: str = ""
    data: str

    @classmethod
    def parse(cls, data: bytes) -> DataResponse:
        """parse"""
        return cls(
            dlc=(data[0] & 0x7F),
            # send_type=DataSendType.map_obj((data[0] & 0xc0) >> 6),
            filter_frame=FilterFrame.map_obj((data[1] & 0x04) >> 2),
            frame_type=FrameType.map_obj((data[1] & 0x2) >> 1),
            accelerate=Status.map_obj((data[1] & 0x01)),
            can_id=data[2:6].hex(),
            data=data[6:-1].hex(),
        )

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("
            f"dlc = {self.dlc}, "
            # f"send_type = {self.send_type}, "
            f"filter_frame = {self.filter_frame}, "
            f"frame_type = {self.frame_type}, "
            f"accelerate = {self.accelerate}, "
            f"can_id = {self.can_id}, "
            f"data = {self.data}"
            f")"
        )
