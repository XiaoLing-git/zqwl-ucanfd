"""Custom Exceptions."""

import logging

logger = logging.getLogger(__name__)


class UCanBaseException(Exception):
    """
    Base Exception For Usb To Can
    """

    def __init__(self, msg: str) -> None:
        """exception init"""
        self._msg = msg
        logger.error(f"{self.__class__.__name__} - {self._msg}")

    def __str__(self) -> str:
        """exception __str__"""
        return f"{self.__class__.__name__}(msg={self._msg})"

    def __repr__(self) -> str:
        """exception __repr__"""
        return f"{self.__class__.__name__}(msg={self._msg})"


class EnumItemNotExistError(UCanBaseException):
    """Enum Item Not Exist Error"""

    pass


class HexStrException(UCanBaseException):
    """Hex Str Exception"""

    pass
