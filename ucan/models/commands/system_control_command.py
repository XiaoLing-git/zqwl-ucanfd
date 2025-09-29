""""""

from ..base_model import FunctionCode, Motion, Status
from .base_command import BaseCommandModel


class SystemControlCommand(BaseCommandModel):
    """System Control Command"""

    function_code: FunctionCode = FunctionCode.system_control
    motion: Motion = Motion.WRITE
    flash: Status = Status.off
    reset: Status = Status.off
    can0: Status = Status.off
    can1: Status = Status.off
    can2: Status = Status.off
    can3: Status = Status.off
    data: str = bytes(12).hex()

    def build(self) -> str:
        """build"""
        return (
            f"{int.to_bytes(self.header,byteorder='big', length=2).hex()}"
            f"{int.to_bytes(self.function_code.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.motion.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.flash.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.reset.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.can0.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.can1.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.can2.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.can3.value,byteorder='big', length=1).hex()}"
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
            f"flash = {self.flash}, "
            f"reset = {self.reset}, "
            f"can0 = {self.can0}, "
            f"can1 = {self.can1}, "
            f"can2 = {self.can2}, "
            f"can3 = {self.can3}, "
            f"data = {self.data}, "
            f"suffix = {self.suffix}"
            f")"
        )
