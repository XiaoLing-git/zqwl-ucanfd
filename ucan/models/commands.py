""""""

from pydantic import BaseModel

from ucan.models.base_model import FunctionCode, Motion


class BaseCommandModel(BaseModel):  # type: ignore[misc]
    """Base Command Model"""

    header: int = 0x4938
    function_code: FunctionCode
    motion: Motion
    data: bytes
    suffix: int = 0x452E

    def build(self) -> str:
        """build"""
        return (
            f"{int.to_bytes(self.header,byteorder='big', length=2).hex()}"
            f"{int.to_bytes(self.function_code.value,byteorder='big', length=1).hex()}"
            f"{int.to_bytes(self.motion.value,byteorder='big', length=1).hex()}"
            f"{self.data.hex()}"
            f"{int.to_bytes(self.suffix,byteorder='big', length=2).hex()}"
        )

    def cmd(self) -> bytes:
        """cmd"""
        return bytes.fromhex(self.build())

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("  # type: ignore[str-bytes-safe]
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
    data: bytes = bytes(16)


if __name__ == "__main__":
    print(GetDeviceInfoCommand().build())
    print(GetDeviceInfoCommand().cmd())
    print(GetDeviceInfoCommand())
