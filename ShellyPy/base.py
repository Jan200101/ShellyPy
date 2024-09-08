from typing import Optional
from abc import abstractmethod


class ShellyBase:

    def __init__(self, ip: str, port: int = 80, *args, **kwargs) -> None:
        """
        @param      ip      the target IP of the shelly device. Can be a string, list of strings or list of integers
        @param      port    target port, may be useful for non Shelly devices that have the same HTTP Api
        @param      login   dict of login credentials. Keys needed are "username" and "password"
        @param      timeout specify the amount of time until requests are aborted.
        @param      debug   enable debug printing
        @param      init    calls the update method on init
        """

        self._name = "Unknown"
        self._type = "Unknown"
        self._generation = 0

        self._debugging = kwargs.get("debug", None)

        self._proto = "http"

        login = kwargs.get("login", {})

        # hostname would be more fitting,
        # but backwards compatibility
        self._hostname = ip

        self._port = port

        self._timeout = kwargs.get("timeout", 5)

        self._credentials = (
            login.get("username", ""), login.get("password", "")
        )

        if kwargs.get("init"):
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
    def post(self, page, values = None):
        ...

    @abstractmethod
    def status(self):
        ...

    @abstractmethod
    def settings(self, subpage = None):
        ...

    @abstractmethod
    def meter(self, index):
        ...

    @abstractmethod
    def relay(self, index, *args, **kwargs):
        ...

    @abstractmethod
    def roller(self, index, *args, **kwargs):
        ...

    @abstractmethod
    def light(self, index, *args, **kwargs):
        ...

    @abstractmethod
    def emeter(self, index, *args, **kwargs):
        ...
