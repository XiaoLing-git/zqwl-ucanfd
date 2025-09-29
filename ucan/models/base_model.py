""""""

from enum import Enum


class Status(Enum):
    """Status"""

    off = 0x00
    on = 0x01


class Motion(Enum):
    """Motion"""

    READ = 0x52
    WRITE = 0x57


class DeviceType(Enum):
    """
    0xFF	单双通道设备（如 ZQWL-UCANFD-100C、ZQWL-UCAN-201U等）反馈单双通道设备的 CAN0~CAN1 状态、收发速率、错误计数器等	17 字节
    0xFE	4通道设备（如 ZQWL-UCANFD-400U、ZQWL-UCAN-401U等）反馈4通道设备的 CAN0~CAN3 状态、收发速率、错误计数器等 32 字节
    """

    device_with_1_and_2_channel = 0xFF
    device_with_4_channel = 0xFE


class ProtocolType(Enum):
    """
    0x00    CAN 协议（传统 CAN 总线）
    0x01    CANFD 协议（CAN Flexible Data Rate，灵活数据率 CAN）
    """

    Can = 0x00
    CanFD = 0x01


class CustomBaud(Enum):
    """
    0x00-常用波特率,
    0x01-自定义
    """

    disable = 0x00
    enable = 0x01


class FunctionCode(Enum):
    """
    0x40	设备信息	读取设备型号、硬件版本等基础信息	仅读（0x52），不支持写
    0x41	设备序列号	读取设备唯一序列号	仅读（0x52），不支持写
    0x42	CAN 参数	配置 CAN 通道的波特率（仲裁域 / 数据域）、滤波器等参数	读（0x52）/ 写（0x57）均支持
    0x44	系统控制	实现参数生效（保存到 Flash，断电不丢失）、系统复位、CAN 通道开关（开启 / 关闭 CAN0~CAN3）
            等控制	读（0x52）/ 写（0x57）均支持
    """

    device_info = 0x40
    device_serial = 0x41
    can_config = 0x42
    system_control = 0x44


class Channel(Enum):
    """Channel"""

    C0 = 0x00
    C1 = 0x01
    C2 = 0x02
    C3 = 0x03


class FilterFrame(Enum):
    """
    标准帧（Standard Frame）：滤波器帧类型标识为0x00，仅对11 位 ID的 CAN (FD) 报文生效
    扩展帧（Extended Frame）：滤波器帧类型标识为0x01，仅对29 位 ID的 CAN (FD) 报文生效
    """

    standard = 0x00
    extended = 0x01


class FrameType(Enum):
    """
    0x00 数据帧 用于传输实际的 CAN (FD) 数据，是设备间传递业务信息（如传感器数据、控制指令）的主要载体，需携带具体数据内容。
    0x01 远程帧 用于请求目标节点发送指定 ID 的 CAN (FD) 数据，自身不携带实际数据，仅通过帧 ID 指定请求的数据标识。
    """

    data = 0x00
    remote = 0x01


class BusState(Enum):
    """
    00	总线正常	总线通讯无异常，数据收发顺畅，无错误帧干扰；此时发送 / 接收错误计数器通常维持在 0，无需干预
    01	总线警告	总线出现轻微异常（如偶发电磁干扰导致的错误帧），但仍可正常传输数据；需关注错误计数器变化，避免异常加剧
    10	总线被动错误	总线错误帧数量较多，设备进入 “被动错误状态”，通讯稳定性下降（如数据延迟、偶发丢帧）；
        需排查总线阻塞、节点冲突、波特率不匹配等问题
    11	设备离线	总线故障严重（如短路、断线、节点过载），设备已无法参与 CAN (FD) 通讯，既不能发送也不能接收报文；
        需紧急排查总线硬件连接或网络配置
    """

    normal = 0x00
    warning = 0x01
    error = 0x02
    offline = 0x03


class ArbitrationBaudRate(Enum):
    """
    仲裁域波特率枚举（对应CAN协议波特率，常用波特率码高4位）
    """

    BAUD_1000KBPS = 0x00 << 4
    BAUD_800KBPS = 0x01 << 4
    BAUD_500KBPS = 0x02 << 4
    BAUD_400KBPS = 0x03 << 4
    BAUD_250KBPS = 0x04 << 4
    BAUD_200KBPS = 0x05 << 4
    BAUD_125KBPS = 0x06 << 4
    BAUD_100KBPS = 0x07 << 4
    BAUD_50KBPS = 0x08 << 4
    BAUD_40KBPS = 0x09 << 4
    BAUD_25KBPS = 0x0A << 4
    BAUD_20KBPS = 0x0B << 4
    BAUD_15KBPS = 0x0C << 4
    BAUD_10KBPS = 0x0D << 4
    BAUD_5KBPS = 0x0E << 4


class DataFieldBaudRate(Enum):
    """
    数据域波特率枚举（对应CANFD数据域波特率，常用波特率码低4位）
    """

    BAUD_5000KBPS = 0x00
    BAUD_4000KBPS = 0x01
    BAUD_2000KBPS = 0x02
    BAUD_1000KBPS = 0x03
    BAUD_800KBPS = 0x04
    BAUD_500KBPS = 0x05
    BAUD_400KBPS = 0x06
    BAUD_250KBPS = 0x07
    BAUD_200KBPS = 0x08
    BAUD_125KBPS = 0x09
    BAUD_100KBPS = 0x0A
