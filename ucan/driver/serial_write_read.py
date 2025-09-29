""""""

import threading
import time

from ..models.base_model import FunctionCode
from ..models.responses import Ack
from ..models.responses.base_response import DeviceInfoResponse, DeviceSerialResponse
from ..models.responses.can_setup_response import CanSetupResponse
from ..models.responses.system_control_response import SystemControlResponse
from .serial_connection import SerialConnection


class SerialWriteRead(SerialConnection):
    """SerialWriteRead"""

    def __init__(self, port: str) -> None:
        """init"""
        super().__init__(port)
        self.__server_status: bool = False

    @property
    def server_status(self) -> bool:
        """get server status"""
        return self.__server_status

    def stop_server(self) -> None:
        """stop server"""
        self.__server_status = False
        time.sleep(0.5)

    def connect(self) -> None:
        """connect"""
        super().connect()
        self.__server_status = True
        threading.Thread(target=self.__server).start()

    def disconnect(self) -> None:
        """disconnect"""
        self.stop_server()
        super().disconnect()

    def __server(self) -> None:
        """__server"""
        pocket_header = bytes.fromhex("493b")
        ack_header = bytes.fromhex("5aff")
        try:
            assert self.serial is not None
            while self.server_status:
                response = self.serial.read(32)
                if not response:
                    continue
                else:
                    if response.startswith(pocket_header):
                        function_code = response[2]
                        match function_code:
                            case FunctionCode.device_info.value:
                                print(DeviceInfoResponse.parse(response[4:]))
                            case FunctionCode.device_serial.value:
                                print(DeviceSerialResponse.parse(response[4:]))
                            case FunctionCode.can_config.value:
                                print(CanSetupResponse.parse(response[4:]))
                            # case FunctionCode.can_filter_config:
                            #     DeviceInfoResponse.parse(response[4:])
                            case FunctionCode.system_control.value:
                                print(SystemControlResponse.parse(response[4:]))
                    if response.startswith(ack_header):
                        print(Ack.parse(response[2:]))
            return
        except Exception as e:
            self.__server_status = False
            raise e

    def write(self, data: bytes) -> None:
        """write"""
        assert self.serial is not None
        self.serial.write(data)
