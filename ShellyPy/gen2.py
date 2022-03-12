from sys import version_info

if version_info.major == 3:
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError

from requests import post

from .error import BadLogin, NotFound, BadResponse

from .base import ShellyBase

class ShellyGen2(ShellyBase):

    def __init__(self, ip, port = "80", *args, **kwargs):
        """
        @param      ip      the target IP of the shelly device. Can be a string, list of strings or list of integers
        @param      port        target port, may be useful for non Shelly devices that have the same HTTP Api
        @param      login   dict of login credentials. Keys needed are "username" and "password"
        @param      timeout specify the amount of time until requests are aborted.
        @param      debug   enable debug printing
        @param      init    calls the update method on init
        """

        super().__init__(ip, port, *args, **kwargs)
        self.__generation__ = 2

    def update(self):
        status = self.settings()

        self.__name__ = status["device"].get("name", self.__name__)
        self.__type__ = status["device"].get("mac", self.__type__)

    def post(self, page, values = None):
        url = "{}://{}:{}/rpc".format(self.__PROTOCOL__, self.__ip__, self.__port__)

        payload = {
            "id": 1,
            "method": page,
        }

        if values:
            payload["params"] = values

        response = post(url, auth=self.__credentials__,
                        json=payload,
                        timeout=self.__timeout__)

        if response.status_code == 401:
            raise BadLogin()
        elif response.status_code == 404:
            raise NotFound("Not Found")

        try:
            response_data = response.json()
        except JSONDecodeError:
            raise BadResponse("Bad JSON")

        if "error" in response_data:
            error_code = response_data["error"].get("code", None)
            error_message = response_data["error"].get("message", "")

            if error_code == 401:
                raise BadLogin(error_message)
            elif error_code == 404:
                raise NotFound(error_message)
            else:
                raise BadResponse("{}: {}".format(error_code, error_message))

        return response_data.get("result", {})

    def status(self):
        return self.post("Sys.GetStatus")

    def settings(self, subpage = None):
        return self.post("Sys.GetConfig")

    def relay(self, index, *args, **kwargs):

        values = {
            "id": index
        }

        turn = kwargs.get("turn", None)
        timer = kwargs.get("timer", None)

        if turn is not None:
            method = "Switch.Set"

            if turn:
                values["on"] = True
            else:
                values["on"] = False

            if timer:
                values["toggle_after"] = timer
        else:
            method = "Switch.GetStatus"

        return self.post(method, values)

    def roller(self, index, *args, **kwargs):

        go = kwargs.get("go", None)
        roller_pos = kwargs.get("roller_pos", None)
        duration = kwargs.get("duration", None)

        values = {
            "id": index
        }

        if go:
            if go == "open":
                method = "Cover.Open"
            elif go == "close":
                method = "Cover.Close"
            elif go == "stop":
                method = "Cover.Stop"
            else:
                raise ValueError("Method is not open, close or stop")

        if roller_pos is not None:
            method = "Cover.GoToPosition"
            values["pos"] = self.__clamp_percentage__(roller_pos)

        if duration is not None:
            values["duration"] = duration

        return self.post(method, values)

    def light(self, index, *args, **kwargs):
        raise NotImplementedError("Unavailable")
        
    def emeter(self, index, *args, **kwargs):
        raise NotImplementedError("Unavailable")