from typing import Any, Optional
from abc import abstractmethod


class ShellyBase:

    def __init__(self, ip: str, port: int = 80, timeout: int = 5,
                 login: Optional[dict[str, str]] = None, debug: bool = False, init: bool = False) -> None:
        """
        @param      ip      the target IP of the shelly device. Can be a string, list of strings or list of integers
        @param      port    target port, may be useful for non Shelly devices that have the same HTTP Api
        @param      login   dict of login credentials. Keys needed are "username" and "password"
        @param      timeout specify the amount of time until requests are aborted.
        @param      debug   enable debug printing
        @param      init    calls the update method on init
        """

        self._name: str = "Unknown"
        self._type: str = "Unknown"
        self._generation: int = 0

        self._proto: str = "http"
        self._hostname: str = ip  # hostname would be more fitting, but backwards compatibility
        self._port: int = port
        self._timeout: int = timeout
        self._credentials: tuple[str, str] = (login.get("username", ""),
                                              login.get("password", "")) if login is not None else ("", "")

        self._debugging: bool = debug
        if init:
            self.update()

    def __repr__(self) -> str:
        return f"<{self._name} {self._type} Gen {self._generation} ({self._hostname})>"

    def __str__(self) -> str:
        return self._name

    @staticmethod
    def _clamp(val: int) -> int:
        """clamp any number to 8 bit"""
        if val > 255:
            val = 255
        elif val < 0:
            val = 0

        return val

    @staticmethod
    def _clamp_percentage(val: int) -> int:
        """
        clamp given percentage to a range from 0 to 100
        """
        if val > 100:
            val = 100
        elif val < 0:
            val = 0
        return val

    @staticmethod
    def _clamp_kelvin(val: int) -> int:
        """
        clamp given kelvin values for a range from 3000..6500
        """
        if val > 6500:
            val = 6500
        elif val < 3000:
            val = 3000
        return val

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def post(self, page: str, values: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        ...

    @abstractmethod
    def status(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def settings(self, subpage: Optional[str] = None) -> dict[str, Any]:
        ...

    @abstractmethod
    def meter(self, index: int) -> dict[str, Any]:
        ...

    @abstractmethod
    def relay(self, index: int, timer: float = 0.0, turn: Optional[bool] = None) -> dict[str, Any]:
        ...

    @abstractmethod
    def roller(self, index: int, go: Optional[str] = None,
               roller_pos: Optional[int] = None, duration: Optional[int] = None) -> dict[str, Any]:
        ...

    @abstractmethod
    def light(self, index: int, mode: Optional[str] = None, timer: Optional[int] = None, turn: Optional[bool] = None,
              red: Optional[int] = None, green: Optional[int] = None, blue: Optional[int] = None,
              white: Optional[int] = None, gain: Optional[int] = None, temp: Optional[int] = None,
              brightness: Optional[int] = None) -> dict[str, Any]:
        ...

    @abstractmethod
    def emeter(self, index: int) -> dict[str, Any]:
        ...
