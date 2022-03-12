from sys import version_info

if version_info.major == 3:
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError


from requests import post

from .error import BadLogin, NotFound, BadResponse

from .base import ShellyBase

class ShellyGen1(ShellyBase):

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
        self.__generation__ = 1

    def update(self):
        """
        @brief update the Shelly attributes
        """
        status = self.settings()

        self.__type__ = status['device'].get("type", self.__type__)
        self.__name__ = status['device'].get("hostname", self.__name__)

        # Settings are already fetched to get device information might as well put the list of things the device has somewhere
        self.relays = status.get("relays", [])
        self.rollers = status.get("rollers", [])
        # RGBW reuses the same lights array
        self.lights = status.get("lights", [])

        self.irs = status.get("light_sensor", None)

        self.emeters = status.get("emeter", [])

    def post(self, page, values = None):
        """
        @brief      returns settings

        @param      page   page to be accesed. Use the Shelly HTTP API Reference to see whats possible

        @return     returns json response
        """

        url = "{}://{}:{}/{}?".format(self.__PROTOCOL__, self.__ip__, self.__port__, page)

        if values:
            url += "&".join(["{}={}".format(key, value) for key, value in values.items()])

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

    def status(self):
        """
        @brief      returns status response

        @return     status dict
        """
        return self.post("status")

    def settings(self, subpage = None):
        """
        @brief      returns settings

        @param      page   page to be accesed. Use the Shelly HTTP API Reference to see whats possible

        @return     returns settings as a dict
        """

        page = "settings"
        if subpage:
            page += "/" + subpage

        return self.post(page)

    def relay(self, index, *args, **kwargs):
        """
        @brief      Interacts with a relay at the given index

        @param      index  index of the relay
        @param      turn   Will turn the relay on or off
        @param      timer  a one-shot flip-back timer in seconds
        """

        values = {}

        turn = kwargs.get("turn", None)
        timer = kwargs.get("timer", None)

        if turn is not None:
            if turn:
                values["turn"] = "on"
            else:
                values["turn"] = "off"

        if timer:
            values["timer"] = timer

        return self.post("relay/{}".format(index), values)

    def roller(self, index, *args, **kwargs):
        """
        @brief      Interacts with a roller at a given index

        @param      self        The object
        @param      index       index of the roller. When in doubt use 0
        @param      go          way of the roller to go. Accepted are "open", "close", "stop", "to_pos"
        @param      roller_pos  the wanted position in percent
        @param      duration    how long it will take to get to that position
        """

        go = kwargs.get("go", None)
        roller_pos = kwargs.get("roller_pos", None)
        duration = kwargs.get("duration", None)

        values = {}

        if go:
            values["go"] = go

        if roller_pos is not None:
            values["roller_pos"] = self.__clamp_percentage__(roller_pos)

        if duration is not None:
            values["duration"] = duration

        return self.post("roller/{}".format(index), values)

    def light(self, index, *args, **kwargs):
        """
        @brief      Interacts with lights at a given index

        @param      mode        Accepts "white" and "color" as possible modes
        @param      index       index of the light. When in doubt use 0
        @param      timer       a one-shot flip-back timer in seconds
        @param      turn        Will turn the lights on or off
        @param      red         Red brightness, 0..255, only works if mode="color"
        @param      green       Green brightness, 0..255, only works if mode="color"
        @param      blue        Blue brightness, 0..255, only works if mode="color"
        @param      white       White brightness, 0..255, only works if mode="color"
        @param      gain        Gain for all channels, 0...100, only works if mode="color"
        @param      temp        Color temperature in K, 3000..6500, only works if mode="white"
        @param      brightness  Brightness, 0..100, only works if mode="white"
        """
        mode = kwargs.get("mode", None)
        timer = kwargs.get("timer", None)
        turn = kwargs.get("turn", None)
        red = kwargs.get("red", None)
        green = kwargs.get("green", None)
        blue = kwargs.get("blue", None)
        white = kwargs.get("white", None)
        gain = kwargs.get("gain", None)
        temp = kwargs.get("temp", None)
        brightness = kwargs.get("brightness", None)

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
            values["red"] = self.__clamp__(red)

        if green is not None:
            values["green"] = self.__clamp__(green)

        if blue is not None:
            values["blue"] = self.__clamp__(blue)

        if white is not None:
            values["white"] = self.__clamp__(white)

        if gain is not None:
            values["gain"] = self.__clamp_percentage__(gain)

        if temp is not None:
            values["temp"] = self.__clamp_kalvin__(temp)

        if brightness is not None:
            values["brightness"] = self.__clamp_percentage__(brightness)

        return self.post("light/{}".format(index), values)

    def emeter(self, index, *args, **kwargs):

        return self.post("emeter/{}".format(index))

# backwards compatibility with old code
Shelly = ShellyGen1