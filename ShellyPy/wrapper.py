from sys import version_info

if version_info.major == 3:
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError

from requests import post

from .error import BadLogin, NotFound, BadResponse

from .gen1 import ShellyGen1
from .gen2 import ShellyGen2

class Shelly():

    def __init__(self, ip, port = "80", *args, **kwargs):
        """
        @param      ip      the target IP of the shelly device. Can be a string, list of strings or list of integers
        @param      port        target port, may be useful for non Shelly devices that have the same HTTP Api
        @param      login   dict of login credentials. Keys needed are "username" and "password"
        @param      timeout specify the amount of time until requests are aborted.
        @param      debug   enable debug printing
        @param      init    calls the update method on init
        """

        self._instance = self.__detect__(ip, port)(ip, port, *args, **kwargs)

    def __detect__(self, ip, port):
        url = "{}://{}:{}/shelly".format("http", ip, port)

        response = post(url, timeout=5)

        if response.status_code == 401:
            raise BadLogin()
        elif response.status_code == 404:
            raise NotFound("Not Found")

        try:
            response_data = response.json()
        except JSONDecodeError:
            raise BadResponse("Bad JSON")

        gen = response_data.get("gen", 1)
        
        if gen == 1:
            return ShellyGen1
        elif gen == 2:
            return ShellyGen2
        else:
            raise ValueError("Generation {} not supported".format(gen))

    def __repr__(self):
        return self.__getattr__("__repr__")()

    def __str__(self):
        return self.__getattr__("__str__")()

    def __getattr__(self, name):
        return getattr(self._instance, name)
