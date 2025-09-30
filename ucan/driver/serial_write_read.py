""""""

import threading
import time
from typing import Any

from ..models.base_model import FunctionCode
from ..models.responses import Ack
from ..models.responses.base_response import DeviceInfoResponse, DeviceSerialResponse
from ..models.responses.can_setup_response import CanSetupResponse
from ..models.responses.data_response import DataResponse
from ..models.responses.system_control_response import SystemControlResponse
from .serial_connection import SerialConnection


class SerialWriteRead(SerialConnection):
    """SerialWriteRead"""

    def __init__(self, port: str) -> None:
        """init"""
        super().__init__(port)
        self.__server_status: bool = False
        self.ack: Any = None
        self.response: Any = None
        self.data: Any = None

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
        pocket_suffix = bytes.fromhex("452e")
        ack_header = bytes.fromhex("5aff")
        data_header = bytes.fromhex("5a")
        data_suffix = bytes.fromhex("a5")
        try:
            assert self.serial is not None
            buffer = b""
            while self.server_status:
                response = self.serial.read(1024)
                if not response:
                    continue
                else:
                    response = buffer + response
                    # print("recv:", response.hex())
                    pocket_flag = False
                    ack_flag = False
                    data_flag = False
                    while True:
                        if response.startswith(pocket_header):
                            temp = response[:22]
                            if temp.endswith(pocket_suffix):
                                response = response[22:]
                                pocket_flag = True
                                ack_flag = False
                                data_flag = False
                                # print("res:", temp.hex(), len(response))

                                function_code = temp[2]
                                if function_code == FunctionCode.device_info.value:
                                    self.response = DeviceInfoResponse.parse(temp[4:])
                                    # print(DeviceInfoResponse.parse(temp[4:]))
                                if function_code == FunctionCode.device_serial.value:
                                    self.response = DeviceSerialResponse.parse(temp[4:])
                                    # print(DeviceSerialResponse.parse(temp[4:]))
                                if function_code == FunctionCode.can_config.value:
                                    self.response = CanSetupResponse.parse(temp[4:])
                                    # print(CanSetupResponse.parse(temp[4:]))
                                    # case FunctionCode.can_filter_config:
                                    #     DeviceInfoResponse.parse(response[4:])
                                if function_code == FunctionCode.system_control.value:
                                    self.response = SystemControlResponse.parse(temp[4:])
                                continue
                        else:
                            pocket_flag = True

                        if response.startswith(ack_header):
                            temp = response[:17]
                            if temp.endswith(data_suffix):
                                response = response[17:]
                                pocket_flag = False
                                ack_flag = True
                                data_flag = False
                                self.ack = Ack.parse(temp[2:])
                                # print(self.ack)
                                continue
                        else:
                            ack_flag = True
                        if response.startswith(data_header):
                            data_length = response[1]
                            data_length = 0x7F & data_length
                            temp = response[: 8 + data_length]
                            if temp.endswith(data_suffix):
                                pocket_flag = False
                                ack_flag = False
                                data_flag = True
                                response = response[8 + data_length :]
                                self.data = DataResponse.parse(temp[1:])
                                # print("recv:", temp.hex())
                                # print(self.data)
                                continue
                        else:
                            data_flag = True
                        if data_flag and pocket_flag and ack_flag:
                            buffer = response
                            break
                        if not self.__server_status:
                            break

            return
        except Exception as e:
            self.__server_status = False
            raise e

    def write(self, data: bytes) -> None:
        """write"""
        assert self.serial is not None
        self.serial.write(data)
