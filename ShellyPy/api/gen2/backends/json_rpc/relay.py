from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any

from .request import Request
from .....base import Relay as BaseRelay
from .....utils import property_fetcher

from .....exceptions import InvalidTimer

class Relay(BaseRelay):

    def toggle(self, timer: Optional[int] = None):
        result = self._fetch("Switch.Toggle")
        try:
            self._ison = not result["was_on"]
        except KeyError:
            pass

    def on(self, timer: Optional[int] = None):
        self._fetch("Switch.Set", on=True)
        self._ison = True

    def off(self, timer: Optional[int] = None):
        self._fetch("Switch.Set", on=False)
        self._ison = False

    def _fetch(self, method, **kwargs):
        kwargs["id"] = self._index
        return self._device._request.post(method, kwargs)

    def update(self) -> None:
        result = self._fetch("Switch.GetStatus")
        self._ison = result.get("output")
