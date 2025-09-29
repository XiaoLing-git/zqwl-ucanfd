""""""

from typing import Any

from pydantic import BaseModel

from ucan.models.base_model import Channel, DataSendType, FilterFrame, FrameType, ProtocolType, Status
from ucan.utils import assert_hex_str


class BaseDataModel(BaseModel):  # type: ignore[misc]
    """Base Data Model"""

    header: int = 0x5A
    channel: Channel
    dlc: int
    send_type: DataSendType
    filter_frame: FilterFrame
    frame_type: FrameType
    accelerate: Status = Status.on
    protocol_type: ProtocolType
    can_id: int
    data: str
    suffix: int = 0xA5

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("
            f"header = {self.header}, "
            f"channel = {self.channel}, "
            f"dlc = {self.dlc}, "
            f"send_type = {self.send_type}, "
            f"filter_frame = {self.filter_frame}, "
            f"frame_type = {self.frame_type}, "
            f"accelerate = {self.accelerate}, "
            f"protocol_type = {self.protocol_type}, "
            f"can_id = {self.can_id}, "
            f"accelerate = {self.accelerate}, "
            f"data = {self.data}"
            f")"
        )

    def model_post_init(self, context: Any, /) -> None:
        """init"""
        assert_hex_str(self.data)

    def cmd(self) -> bytes:
        """cmd"""
        return bytes.fromhex(self.build())

    def build(self) -> str:
        """build"""
        return (
            f"{int.to_bytes(self.header,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.get_byte_1(),byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.get_byte_2(), byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.get_byte_3_6(), byteorder='big', length=4).hex()}"
            f"{self.data}"
            f"{int.to_bytes(self.suffix,byteorder='big', length=1).hex()}"
        )

    def get_byte_1(self) -> int:
        """get_byte_1"""
        dlc = self.dlc & 0x7F
        channel = (self.channel.value & 0x01) << 7
        return dlc | channel

    def get_byte_2(self) -> int:
        """get_byte_2"""
        send_type = self.send_type.value << 6
        channel = (self.channel.value & 0x06) << 3
        filter_frame = self.filter_frame.value << 2
        frame_type = self.frame_type.value << 1
        return send_type | channel | filter_frame | frame_type | self.accelerate.value

    def get_byte_3_6(self) -> int:
        """get_byte_3 ~ 6"""
        protocol_type = self.protocol_type.value << 31
        print(protocol_type)
        print(self.can_id)
        return protocol_type | self.can_id
