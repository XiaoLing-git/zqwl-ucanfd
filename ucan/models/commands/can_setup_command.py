""""""

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
