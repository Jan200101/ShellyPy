from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import Union, Tuple, Optional

from ..utils import (
    clamp, clamp_percent, clamp_byte,
    clamp_temp, property_fetcher,
)

from .hints import byte, percent, temperaur, transition, rgbw_mode

class Light(metaclass=ABCMeta):
    _index: int

    _ison: bool
    _timer_start: datetime
    _timer_end: datetime

    _mode: rgbw_mode
    _red: byte
    _blue: byte
    _green: byte
    _white: byte
    _gain: percent
    _temp: temperaur
    _brightness: percent

    _effect: int
    _transition: transition

    def __init__(self, device, index, *args, **kwargs):
        self._device = device
        self._index = index

        self._ison = None
        self._timer_started = None
        self._timer_end = None

        self._mode = None
        self._red = None
        self._green = None
        self._blue = None
        self._white = None
        self._gain = None
        self._temp = None
        self._brightness = None

        self._effect = None
        self._transition = None

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

    @property
    @property_fetcher()
    def mode(self) -> rgbw_mode:
        return self._mode

    @mode.setter
    def mode(self, mode: rgbw_mode):
        if mode != "color" and mode != "white":
            raise Exception("mode has to be 'color' or 'white'")

        self.mode_setter(mode)

    @abstractmethod
    def mode_setter(self, mode: rgbw_mode):
        pass

    # color mode
    @property
    @property_fetcher()
    def red(self) -> byte:
        return clamp_byte(self._red)

    @red.setter
    def red(self, *args, **kwargs):
        return self.red_setter(*args, **kwargs)

    @abstractmethod
    def red_setter(self, val: byte):
        pass

    @property
    @property_fetcher()
    def green(self) -> byte:
        return clamp_byte(self._green)

    @green.setter
    def green(self, *args, **kwargs):
        return self.green_setter(*args, **kwargs)

    @abstractmethod
    def green_setter(self, val: byte):
        pass

    @property
    @property_fetcher()
    def blue(self) -> byte:
        return clamp_byte(self._blue)

    @blue.setter
    def blue(self, *args, **kwargs):
        return self.blue_setter(*args, **kwargs)

    @abstractmethod
    def blue_setter(self, val: byte):
        pass

    @property
    @property_fetcher()
    def white(self) -> byte:
        return clamp_byte(self._white)

    @white.setter
    def white(self, *args, **kwargs):
        return self.white_setter(*args, **kwargs)

    @abstractmethod
    def white_setter(self, val: byte):
        pass

    @property
    def rgb(self) -> Tuple[byte, byte, byte]:
        return (self.red, self.green, self.blue)

    @rgb.setter
    def rgb(self, *args, **kwargs):
        return self.rgb_setter(*args, **kwargs)

    def rgb_setter(self, rgb: Tuple[byte, byte, byte]):
        self.red, self.green, self.blue = rgb

    @property
    def rgbw(self) -> Tuple[byte, byte, byte, byte]:
        return self.rgb + (self.white,)

    @rgbw.setter
    def rgbw(self, *args, **kwargs):
        return self.rgbw_setter(*args, **kwargs)

    def rgbw_setter(self, rgbw: Tuple[byte, byte, byte, byte]):
        self.rgb = rgbw[:3]
        self.white = rgbw[3]

    @property
    @property_fetcher()
    def gain(self) -> percent:
        return clamp_percent(self._gain)

    # white mode
    @property
    @property_fetcher()
    def temp(self) -> temperaur:
        return clamp_temp(self._temp)

    @property
    @property_fetcher()
    def brightness(self) -> percent:
        return clamp_percent(self._brightness)

    @brightness.setter
    def brightness(self, *args, **kwargs):
        return brightness_setter(*args, **kwargs)

    @abstractmethod
    def brightness_setter(self, val: percent):
        pass

    @property
    @property_fetcher()
    def effect(self) -> int:
        return self._effect

    @property
    @property_fetcher()
    def transition(self) -> transition:
        return self._transition

    @abstractmethod
    def update(self) -> None:
        pass
