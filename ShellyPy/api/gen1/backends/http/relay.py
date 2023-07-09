from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any

from .request import Request
from .....base import Relay as BaseRelay
from .....utils import property_fetcher

from .....exceptions import InvalidTimer

class Relay(BaseRelay):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ison = kwargs.get("ison")

    def toggle(self, timer: Optional[int] = None):
        parameters: Dict[str, Any] = {
            "turn": "toggle"
        }
        if timer is not None:
            parameters["timer"] = timer

        self._fetch(f"relay/{self.index}", parameters)

    def on(self, timer: Optional[int] = None):
        parameters: Dict[str, Any] = {
            "turn": "on"
        }
        if timer is not None:
            parameters["timer"] = timer

        self._fetch(f"relay/{self.index}", parameters)

    def off(self, timer: Optional[int] = None):
        parameters: Dict[str, Any] = {
            "turn": "off"
        }
        if timer is not None:
            parameters["timer"] = timer

        self._fetch(f"relay/{self.index}", parameters)

    def _fetch(self, *args, **kwargs):
        data = self._device._request.json_post(*args, *kwargs)

        self._ison = data["ison"]
        self._timer_started = datetime.fromtimestamp(data["timer_started"])
        self._timer_end = self._timer_started + timedelta(seconds=data["timer_duration"])

        return data

    def update(self) -> None:
        self._fetch(f"relay/{self.index}")
