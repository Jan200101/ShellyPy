from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Union

from ..utils import property_fetcher

class Relay(metaclass=ABCMeta):

    def __init__(self, device, index, *args, **kwargs):
        self._device = device
        self._index = index

        self._ison = None
        self._timer_start = None
        self._timer_end = None

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}{self.index}(on={self.ison})"

    @abstractmethod
    def toggle(self, timer: Optional[int] = None):
        pass

    @abstractmethod
    def on(self, timer: Optional[int] = None):
        pass

    @abstractmethod
    def off(self, timer: Optional[int] = None):
        pass

    def turn(self, value: Union[str, bool], timer: Optional[int] = None):
        
        value_method = {
            "toggle": self.toggle,
            "on": self.on,
            "off": self.off,
            True: self.on,
            False: self.off
        }

        return value_method[value](timer)

    @property
    def index(self) -> int:
        return self._index

    @property
    @property_fetcher()
    def ison(self) -> bool:
        return bool(self._ison)

    @property
    def has_timer(self) -> bool:
        """
        return true when the timer is primed and has not happened yet
        """
        start = self._timer_start
        end = self._timer_end
        if not start or not end:
            return False

        date_now = datetime.now()
        return end > date_now and start < date_now


    @property
    @property_fetcher()
    def timer_started(self) -> Optional[datetime]:
        if self.has_timer:
            return self._timer_start
        return None

    @property
    def timer_duration(self) -> Optional[timedelta]:
        # fetch the start before to populate the implementation values
        if not self.has_timer:
            return None

        start = self.timer_started
        end = self._timer_end

        return end - start

    @abstractmethod
    def update(self) -> None:
        pass
