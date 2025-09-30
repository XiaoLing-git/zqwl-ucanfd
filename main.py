import time

import serial

from ucan.driver.serial_write_read import SerialWriteRead
from ucan.models.base_model import Channel, ArbitrationBaudRate, DataFieldBaudRate, Status, DataSendType, FilterFrame, \
    FrameType, ProtocolType
from ucan.models.commands import GetDeviceInfoCommand, GetDeviceSerialCommand, CanSetupCommand, SystemControlCommand
from ucan.models.data.base_data import BaseDataModel
from ucan.models.responses.base_response import DeviceInfoResponse, DeviceSerialResponse
from ucan.models.responses.can_setup_response import CanSetupResponse
from ucan.models.responses.system_control_response import SystemControlResponse
from ucan.serial_number import SerialNumber

if __name__ == '__main__':
    # ser = serial.Serial("COM15", baudrate=6000000, timeout=0.1)
    # cmd = CanSetupCommand(
    #     channel=Channel.C0,
    #     arbitration_baud=ArbitrationBaudRate.BAUD_250KBPS,
    #     data_field_baud=DataFieldBaudRate.BAUD_500KBPS
    # )
    # print(cmd.build())
    # ser.write(cmd.cmd())
    # res = ser.read_until(b"452e")
    # res = CanSetupResponse.parse(res[4:])
    # print(res)
    #
    # cmd = SystemControlCommand(
    #     flash=Status.on,
    #     can0=Status.on
    # )
    # print(cmd.build())
    # ser.write(cmd.cmd())
    # res = ser.read_until(b"452e")
    # res = SystemControlResponse.parse(res[4:])
    # print(res)
    #
    # start_time = time.time()
    # while True:
    #     if time.time() - start_time > 5:
    #         break
    #     time.sleep(0.01)
    #     res = ser.read_all().hex()
    #     print("res:",res)
    #
    # device = SerialWriteRead("COM15")
    # device.connect()
    #
    # cmd = CanSetupCommand(
    #     channel=Channel.C0,
    #     arbitration_baud=ArbitrationBaudRate.BAUD_250KBPS,
    #     data_field_baud=DataFieldBaudRate.BAUD_500KBPS
    # )
    # device.write(cmd.cmd())
    # time.sleep(1)
    # cmd = SystemControlCommand(
    #     flash=Status.on,
    #     can0=Status.on
    # )
    # device.write(cmd.cmd())
    #
    # time.sleep(5)
    # device.disconnect()

    # data = BaseDataModel(
    #     channel=Channel.C0,
    #     dlc=8,
    #     send_type=DataSendType.normal,
    #     filter_frame=FilterFrame.standard,
    #     frame_type=FrameType.data,
    #     accelerate=Status.on,
    #     protocol_type=ProtocolType.Can,
    #     can_id=0x55,
    #     data="1112131415161718"
    # )
    # print(data.build())
    # print(data)

    for i in range(0x556):
        res = SerialNumber()
        print(res.value, res.hex)


