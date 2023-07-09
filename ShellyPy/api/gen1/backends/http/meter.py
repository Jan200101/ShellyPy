from datetime import datetime
from typing import List

from .request import Request
from .....base import Meter as BaseMeter

from .....exceptions import InvalidTimer

class Meter(BaseMeter):

    def _fetch(self, *args, **kwargs):
        data = self._device._request.json_post(*args, *kwargs)

        self._power = data["power"]
        self._is_valid = data["is_valid"]
        self._timestamp = datetime.fromtimestamp(data["timestamp"])
        self._counters = data["counters"]
        self._total = data["total"]

        return data

    def update(self) -> None:
        self._fetch(f"meter/{self.index}")
