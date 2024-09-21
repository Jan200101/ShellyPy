from typing import Any, Optional, Type
from json.decoder import JSONDecodeError

from requests import get
from requests import Response

from .base import _ShellyBase
from .error import BadLogin, NotFound, BadResponse
from .gen1 import ShellyGen1
from .gen2 import ShellyGen2


class Shelly(_ShellyBase):
    """
    General wrapper class for shelly devices of all generations automatically using methods of proper one generation
    """
    def __init__(self, ip: str, port: int = 80, timeout: int = 5,
                 login: Optional[dict[str, str]] = None, debug: bool = False, init: bool = False) -> None:

        super().__init__(ip=ip, port=port, timeout=timeout, login=login, debug=debug, init=init)
        self._instance: _ShellyBase = self.__detect(ip, port)(ip=ip, port=port, timeout=timeout,
                                                              login=login, debug=debug, init=init)

    @staticmethod
    def __detect(ip: str, port: int, proto: str = 'http') -> Type[_ShellyBase]:
        url: str = f"{proto}://{ip}:{port}/shelly"

        response: Response = get(url, timeout=5)

        if response.status_code == 401:
            raise BadLogin()
        elif response.status_code == 404:
            raise NotFound("Not Found")

        try:
            response_data: dict[str, Any] = response.json()
        except JSONDecodeError:
            raise BadResponse("Bad JSON")

        gen: int = response_data.get("gen", 1)

        if gen == 1:
            return ShellyGen1
        elif gen == 2:
            return ShellyGen2
        else:
            raise ValueError(f"Generation {gen} not supported")

    def __repr__(self) -> str:
        return self._instance.__repr__()

    def __str__(self) -> str:
        return self._instance.__str__()

    def __getattr__(self, name: str) -> Any:
        return self._instance.__getattribute__(name)

    def update(self) -> None:
        self._instance.update()

    def post(self, page: str, values: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        return self._instance.post(page, values)

    def status(self) -> dict[str, Any]:
        return self._instance.status()

    def settings(self, subpage: Optional[str] = None) -> dict[str, Any]:
        return self._instance.settings(subpage)

    def meter(self, index: int) -> dict[str, Any]:
        return self._instance.meter(index)

    def relay(self, index: int, timer: float = 0.0, turn: Optional[bool] = None) -> dict[str, Any]:
        return self._instance.relay(index, timer, turn)

    def roller(self, index: int, go: Optional[str] = None,
               roller_pos: Optional[int] = None, duration: Optional[int] = None) -> dict[str, Any]:
        return self._instance.roller(index, go, roller_pos, duration)

    def light(self, index: int, mode: Optional[str] = None, timer: Optional[int] = None, turn: Optional[bool] = None,
              red: Optional[int] = None, green: Optional[int] = None, blue: Optional[int] = None,
              white: Optional[int] = None, gain: Optional[int] = None, temp: Optional[int] = None,
              brightness: Optional[int] = None) -> dict[str, Any]:
        return self._instance.light(index, mode, timer, turn, red, green, blue, white, gain, temp, brightness)

    def emeter(self, index: int) -> dict[str, Any]:
        return self._instance.emeter(index)
