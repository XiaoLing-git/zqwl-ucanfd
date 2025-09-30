# import time
#
# import serial
#
# from ucan.driver.serial_write_read import SerialWriteRead
# from ucan.models.base_model import Channel, ArbitrationBaudRate, DataFieldBaudRate, Status, DataSendType, FilterFrame, \
#     FrameType, ProtocolType
# from ucan.models.commands import GetDeviceInfoCommand, GetDeviceSerialCommand, CanSetupCommand, SystemControlCommand
# from ucan.models.data.base_data import BaseDataModel
# from ucan.models.responses.base_response import DeviceInfoResponse, DeviceSerialResponse
# from ucan.models.responses.can_setup_response import CanSetupResponse
# from ucan.models.responses.system_control_response import SystemControlResponse
# from ucan.serial_number import SerialNumber
#
# if __name__ == '__main__':
#
#     device = SerialWriteRead("COM15")
#     device.connect()
#
#     cmd = CanSetupCommand(
#         channel=Channel.C0,
#         arbitration_baud=ArbitrationBaudRate.BAUD_1000KBPS,
#         data_field_baud=DataFieldBaudRate.BAUD_1000KBPS
#     )
#     device.write(cmd.cmd())
#     time.sleep(1)
#     cmd = SystemControlCommand(
#         flash=Status.on,
#         can0=Status.on
#     )
#     device.write(cmd.cmd())
#
#     # data = BaseDataModel(
#     #     channel=Channel.C0,
#     #     dlc = 4,
#     #     send_type=DataSendType.single,
#     #     filter_frame=FilterFrame.standard,
#     #     frame_type=FrameType.data,
#     #     accelerate=Status.off,
#     #     protocol_type=ProtocolType.Can,
#     #     can_id=0x110,
#     #     data="7f5aa50a"
#     # )
#     # print(data.build())
#     # device.write(data.cmd())
#
#
#     while True:
#         time.sleep(1)




import os
import time

from serial import Serial

from ucan.driver.serial_write_read import SerialWriteRead
from ucan.models.base_model import Channel, DataSendType, FilterFrame, FrameType, Status, ProtocolType
from ucan.models.data.base_data import BaseDataModel


class YModem:
    def __init__(self):
        self.ser = None
        self.EOT = b'\x04'
        self.ACK = b'\x06'
        self.NAK = b'\x15'
        self.CAN = b'\x18'
        self.CRC = b'\x43'
        self.ACK_FLAG = False

    @staticmethod
    def crc16(x, invert):
        crc_in = 0x0000
        poly = 0x1021
        for b in x:
            if type(b) is str:  # 这里做了个判断可以直接传入字符串，但存在意义不大
                crc_in ^= (ord(b) << 8)
            else:
                crc_in ^= (b << 8)
            for i in range(8):
                if crc_in & 0x8000:
                    crc_in = (crc_in << 1) ^ poly
                else:
                    crc_in = (crc_in << 1)
        s = hex(crc_in).upper()
        # return (s[-2:], s[-4:-2]) if invert else (s[-4:-2], s[-2:])
        return (s[-2:], s[-4:-2]) if invert else (s[-4:-2], s[-2:])

    @staticmethod
    def str2hex(s):
        i_data = 0
        su = s.upper()
        for c in su:
            tmp = ord(c)
            if tmp <= ord('9'):
                i_data = i_data << 4
                i_data += tmp - ord('0')
            elif ord('A') <= tmp <= ord('F'):
                i_data = i_data << 4
                i_data += tmp - ord('A') + 10
        return i_data

    def open(self, port="COM15"):
        try:
            self.ser = SerialWriteRead(port)
            self.ser.connect()
            print(f'port {port} open ...')
            return True
        except Exception as e:
            print(f'serial {port} is not open {str(e)}')
            return False

    # 将ymodem数据拆分成can协议数据
    def ymodem_to_can(self, ymodem_data):
        can_data = []
        for i in range(0, len(ymodem_data), 8):
            can_data.append(ymodem_data[i:i+8])
        return can_data

    # 发送can协议数据
    def send_can(self, ymodem_data):
        can_data = self.ymodem_to_can(ymodem_data)
        for data in can_data:
            cmd = BaseDataModel(
                channel=Channel.C0,
                dlc = len(data),
                # send_type=DataSendType.single,
                filter_frame=FilterFrame.standard,
                frame_type=FrameType.data,
                accelerate=Status.off,
                protocol_type=ProtocolType.Can,
                can_id=0x110,
                data=data.hex()
            )
            self.ser.write(cmd.cmd())
            print(3, data)
            time.sleep(0.01)

    # 接收can协议数据
    def recv_can(self, read_len):
        # res = self.ser.data
        start_time = time.time()
        while self.ser.data is None:
            if time.time() -start_time >5:
                break
        print(1,self.ser.data)
        res = self.ser.data.data
        # print(res, bytes.fromhex(res))
        self.ser.data = None
        test = bytes.fromhex(res)
        # print(test[0])
        # if len(test) > 1:
        #     print(test[1])
        print("res: ", res, type(res))
        print("test: ", test, type(test))
        # return bytes.fromhex(res)
        return test
        # ymodem_data = b''
        # if read_len <= 8:
        #     data = self.ser.read(read_len)
        #     ymodem_data += data
        # else:
        #     loop_times = read_len // 8
        #     while loop_times > 0:
        #         data = self.ser.read(8)
        #         ymodem_data += data
        #         loop_times -= 1
        #     ymodem_data += self.ser.read(read_len % 8)
        # return ymodem_data

    def send_first(self, mode, file_name, file_size):
        if mode == 128:
            x = 1
        else:
            x = 2
        print('start send YModem first package')
        space = bytearray()
        header = bytearray([x, 0, 255])
        file_byte = bytearray([ord(i) for i in file_name])
        size = bytearray([ord(i) for i in str(file_size)])
        for i in range(mode - len(file_byte) - 1 - len(size)):
            space.append(0)
        a1, b1 = self.crc16(file_byte + bytearray([0]) + size + space, False)
        hex_a1 = self.str2hex(a1)
        hex_b1 = self.str2hex(b1)
        last = bytearray([hex_a1, hex_b1])
        data = header + file_byte + bytearray([0]) + size + space + last
        # self.ser.write(data)
        self.send_can(data)
        print('send first package success')

    def send_data(self, file_data, mode, package_count):
        print('start send file data')
        if mode == 128:
            x = 1
        else:
            x = 2
        for i in range(1, package_count + 1):
            header = bytearray()
            header.append(x)
            header.append(i % 256)
            header.append(255 - (i % 256))
            if i == package_count:
                data = bytearray(file_data[(i - 1) * mode:])
                for j in range(mode - len(data)):
                    data.append(26)
            else:
                data = file_data[(i - 1) * mode: i * mode]
            a1, b1 = self.crc16(data, False)
            hex_a1 = self.str2hex(a1)
            hex_b1 = self.str2hex(b1)
            last = bytearray([hex_a1, hex_b1])
            # self.ser.write(header + data + last)
            self.send_can(header + data + last)
            # 判断ack
            for j in range(10):
                # char = self.ser.read(1)
                char = self.recv_can(1)
                if char == self.ACK:
                    break
                elif char == self.NAK or j == 9:
                    print('error')
                    return False
                else:
                    continue

        # self.ser.write(self.EOT)
        self.send_can(self.EOT)
        # is_ack = self.ser.read(1)
        is_ack = self.recv_can(1)
        if is_ack == self.ACK:
            return True
        print('send file data end')

    def send_last(self, mode):
        print('send last data')
        if mode == 128:
            x = 1
        else:
            x = 2
        last_package = bytearray([x, 0, 255])
        for i in range(mode):
            last_package.append(0)
        # self.ser.write(last_package)
        self.send_can(last_package)
        # self.ser.write(bytearray([0, 0]))
        self.send_can(bytearray([0, 0]))
        for i in range(10):
            # is_ack = self.ser.read(1)
            is_ack = self.recv_can(1)
            if is_ack == self.ACK:
                print('send last ok')
                return True
        print('send last error')
        return False

    def send(self, file_path, mode=128):
        if not os.path.exists(file_path):
            print('file is not found')
            return False
        data_byte = bytes()
        with open(file_path, 'rb') as f:
            for i in f.readlines():
                data_byte += i
        name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        if file_size % mode >= 1:
            package_count = int(file_size / mode) + 1
        else:
            package_count = int(file_size / mode)
        count = 0
        while True:
            count += 1
            if count == 50:
                print('recv char is not crc')
                return False
            # char = self.ser.read(1)
            char = self.recv_can(1)
            print("char: ", char)
            if char == self.CRC:
                print('recv char is crc')
                self.send_first(mode, name, file_size)
                for i in range(30):
                    # is_ack = self.ser.read(1)
                    is_ack = self.recv_can(1)
                    if is_ack == self.ACK:
                        self.ACK_FLAG = True
                        break
                if self.ACK_FLAG:
                    self.send_data(data_byte, mode, package_count)
                    if self.send_last(mode):
                        return True
                    else:
                        print('send data ok but not start app')
            continue

    def close(self):
        self.ser.disconnect()
        self.ser = None


if __name__ == '__main__':
    y_mode = YModem()
    y_mode.open()
    y_mode.send(r'.\app.bin')
    y_mode.close()


