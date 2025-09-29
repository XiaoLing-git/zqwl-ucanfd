import time

import serial

from ucan.models.commands import GetDeviceInfoCommand, GetDeviceSerialCommand
from ucan.models.responses.base_response import DeviceInfoResponse, DeviceSerialResponse

if __name__ == '__main__':
    ser = serial.Serial("COM15", baudrate=6000000, timeout=0.1)
    cmd = GetDeviceSerialCommand()
    print(cmd.build())

    start_time = time.time()
    while True:
        if time.time() - start_time > 10:
            break
        ser.write(cmd.cmd())
        res= ser.read_until(b"452e")
        d = DeviceSerialResponse.parse(res[4:])
        print(d)
    ser.close()
