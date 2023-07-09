from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

from ..utils import property_fetcher

class Meter(metaclass=ABCMeta):
    def __init__(self, device, index, *args, **kwargs):
        self._device = device
        self._index = index

        self._power = None
        self._is_valid = None
        self._timestamp = None
        self._counters = None
        self._total = None

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(total={self.total})"

    @property
    def index(self) -> int:
        return self._index

    @property
    @property_fetcher()
    def power(self):
        return self._power

    @property
    @property_fetcher()
    def is_valid(self) -> bool:
        return bool(self._is_valid)

    @property
    @property_fetcher()
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    @property_fetcher()
    def counters(self) -> List[float]:
        return self._counters

    @property
    @property_fetcher()
    def total(self) -> float:
        return self._total

    @abstractmethod
    def update(self) -> None:
        pass
