from typing import Any, Optional
from abc import abstractmethod


class _ShellyBase:
    """
    Base or parent class for Shelly device implementation
    """

    def __init__(self, ip: str, port: int = 80, timeout: int = 5,
                 login: Optional[dict[str, str]] = None, debug: bool = False, init: bool = False) -> None:
        """
        @param      ip      the target IP of the shelly device. Can be a string, list of strings or list of integers
        @param      port        target port, may be useful for non Shelly devices that have the same HTTP Api
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
        """
        @brief  clamp any number to 8 bit
        @param      val     any number to clamp
        @return     clamped number
        """
        if val > 255:
            val = 255
        elif val < 0:
            val = 0

        return val

    @staticmethod
    def _clamp_percentage(val: int) -> int:
        """
        clamp given percentage to a range from 0 to 100
        @param      val     percentage to clamp
        @return     clamped percentage
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
        @param      val     kelvin values to clamp
        @return     clamped kelvin value
        """
        if val > 6500:
            val = 6500
        elif val < 3000:
            val = 3000
        return val

    @abstractmethod
    def update(self) -> None:
        """
        @brief update the Shelly attributes
        """
        ...

    @abstractmethod
    def post(self, page: str, values: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        @brief      returns settings of shelly device

        @param      page    the page to be accessed. Use the Shelly HTTP API Reference to see what's possible
        @param      values  dict of values to send in the body of the request
        @return     returns json response
        """
        ...

    @abstractmethod
    def status(self) -> dict[str, Any]:
        """
        @brief      returns status response of shelly device

        @return     status dict
        """
        ...

    @abstractmethod
    def settings(self, subpage: Optional[str] = None) -> dict[str, Any]:
        """
        @brief      returns settings of shelly device or a specific subset

        @param      subpage page to be accessed. Use the Shelly HTTP API Reference to see what's possible
        @return     returns settings as a dict
        """
        ...

    @abstractmethod
    def meter(self, index: int) -> dict[str, Any]:
        """
        @brief      Get meter information from a relay at the given index

        @param      index  the index of the relay
        @return     returns attributes of meter: power, overpower, is_valid, timestamp, counters, total
        """
        ...

    @abstractmethod
    def relay(self, index: int, timer: float = 0.0, turn: Optional[bool] = None) -> dict[str, Any]:
        """
        @brief      Interacts with a relay at the given index

        @param      index  the index of the relay
        @param      turn   Will turn the relay on or off
        @param      timer  a one-shot flip-back timer in seconds
        @return     returns attributes dict of relay: was_on
        """
        ...

    @abstractmethod
    def roller(self, index: int, go: Optional[str] = None,
               roller_pos: Optional[int] = None, duration: Optional[int] = None) -> dict[str, Any]:
        """
        @brief      Interacts with a roller at a given index

        @param      self        the object
        @param      index       the index of the roller. When in doubt use 0
        @param      go          way of the roller to go. Accepted are "open", "close", "stop", "to_pos"
        @param      roller_pos  the wanted position in percent
        @param      duration    how long it will take to get to that position
        @return     returns attributes dict of roller
        """
        ...

    @abstractmethod
    def light(self, index: int, mode: Optional[str] = None, timer: Optional[int] = None, turn: Optional[bool] = None,
              red: Optional[int] = None, green: Optional[int] = None, blue: Optional[int] = None,
              white: Optional[int] = None, gain: Optional[int] = None, temp: Optional[int] = None,
              brightness: Optional[int] = None) -> dict[str, Any]:
        """
        @brief      Interacts with lights at a given index

        @param      index       the index of the light. When in doubt use 0
        @param      mode        accepts "white" and "color" as possible modes
        @param      timer       a one-shot flip-back timer in seconds
        @param      turn        will turn the lights on or off
        @param      red         brightness of red, 0..255, only works if mode="color"
        @param      green       brightness of green, 0..255, only works if mode="color"
        @param      blue        brightness of blue, 0..255, only works if mode="color"
        @param      white       brightness of white, 0..255, only works if mode="color"
        @param      gain        the gain for all channels, 0...100, only works if mode="color"
        @param      temp        color temperature in K, 3000..6500, only works if mode="white"
        @param      brightness  the brightness, 0..100, only works if mode="white"
        @return     returns json response as dict
        """
        ...

    @abstractmethod
    def emeter(self, index: int) -> dict[str, Any]:
        """
        @brief      Get emeter information

        @param      index  the index of the emeter. When in doubt use 0
        @return     returns attributes dict of emeter
        """
        ...
