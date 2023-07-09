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
        parameter = {
            "go": "open"
        }

        self._fetch(f"roller/{self.index}", parameter)

    def close(self):
        parameter = {
            "go": "close"
        }

        self._fetch(f"roller/{self.index}", parameter)

    def stop(self):
        parameter = {
            "go": "stop"
        }

        self._fetch(f"roller/{self.index}", parameter)

    def pos_setter(self, pos: percent):
        parameter = {
            "go": "to_pos",
            "roller_pos": pos
        }

        self._fetch(f"roller/{self.index}", parameter)

    def _fetch(self, *args, **kwargs):
        data = self._device._request.json_post(*args, *kwargs)

        self._state = data["state"]
        self._power = data["power"]
        self._safety_switch = data["safety_switch"]
        self._stop_reason = data["stop_reason"]
        self._last_direction = data["last_direction"]
        self._pos = data["current_pos"]

        self._calibrating = data["calibrating"]
        self._positioning = data["positioning"]

        return data

    def update(self) -> None:
        self._fetch(f"roller/{self.index}")

    def calibrate(self) -> None:
        self._fetch(f"roller/{self.index}/calibrate")
