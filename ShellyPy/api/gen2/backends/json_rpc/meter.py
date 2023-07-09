from datetime import datetime
from typing import List

from .request import Request
from .....base import Meter as BaseMeter

from .....exceptions import InvalidTimer

class Meter(BaseMeter):

    def _fetch(self, method, **kwargs):
        kwargs["id"] = self._index
        result = self._device._request.post(method, kwargs)

        self._power = result.get("voltage", 0)
        self._is_valid = True
        self._timestamp = 0
        self._counters = 0
        self._total = 0

        return result

    def update(self) -> None:
        self._fetch("Voltmeter.GetStatus")
