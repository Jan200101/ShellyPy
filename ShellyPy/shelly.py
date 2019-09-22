from typing import Union, List, Dict
from json.decoder import JSONDecodeError

from requests import post
from requests.auth import HTTPBasicAuth

from .error import *


def confirm_ip(ip: Union[str, List[str], List[int]]) -> bool:
    """
    @brief      Confirm IPv4 adress

    @param      ip    IP given as either a string or List containing strings or integers

    @return     returns True if ip is valid
    """

    if isinstance(ip, str):
        ip = ip.split(".")
        if len(ip) != 4:
            return False

    if isinstance(ip, list):
        for value in ip:
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    value = 256
            if value > 255 or value < 0:
                return False
        return True

    return False


class Shelly:

    def __init__(self, ip: Union[str, List[str], List[int]], port: Union[str, int] = "80", *, login: Dict[str, str]=None, **kwargs):
        """
        @param      ip     	the target IP of the shelly device. Can be a string, list of strings or list of integers
        @param      port        target port, may be useful for non Shelly devices that have the same HTTP Api
        @param      login  	dict of login credentials. Keys needed are "username" and "password"
        @param      timeout	specify the amount of time until requests are aborted.
        @param      debug	enable debug printing
        """

        # TODO add domain support

        self.__debugging__ = kwargs.get("debug", None)

        self.__PROTOCOL__ = "http"

        if not confirm_ip(ip):
            raise MalformedIP("IP is is malformed or not IPv4")

        if login is None:
            login = {}

        if isinstance(ip, list):
            self.__ip__ = ".".join([str(val) for val in ip])
        else:
            self.__ip__ = ip

        self.__port__ = port

        self.__timeout__ = kwargs.get("timeout", 5)

        self.__credentials__ = HTTPBasicAuth(
            login.get("username", ""), login.get("password", ""))

        self.update()

    def __repr__(self):
        return f"<{self.__name__} {self.__type__} ({self.__ip__})>"

    def __str__(self):
        return str(self.__name__)

    def update(self):
        """
        @brief update the Shelly attributes
        """
        status = self.settings()

        self.__type__ = status['device']['type']
        self.__name__ = status['device']['hostname']

        self.__relay__ = status.get("relays", [])
        self.__roller__ = status.get("rollers", [])
        self.__light__ = status.get("lights", [])

        # documentation for the Shelly Sense is very weird
        # FIXME
        self.__ir__ = status.get("ir", [])
        # There isn't even an example of the response for the RGBW
        # FIXME
        self.__color__ = status.get("color", [])

        self.__emeter__ = status.get("emeter", [])

    def post(self, page: str, values: Dict[str, Union[str, int]]=None) -> dict:
        """
        @brief      returns settings

        @param      page   page to be accesed. Use the Shelly HTTP API Reference to see whats possible

        @return     returns json response
        """

        url = f"{self.__PROTOCOL__}://{self.__ip__}:{self.__port__}/{page}?"

        if values:
            url += "&".join([f"{key}={value}" for key, value in values.items()])

        if self.__debugging__:
            print("Target Adress: {}\n"
                  "Authentication: {}\n"
                  "Timeout: {}"
                  "".format(url, any(self.__credentials__.username + self.__credentials__.password), self.__timeout__))

        response = post(url, auth=self.__credentials__,
                        timeout=self.__timeout__)

        if response.status_code == 401:
            raise BadLogin()
        elif response.status_code == 404:
            raise NotFound("Not Found")

        try:
            return response.json()
        except JSONDecodeError:
            raise BadResponse("Bad JSON")

    def settings(self, subpage: str = None) -> dict:
        """
        @brief      returns settings

        @param      page   page to be accesed. Use the Shelly HTTP API Reference to see whats possible

        @return     returns settings as a dict
        """

        page = "settings"
        if subpage:
            page += "/" + subpage

        return self.post(page)

    def relay(self, index: int, *, turn: bool = None, timer: float = None) -> dict:
        """
        @brief      Interacts with a relay at the given index

        @param      self   The object
        @param      index  index of the relay
        @param      turn   Will turn the relay on or off
        @param      timer  a one-shot flip-back timer in seconds
        """

        values = {}

        if turn is not None:
            if turn:
                values["turn"] = "on"
            else:
                values["turn"] = "off"

        if timer:
            values["timer"] = timer

        return self.post(f"relay/{index}", values)

    def roller(self, index: int, *, go: str = None,
               roller_pos: float = None, duration: float = None) -> dict:
        """
        @brief      Interacts with a roller at a given index

        @param      self        The object
        @param      index       index of the roller. When in doubt use 0
        @param      go          way of the roller to go. Accepted are "open", "close", "stop", "to_pos"
        @param      roller_pos  the wanted position in percent
        @param      duration    how long it will take to get to that position
        """

        def clamp_percentage(val: int):
            """
            clamp given percentage to a range from 0 to 100
            """
            if val > 100:
                val = 100
            elif val < 0:
                val = 0
            return val

        values = {}

        if go:
            values["go"] = go

        if roller_pos is not None:
            values["roller_pos"] = clamp_percentage(roller_pos)

        if duration is not None:
            values["duration"] = duration

        return self.post(f"roller/{index}", values)

    def light(self, index: int, *, mode: str = None, timer: int = None, turn: bool = None,
              red: int = None, green: int = None, blue: int = None, white: int = None,
              gain: int = None, temp: int = None, brightness: int = None) -> dict:

        def clamp(val: int) -> int:
            """clamp any number to 8 bit"""
            if val > 255:
                val = 255
            elif val < 0:
                val = 0

            return val

        values = {}

        if mode:
            values["mode"] = mode

        if timer is not None:
            values["timer"] = timer

        if turn is not None:
            if turn:
                values["turn"] = "on"
            else:
                values["turn"] = "off"

        if red is not None:
            values["red"] = clamp(red)

        if green is not None:
            values["green"] = clamp(green)

        if blue is not None:
            values["blue"] = clamp(blue)

        if white is not None:
            values["white"] = clamp(white)

        if gain is not None:
            values["gain"] = clamp(gain)

        if temp is not None:
            values["temp"] = temp

        if brightness is not None:
            values["brightness"] = brightness

        return self.post(f"light/{index}", values)

    def emeter(self, i: int, *args, **kwargs):
        #TODO
        return
