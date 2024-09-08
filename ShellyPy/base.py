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

        self.__name__ = "Unknown"
        self.__type__ = "Unknown"
        self.__generation__ = 0

        self.__debugging__ = kwargs.get("debug", None)

        self.__PROTOCOL__ = "http"

        login = kwargs.get("login", {})

        # hostname would be more fitting,
        # but backwards compatibility
        self.__ip__ = ip

        self.__port__ = port

        self.__timeout__ = kwargs.get("timeout", 5)

        self.__credentials__ = (
            login.get("username", ""), login.get("password", "")
        )

        if kwargs.get("init"):
            self.update()

    def __repr__(self):
        return "<{} {} Gen {} ({})>".format(self.__name__, self.__type__, self.__generation__, self.__ip__)

    def __str__(self):
        return str(self.__name__)

    @staticmethod
    def __clamp__(val):
        """clamp any number to 8 bit"""
        if val > 255:
            val = 255
        elif val < 0:
            val = 0

        return val

    @staticmethod
    def __clamp_percentage__(val):
        """
        clamp given percentage to a range from 0 to 100
        """
        if val > 100:
            val = 100
        elif val < 0:
            val = 0
        return val

    @staticmethod
    def __clamp_kalvin__(val):
        """
        clamp given kalvin values for a range from 3000..6500
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
