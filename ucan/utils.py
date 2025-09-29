""""""

from ucan.errors import HexStrException


def assert_hex_str(target: str) -> None:
    """
    assert hex str
    :param target:
    :return: None
    """
    if not isinstance(target, str):
        raise HexStrException(f"{target} can't be hex_str")

    target_str = "0123456789ABCDEF"
    for i in target:
        if i.upper() not in target_str:
            raise HexStrException(f"{i} can't be hex_str")
    if len(target) % 2 != 0:
        raise HexStrException(f"{target} can't be hex_str,length of target is odd")
