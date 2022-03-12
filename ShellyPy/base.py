from sys import version_info

if version_info.major == 3:
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError

from requests.auth import HTTPBasicAuth

class ShellyBase:

    def __init__(self, ip, port = "80", *args, **kwargs):
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

        self.__credentials__ = HTTPBasicAuth(
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

    def update(self):
        raise NotImplementedError("Base Class")

    def post(self, page, values = None):
        raise NotImplementedError("Base Class")

    def status(self):
        raise NotImplementedError("Base Class")

    def settings(self, subpage = None):
        raise NotImplementedError("Base Class")

    def relay(self, index, *args, **kwargs):
        raise NotImplementedError("Base Class")

    def roller(self, index, *args, **kwargs):
        raise NotImplementedError("Base Class")

    def light(self, index, *args, **kwargs):
        raise NotImplementedError("Base Class")
        
    def emeter(self, index, *args, **kwargs):
        raise NotImplementedError("Base Class")
