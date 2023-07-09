from abc import ABCMeta, abstractmethod
from typing import Dict, List

from ..utils import property_fetcher

class Settings(metaclass=ABCMeta):
    _max_power: int
    _actions: Dict # TODO
    _mode: str
    _led_status: bool

    def __init__(self, device, *args, **kwargs):
        self._device = device

    @property
    @property_fetcher()
    def max_power(self):
        return self._max_power

    @max_power.setter
    def max_power(self, *args, **kwargs):
        return self.max_power_setter(*args, **kwargs)

    @abstractmethod
    def max_power_setter(self, power):
        pass

    @property
    @property_fetcher()
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, *args, **kwargs):
        return self.mode_setter(*args, **kwargs)

    @abstractmethod
    def mode_setter(self, mode):
        pass

    @property
    @property_fetcher()
    def led_status(self):
        return self._led_status

    @led_status.setter
    def led_status(self, *args, **kwargs):
        return self.led_status_setter(*args, **kwargs)

    @abstractmethod
    def led_status_setter(self, status):
        pass

    @abstractmethod
    def update(self) -> None:
        pass
