from typing import Any, Optional, Type
from json.decoder import JSONDecodeError

from requests import get
from requests import Response

from .base import ShellyBase
from .error import BadLogin, NotFound, BadResponse
from .gen1 import ShellyGen1
from .gen2 import ShellyGen2


class Shelly:

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

        self._instance: ShellyBase = self.__detect(ip, port)(ip=ip, port=port, timeout=timeout,
                                                             login=login, debug=debug, init=init)

    @staticmethod
    def __detect(ip: str, port: int, proto: str = 'http') -> Type[ShellyBase]:
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
        return self.__getattr__("__repr__")()

    def __str__(self) -> str:
        return self.__getattr__("__str__")()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._instance, name)
