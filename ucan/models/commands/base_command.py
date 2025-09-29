""""""

from typing import Any

from pydantic import BaseModel

from ...utils import assert_hex_str
from ..base_model import FunctionCode, Motion


class BaseCommandModel(BaseModel):  # type: ignore[misc]
    """Base Command Model"""

    header: int = 0x4938
    function_code: FunctionCode
    motion: Motion
    data: str
    suffix: int = 0x452E

    def model_post_init(self, context: Any, /) -> None:
        """init"""
        assert_hex_str(self.data)

    def build(self) -> str:
        """build"""
        return (
            f"{int.to_bytes(self.header,byteorder='big', length=2).hex()}"
            f"{int.to_bytes(self.function_code.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.motion.value,byteorder='big', length=1).hex()}"
            f"{bytes.fromhex(self.data).hex()}"
            f"{int.to_bytes(self.suffix,byteorder='big', length=2).hex()}"
        )

    def cmd(self) -> bytes:
        """cmd"""
        return bytes.fromhex(self.build())

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("
            f"header = {self.header}, "
            f"function_code = {self.function_code}, "
            f"motion = {self.motion}, "
            f"data = {self.data}, "
            f"suffix = {self.suffix}"
            f")"
        )


class GetDeviceInfoCommand(BaseCommandModel):
    """Get Device Info Command"""

    function_code: FunctionCode = FunctionCode.device_info
    motion: Motion = Motion.READ
    data: str = bytes(16).hex()


class GetDeviceSerialCommand(BaseCommandModel):
    """Get Device Serial Command"""

    function_code: FunctionCode = FunctionCode.device_serial
    motion: Motion = Motion.READ
    data: str = bytes(16).hex()
