from ..exceptions.backend import InvalidBackend
from ..exceptions.request import UnauthorizedException, InvalidRequestException

from . import gen1
from . import gen2

from typing import Optional
import json
from urllib.request import urlopen

class Device:

    def __init__(self, hostname: str, port: Optional[int] = None, *args, **kwargs):
        self._instance = self.__detect__(hostname, port)(hostname, port, *args, **kwargs)

    @staticmethod
    def __detect__(ip, port):
        url = f"http://{ip}:{port or 80}/shelly"

        resp = urlopen(url, timeout=5)

        status_code = resp.getcode()

        if status_code == 401:
            raise UnauthorizedException()
        elif status_code == 404:
            raise InvalidRequestException("Endpoint Not Found")

        try:
            response_data = json.loads(resp.read().decode())
        except JSONDecodeError:
            raise InvalidRequestException("Received Invalid Response")

        gen = response_data.get("gen", 1)
        
        if gen == 1:
            return gen1.Device
        elif gen == 2:
            return gen2.Device
        else:
            raise InvalidBackend(f"Generation {gen} not supported")

    def __repr__(self):
        return self.__getattr__("__repr__")()

    def __str__(self):
        return self.__getattr__("__str__")()

    def __getattr__(self, name):
        return getattr(self._instance, name)

    @classmethod
    def connect(cls, hostname: str, port: Optional[int] = None, *args, **kwargs):
        instance = cls.__detect__(hostname, port)(hostname, port, *args, **kwargs)
        return instance
