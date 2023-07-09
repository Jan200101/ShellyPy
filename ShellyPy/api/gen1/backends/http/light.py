from datetime import datetime, timedelta
from typing import Optional, Tuple, Union, Dict, Any

from .request import Request
from .....base import Light as BaseLight
from .....base.hints import (
    rgbw_mode, byte, percent,
    temperaur, transition
)
from .....utils import (
    clamp, clamp_percent, clamp_byte,
    clamp_temp, property_fetcher,
)
from .....exceptions import InvalidTimer

class Light(BaseLight):

    def toggle(self, timer: Optional[int] = None):
        parameters: Dict[str, Any] = {
            "turn": "toggle"
        }
        if timer is not None:
            parameters["timer"] = timer

        self._fetch(f"light/{self.index}", parameters)

    def on(self, timer: Optional[int] = None):
        parameters: Dict[str, Any] = {
            "turn": "on"
        }
        if timer is not None:
            parameters["timer"] = timer

        self._fetch(f"light/{self.index}", parameters)

    def off(self, timer: Optional[int] = None):
        parameters: Dict[str, Any] = {
            "turn": "off"
        }
        if timer is not None:
            parameters["timer"] = timer

        self._fetch(f"light/{self.index}", parameters)

    def mode_setter(self, mode: rgbw_mode):
        self._fetch(f"light/{self.index}", {"mode": mode})

    def red_setter(self, val: byte):
        self._fetch(f"light/{self.index}", {"red": val})

    def green_setter(self, val: byte):
        self._fetch(f"light/{self.index}", {"green": val})

    def blue_setter(self, val: byte):
        self._fetch(f"light/{self.index}", {"blue": val})

    def white_setter(self, val: byte):
        self._fetch(f"light/{self.index}", {"white": val})

    def rgb_setter(self, rgb: Tuple[byte, byte, byte]):
        self._fetch(f"light/{self.index}", {
            "red": rgb[0],
            "green": rgb[1],
            "blue": rgb[2]
        })

    def rgbw_setter(self, rgbw: Tuple[byte, byte, byte, byte]):
        self._fetch(f"light/{self.index}", {
            "red": rgbw[0],
            "green": rgbw[1],
            "blue": rgbw[2],
            "white": rgbw[3],
        })

    def brightness_setter(self, val: percent):
        self._fetch(f"light/{self.index}", {"brightness": val})

    def _fetch(self, *args, **kwargs):
        data = self._device._request.json_post(*args, *kwargs)

        self._ison = data.get("ison")

        started = data.get("timer_started")
        duration = data.get("timer_duration")
        if started and duration:
            self._timer_start = datetime.utcfromtimestamp(started)
            self._timer_end = self._timer_start + timedelta(seconds=duration)

        self._mode = data.get("mode")
        self._red = data.get("red")
        self._green = data.get("green")
        self._blue = data.get("blue")
        self._white = data.get("white")
        self._gain = data.get("gain")
        self._temp = data.get("temp")
        self._brightness = data.get("brightness")

        self._effect = data.get("effect")
        self._transition = data.get("transition")

        return data

    def update(self) -> None:
        self._fetch(f"light/{self.index}")
