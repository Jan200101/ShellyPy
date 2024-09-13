from typing import Any, Optional
from json.decoder import JSONDecodeError

from requests import post
from requests import Response
from requests.auth import HTTPBasicAuth

from .error import BadLogin, NotFound, BadResponse
from .base import _ShellyBase


class ShellyGen1(_ShellyBase):
    """
    Implements a general Class for interaction with Shelly devices of generation 1
    """

    def __init__(self, ip: str, port: int = 80, timeout: int = 5,
                 login: Optional[dict[str, str]] = None, debug: bool = False, init: bool = False) -> None:

        super().__init__(ip=ip, port=port, timeout=timeout, login=login, debug=debug, init=init)
        self._generation: int = 1

        self.relays: list[dict[str, Any]] = []
        self.rollers: list[dict[str, Any]] = []
        self.lights: list[dict[str, Any]] = []

        self.ir_sense: str = "Unknown"

        self.emeters: list[dict[str, Any]] = []
        self.meters: list[dict[str, Any]] = []

    def update(self) -> None:

        status: dict[str, Any] = self.settings()

        self._name: str = status['device'].get("hostname", self._name)
        self._type: str = status['device'].get("type", self._type)

        # Settings are already fetched to get device information might as well put the list of things the device has somewhere
        self.relays = status.get("relays", [])
        self.rollers = status.get("rollers", [])
        # RGBW reuses the same lights array
        self.lights = status.get("lights", [])

        self.ir_sense = status.get("light_sensor", "Unknown")

        self.emeters = status.get("emeter", [])

        self.meters = []
        meter_index = 0
        # Meters are not returned as part of the settings
        while True:
            try:
                # Request meter information
                self.meters.append(self.meter(meter_index))
                meter_index += 1
            except (BadLogin, NotFound, BadResponse):
                break

    def post(self, page: str, values: Optional[dict[str, Any]] = None) -> dict[str, Any]:

        url: str = f"{self._proto}://{self._hostname}:{self._port}/{page}?"

        if values:
            url += "&".join([f"{key}={value}" for key, value in values.items()])

        if self._debugging:
            print(f"Target Address: {url}\nAuthentication: {any(self._credentials)}\nTimeout: {self._timeout}")

        credentials = HTTPBasicAuth(*self._credentials)

        response: Response = post(url, auth=credentials, timeout=self._timeout)

        if response.status_code == 401:
            raise BadLogin()
        elif response.status_code == 404:
            raise NotFound("Not Found")

        try:
            return response.json()
        except JSONDecodeError:
            raise BadResponse("Bad JSON")

    def status(self) -> dict[str, Any]:
        return self.post("status")

    def settings(self, subpage: Optional[str] = None) -> dict[str, Any]:

        page: str = "settings"
        if subpage:
            page += f"/{subpage}"

        return self.post(page)

    def meter(self, index: int) -> dict[str, Any]:
        return self.post(f"meter/{index}")

    def relay(self, index: int, timer: float = 0.0, turn: Optional[bool] = None)  -> dict[str, Any]:

        values: dict[str, Any] = {}

        if turn is not None:
            if turn:
                values["turn"] = "on"
            else:
                values["turn"] = "off"

        if timer > 0.0:
            values["timer"] = timer

        return self.post(f"relay/{index}", values)

    def roller(self, index: int, go: Optional[str] = None,
               roller_pos: Optional[int] = None, duration: Optional[int] = None) -> dict[str, Any]:

        values: dict[str, Any] = {}

        if go is not None:
            values["go"] = go

        if roller_pos is not None:
            values["roller_pos"] = self._clamp_percentage(roller_pos)

        if duration is not None:
            values["duration"] = duration

        return self.post(f"roller/{index}", values)

    def light(self, index: int, mode: Optional[str] = None, timer: Optional[int] = None, turn: Optional[bool] = None,
              red: Optional[int] = None, green: Optional[int] = None, blue: Optional[int] = None,
              white: Optional[int] = None, gain: Optional[int] =  None, temp: Optional[int] = None,
              brightness: Optional[int] = None) -> dict[str, Any]:

        values: dict[str, Any] = {}

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
            values["red"] = self._clamp(red)

        if green is not None:
            values["green"] = self._clamp(green)

        if blue is not None:
            values["blue"] = self._clamp(blue)

        if white is not None:
            values["white"] = self._clamp(white)

        if gain is not None:
            values["gain"] = self._clamp_percentage(gain)

        if temp is not None:
            values["temp"] = self._clamp_kelvin(temp)

        if brightness is not None:
            values["brightness"] = self._clamp_percentage(brightness)

        return self.post(f"light/{index}", values)

    def emeter(self, index: int) -> dict[str, Any]:
        return self.post(f"emeter/{index}")

# backwards compatibility with old code
Shelly = ShellyGen1
