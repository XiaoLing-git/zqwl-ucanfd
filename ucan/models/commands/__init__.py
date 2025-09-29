""""""

from ucan.models.base_model import ArbitrationBaudRate, Channel, DataFieldBaudRate
from ucan.models.commands.base_command import GetDeviceInfoCommand, GetDeviceSerialCommand
from ucan.models.commands.can_setup_command import CanCustomSetupCommand, CanSetupCommand

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
    print("-" * 100)
    cmd = CanCustomSetupCommand(
        channel=Channel.C1,
        arbitration_sjw=1,
        arbitration_tseg1=2,
        arbitration_tseg2=3,
        arbitration_brp=4,
        data_field_sjw=2,
        data_field_tseg1=3,
        data_field_tseg2=4,
        data_field_brp=5,
    )

    print(cmd.build())
    print(cmd.cmd())
    print(cmd)
