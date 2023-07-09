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
        self._fetch("Light.Toggle")
        self.update()

    def on(self, timer: Optional[int] = None):
        params: Dict[str, Any] = {"on": True}
        if timer is not NOne:
            params["toggle_after"] = timer
        self._fetch("Light.Set", **params)
        self._ison = True

    def off(self, timer: Optional[int] = None):
        params: Dict[str, Any] = {"on": False}
        if timer is not None:
            params["toggle_after"] = timer
        self._fetch("Light.Set", **params)
        self._ison = False

    def mode_setter(self, mode: rgbw_mode):
        raise UnimplementedMethod("TODO Gen2 Light::mode_setter()")

    def red_setter(self, val: byte):
        raise UnimplementedMethod("TODO Gen2 Light::red_setter()")

    def green_setter(self, val: byte):
        raise UnimplementedMethod("TODO Gen2 Light::green_setter()")

    def blue_setter(self, val: byte):
        raise UnimplementedMethod("TODO Gen2 Light::blue_setter()")

    def white_setter(self, val: byte):
        raise UnimplementedMethod("TODO Gen2 Light::white_setter()")

    def rgb_setter(self, rgb: Tuple[byte, byte, byte]):
        raise UnimplementedMethod("TODO Gen2 Light::rgb_setter()")

    def rgbw_setter(self, rgbw: Tuple[byte, byte, byte, byte]):
        raise UnimplementedMethod("TODO Gen2 Light::rgbw_setter()")

    def brightness_setter(self, val: percent):
        self._fetch("Light.Set", brightness=val)

    def _fetch(self, method, **kwargs):
        kwargs["id"] = self._index
        return self._device._request.post(method, kwargs)

    def update(self) -> None:
        result = self._fetch("Light.GetStatus")
        self._ison = result.get("output")
        self._brightness = result.get("brightness")

        started = data.get("timer_started")
        duration = data.get("timer_duration")
        if started and duration:
            self._timer_start = datetime.utcfromtimestamp(started)
            self._timer_end = self._timer_start + timedelta(seconds=duration)