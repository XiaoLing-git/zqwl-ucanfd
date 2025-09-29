""""""

from __future__ import annotations

from pydantic import BaseModel

from ..base_model import BusState, FunctionCode, Status


class Ack(BaseModel):  # type: ignore[misc]
    """Ack"""

    function_code: FunctionCode = FunctionCode.ack_1
    can0: Status
    can1: Status
    can0_bus: BusState
    can1_bus: BusState
    can0_recv_speed: int
    can0_send_speed: int
    can0_recv_error_count: int
    can0_send_error_count: int
    can1_recv_speed: int
    can1_send_speed: int
    can1_recv_error_count: int
    can1_send_error_count: int

    @classmethod
    def parse(cls, data: bytes) -> Ack:
        """parse"""
        print(data[0])
        return cls(
            can0=cls.get_can0_status(data=data[8]),
            can1=cls.get_can1_status(data=data[8]),
            can0_bus=cls.get_can0_bus_status(data[8]),
            can1_bus=cls.get_can1_bus_status(data[8]),
            can0_send_speed=int(data[0:2].hex(), 16),
            can0_recv_speed=int(data[2:4].hex(), 16),
            can1_send_speed=int(data[4:6].hex(), 16),
            can1_recv_speed=int(data[6:8].hex(), 16),
            can0_send_error_count=data[10],
            can0_recv_error_count=data[11],
            can1_send_error_count=data[12],
            can1_recv_error_count=data[13],
        )

    def __str__(self) -> str:
        """__str__"""
        return (
            f"{self.__class__.__name__}("
            f"can0 = {self.can0}, "
            f"can1 = {self.can1}, "
            f"can0_bus = {self.can0_bus}, "
            f"can1_bus = {self.can1_bus}, "
            f"can0_send_speed = {self.can0_send_speed}, "
            f"can0_recv_speed = {self.can0_recv_speed}, "
            f"can1_send_speed = {self.can1_send_speed}, "
            f"can1_recv_speed = {self.can1_recv_speed}, "
            f"can0_send_error_count = {self.can0_send_error_count}, "
            f"can0_recv_error_count = {self.can0_recv_error_count}, "
            f"can1_send_error_count = {self.can1_send_error_count}, "
            f"can1_recv_error_count = {self.can1_recv_error_count}"
            f")"
        )

    @staticmethod
    def get_can0_status(data: int) -> Status:
        """"""
        value = (0x20 & data) >> 5
        if value == Status.off.value:
            return Status.off
        else:
            return Status.on

    @staticmethod
    def get_can1_status(data: int) -> Status:
        """"""
        value = (0x10 & data) >> 4
        if value == Status.off.value:
            return Status.off
        else:
            return Status.on

    @staticmethod
    def get_can0_bus_status(data: int) -> BusState:
        """"""
        value = (0x0C & data) >> 2
        return BusState.map_obj(value)

    @staticmethod
    def get_can1_bus_status(data: int) -> BusState:
        """"""
        value = (0x03 & data) >> 2
        return BusState.map_obj(value)


class DeviceInfoResponse(BaseModel):  # type: ignore[misc]
    """DeviceInfoResponse"""

    model: str
    version: str

    @classmethod
    def parse(cls, data: bytes) -> DeviceInfoResponse:
        """parse"""
        return cls(model=data[:12].decode(encoding="ascii"), version=data[12:16].decode(encoding="ascii"))


class DeviceSerialResponse(BaseModel):  # type: ignore[misc]
    """DeviceSerialResponse"""

    sn: str

    @classmethod
    def parse(cls, data: bytes) -> DeviceSerialResponse:
        """parse"""
        return cls(sn=data[:8].hex())
