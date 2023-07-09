from .....base import Settings as BaseSettings
from .....exceptions.backend import UnimplementedMethod

class Settings(BaseSettings):

    def _fetch(self, method, **kwargs):
        result = self._device._request.post(method, kwargs)

        self._device._name = result.get("name")
        self._device._type = result.get("model")
        self._device._mac = result.get("mac")
        self._device._firmware = result.get("fw_id")
        return result

    def max_power_setter(self, power):
        raise UnimplementedMethod("TODO Gen2 Settings::max_power_setter()")

    def mode_setter(self, mode):
        raise UnimplementedMethod("TODO Gen2 Settings::mode_setter()")

    def led_status_setter(self, status):
        raise UnimplementedMethod("TODO Gen2 Settings::led_status_setter()")

    def update(self) -> None:
        self._fetch("Shelly.GetDeviceInfo")
