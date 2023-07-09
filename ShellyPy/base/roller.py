from abc import ABCMeta, abstractmethod
from typing import Literal, Optional

from ..utils import property_fetcher

from .hints import percent

class Roller(metaclass=ABCMeta):
    _index: int

    _state: Literal["stop", "open", "close"]
    _power: int
    _safety_switch: bool
    _stop_reason: Literal["normal", "safety_switch", "obstacle", "overpower"]
    _last_direction: Literal["open", "close"] # documented as bool?
    _pos: percent

    _calibrating: bool
    _positioning: bool

    def __init__(self, device, index, *args, **kwargs):
        self._device = device
        self._index = index

        self._power = None
        self._safety_switch = None
        self._stop_reason = None
        self._last_direction = None
        self._pos = None

        self._calibrating = None
        self._positioning = None

    def __repr__(self):
        class_name = self.__class__.__name__
        pos = self.pos
        if pos == "100":
            pos = "close"
        elif pos == "0":
            pos = "open"

        return f"{class_name}{self.index}(pos={pos})"

    @property
    def index(self) -> int:
        return self._index

    @property
    @property_fetcher()
    def state(self) -> str: # TODO typing
        return self._state

    @property
    @property_fetcher()
    def power(self) -> int:
        return max(self._power, 0)

    @property
    @property_fetcher()
    def safety_switch(self) -> bool:
        return bool(self._safety_switch)

    @property
    @property_fetcher()
    def stop_reason(self) -> str: # TODO typing
        return self._stop_reason

    @property
    @property_fetcher()
    def last_direction(self) -> str: # TODO typing
        return self._last_direction

    @property
    @property_fetcher()
    def pos(self) -> percent:
        return self._pos

    @pos.setter
    def pos(self, value: percent):
        self.pos_setter(value)

    @abstractmethod
    def pos_setter(self, value: percent):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def to_pos(self, pos: percent):
        self.pos = pos

    def go(self, state: Literal["open", "close", "stop", "to_pos"], pos: Optional[percent] = None):

        if state == "to_pos":
            if pos is None:
                raise TypeError("pos cannot be None")
            return self.to_pos(pos)

        state_method = {
            "open": self.open,
            "close": self.close,
            "stop": self.stop,
        }

        return state_method[state]()

    @property
    @property_fetcher()
    def calibrating(self) -> bool:
        return bool(self._calibrating)

    @property
    @property_fetcher()
    def positioning(self) -> bool:
        return bool(self._positioning)

    @abstractmethod
    def update(self) -> None:
        pass
