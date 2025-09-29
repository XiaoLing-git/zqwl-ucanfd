""""""

from ucan.models.base_model import ArbitrationBaudRate, Channel, DataFieldBaudRate
from ucan.models.commands.base_command import GetDeviceInfoCommand, GetDeviceSerialCommand
from ucan.models.commands.can_setup_command import CanSetupCommand

if __name__ == "__main__":
    print(GetDeviceInfoCommand().build())
    print(GetDeviceInfoCommand().cmd())
    print(GetDeviceInfoCommand())
    print("-" * 100)
    print(GetDeviceSerialCommand().build())
    print(GetDeviceSerialCommand().cmd())
    print(GetDeviceSerialCommand())
    print("-" * 100)
    cmd = CanSetupCommand(
        channel=Channel.C1,
        arbitration_baud=ArbitrationBaudRate.BAUD_50KBPS,
        data_field_baud=DataFieldBaudRate.BAUD_500KBPS,
    )

    print(cmd.build())
    print(cmd.cmd())
    print(cmd)
