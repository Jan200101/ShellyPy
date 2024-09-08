from typing import Optional
from json.decoder import JSONDecodeError

from requests import post
from requests.auth import HTTPDigestAuth

from .error import BadLogin, NotFound, BadResponse
from .base import ShellyBase


class ShellyGen2(ShellyBase):

    def __init__(self, ip: str, port: int = 80, *args, **kwargs) -> None:
        """
        @param      ip      the target IP of the shelly device. Can be a string, list of strings or list of integers
        @param      port        target port, may be useful for non Shelly devices that have the same HTTP Api
        @param      login   dict of login credentials. Keys needed are "username" and "password"
        @param      timeout specify the amount of time until requests are aborted.
        @param      debug   enable debug printing
        @param      init    calls the update method on init
        """

        super().__init__(ip, port, *args, **kwargs)
        self.payload_id = 1
        self.__generation__ = 2

    def update(self) -> None:
        status = self.settings()

        self._name = status["device"].get("name", self._name)
        self._type = status["device"].get("mac", self._type)

    def post(self, page, values = None):
        url = f"{self._proto}://{self._hostname}:{self._port}/rpc"

        # increment payload id globally
        self.payload_id += 1
        # but keep a local copy around so we face no race conditions
        payload_id = self.payload_id

        payload = {
            "jsonrpc": "2.0",
            "id": payload_id,
            "method": page,
        }

        if values:
            payload["params"] = values

        credentials = None
        try:
            credentials = HTTPDigestAuth('admin', self._credentials[1])
        except IndexError:
            pass

        response = post(url, auth=credentials,
                        json=payload,
                        timeout=self._timeout)

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
                raise BadResponse(f"{error_code}: {error_message}")

        if response_data["id"] != payload_id:
            raise BadResponse("invalid payload id was returned")

        return response_data.get("result", {})

    def status(self):
        return self.post("Sys.GetStatus")

    def settings(self, subpage = None):
        return self.post("Sys.GetConfig")

    def meter(self, index):
        raise NotImplementedError("Unavailable")

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
            values["pos"] = self._clamp_percentage(roller_pos)

        if duration is not None:
            values["duration"] = duration

        return self.post(method, values)

    def light(self, index, *args, **kwargs):
        raise NotImplementedError("Unavailable")
        
    def emeter(self, index, *args, **kwargs):
        raise NotImplementedError("Unavailable")
