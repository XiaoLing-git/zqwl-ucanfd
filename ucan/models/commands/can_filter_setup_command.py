""""""

from typing import Any

from ...utils import assert_hex_str
from ..base_model import Channel, FilterFrame, FunctionCode, Motion, Status
from .base_command import BaseCommandModel


class CanFilterSetupCommand(BaseCommandModel):
    """Can Filter Setup Command"""

    function_code: FunctionCode = FunctionCode.can_filter_config
    motion: Motion = Motion.WRITE
    channel: Channel
    group: int
    status: Status
    frame_type: FilterFrame
    accept_id: int
    mask: int
    data: str = bytes(4).hex()

    def model_post_init(self, context: Any, /) -> None:
        """init."""
        assert_hex_str(self.data)
        if self.frame_type is FilterFrame.standard:
            self.accept_id = 0x0000FFFF & self.accept_id
            self.accept_id = self.accept_id << 16
            self.mask = 0x0000FFFF & self.mask
            self.mask = self.mask << 16

    def build(self) -> str:
        """build"""
        return (
            f"{int.to_bytes(self.header,byteorder='big', length=2).hex()}"
            f"{int.to_bytes(self.function_code.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.motion.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.channel.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.group,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.status.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.frame_type.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.accept_id,byteorder='big', length=4).hex()}"
            f"{int.to_bytes(self.mask,byteorder='big', length=4).hex()}"
            f"{bytes.fromhex(self.data).hex()}"
            f"{int.to_bytes(self.suffix,byteorder='big', length=2).hex()}"
        )

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("
            f"header = {self.header}, "
            f"function_code = {self.function_code}, "
            f"motion = {self.motion}, "
            f"channel = {self.channel}, "
            f"group = {self.group}, "
            f"status = {self.status}, "
            f"frame_type = {self.frame_type}, "
            f"accept_id = {int.to_bytes(self.accept_id,byteorder='big',length=4).hex()}, "
            f"mask = {int.to_bytes(self.mask,byteorder='big',length=4).hex()}, "
            f"data = {self.data}, "
            f"suffix = {self.suffix}"
            f")"
        )
