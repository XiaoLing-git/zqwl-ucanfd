import time

import serial

from ucan.models.base_model import Channel, ArbitrationBaudRate, DataFieldBaudRate
from ucan.models.commands import GetDeviceInfoCommand, GetDeviceSerialCommand, CanSetupCommand
from ucan.models.responses.base_response import DeviceInfoResponse, DeviceSerialResponse
from ucan.models.responses.can_setup_response import CanSetupResponse

if __name__ == '__main__':
    ser = serial.Serial("COM15", baudrate=6000000, timeout=0.1)
    cmd = CanSetupCommand(
        channel=Channel.C0,
        arbitration_baud=ArbitrationBaudRate.BAUD_250KBPS,
        data_field_baud=DataFieldBaudRate.BAUD_500KBPS
    )
    print(cmd.build())

    start_time = time.time()
    while True:
        if time.time() - start_time > 10:
            break
        ser.write(cmd.cmd())
        res= ser.read_until(b"452e")
        print(CanSetupResponse.parse(res[4:]))
    ser.close()
