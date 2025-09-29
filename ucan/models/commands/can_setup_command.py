""""""

from typing import Any

from ...utils import assert_hex_str
from ..base_model import ArbitrationBaudRate, Channel, CustomBaud, DataFieldBaudRate, FunctionCode, Motion
from .base_command import BaseCommandModel


class CanSetupCommand(BaseCommandModel):
    """Can Setup Command"""

    function_code: FunctionCode = FunctionCode.can_config
    motion: Motion = Motion.WRITE
    channel: Channel
    custom_baud: CustomBaud = CustomBaud.disable
    arbitration_baud: ArbitrationBaudRate
    data_field_baud: DataFieldBaudRate
    data: str = bytes(13).hex()

    def build(self) -> str:
        """build"""
        return (
            f"{int.to_bytes(self.header,byteorder='big', length=2).hex()}"
            f"{int.to_bytes(self.function_code.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.motion.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.channel.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.custom_baud.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.arbitration_baud.value | self.data_field_baud.value,byteorder='big', length=1).hex()}"
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
            f"custom_baud = {self.custom_baud}, "
            f"arbitration_baud = {self.arbitration_baud}, "
            f"data_field_baud = {self.data_field_baud}, "
            f"data = {self.data}, "
            f"suffix = {self.suffix}"
            f")"
        )


class CanCustomSetupCommand(BaseCommandModel):
    """Can Custom Setup Command"""

    function_code: FunctionCode = FunctionCode.can_config
    motion: Motion = Motion.WRITE
    channel: Channel
    custom_baud: CustomBaud = CustomBaud.enable
    arbitration_baud: int = 0xF0
    data_field_baud: int = 0x0F
    arbitration_sjw: int
    arbitration_tseg1: int
    arbitration_tseg2: int
    arbitration_brp: int
    data_field_sjw: int
    data_field_tseg1: int
    data_field_tseg2: int
    data_field_brp: int
    data: str = bytes(2).hex()

    def model_post_init(self, context: Any, /) -> None:
        """init"""
        assert_hex_str(self.data)
        assert 0x00 <= self.arbitration_sjw < 0x03
        assert 0x00 <= self.arbitration_tseg1 < 0x03F
        assert 0x00 <= self.arbitration_tseg2 < 0x07
        assert 0x01 <= self.arbitration_brp < 0x0400
        assert 0x00 <= self.data_field_sjw < 0x03
        assert 0x00 <= self.data_field_tseg1 < 0x03F
        assert 0x00 <= self.data_field_tseg2 < 0x07
        assert 0x01 <= self.data_field_brp < 0x0400

    def build(self) -> str:
        """build"""
        return (
            f"{int.to_bytes(self.header,byteorder='big', length=2).hex()}"
            f"{int.to_bytes(self.function_code.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.motion.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.channel.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.custom_baud.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.arbitration_baud | self.data_field_baud,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.arbitration_sjw,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.arbitration_tseg1,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.arbitration_tseg2,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.arbitration_brp,byteorder='big', length=2).hex()}"
            f"{int.to_bytes(self.data_field_sjw,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.data_field_tseg1,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.data_field_tseg2,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.data_field_brp,byteorder='big', length=2).hex()}"
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
            f"custom_baud = {self.custom_baud}, "
            f"arbitration_baud = {self.arbitration_baud}, "
            f"data_field_baud = {self.data_field_baud}, "
            f"arbitration_sjw = {self.arbitration_sjw}, "
            f"arbitration_tseg1 = {self.arbitration_tseg1}, "
            f"arbitration_tseg2 = {self.arbitration_tseg2}, "
            f"arbitration_brp = {self.arbitration_brp}, "
            f"data_field_sjw = {self.data_field_sjw}, "
            f"data_field_tseg1 = {self.data_field_tseg1}, "
            f"data_field_tseg2 = {self.data_field_tseg2}, "
            f"data_field_brp = {self.data_field_brp}, "
            f"data = {self.data}, "
            f"suffix = {self.suffix}"
            f")"
        )
