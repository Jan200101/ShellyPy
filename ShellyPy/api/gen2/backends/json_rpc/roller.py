from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any

from .request import Request
from .....base import Roller as BaseRoller
from .....base.hints import percent
from .....utils import (
    clamp,
    property_fetcher,
)
from .....exceptions import InvalidTimer

class Roller(BaseRoller):

    def open(self):
        self._fetch("Cover.Open")
        self._state = "open"

    def close(self):
        self._fetch("Cover.Close")
        self._state = "close"

    def stop(self):
        self._fetch("Cover.Stop")
        self._state = "stop"

    def pos_setter(self, pos: percent):
        self._fetch("Cover.GoToPosition", pos=pos)

    def _fetch(self, method, **kwargs):
        kwargs["id"] = self._index
        try:
            return self._device._request.post(method, kwargs)
        finally:
            if method != "Cover.GetStatus":
                self.update()

    def update(self) -> None:
        result = self._fetch("Cover.GetStatus")
        self._state = result.get("state")
        self._last_direction = result.get("last_direction")
        self._pos = result.get("current_pos")

    def calibrate(self) -> None:
        self._fetch("Cover.Calibrate")
