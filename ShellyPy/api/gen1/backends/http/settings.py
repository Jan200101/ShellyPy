from .....base import Settings as BaseSettings

class Settings(BaseSettings):

    def _fetch(self, *args, **kwargs):
        data = self._device._request.json_post(*args, *kwargs)

        device = data.get("device", {})
        self._device._name = data.get("name")
        self._device._type = device.get("type")
        self._device._mac = device.get("mac")
        self._device._firmware = data.get("fw")

        for index, state in enumerate(data.get("relays", [])):
            self._device._relays.append(self._device._backend.Relay(self._device, index, **state))

        for index, state in enumerate(data.get("rollers", [])):
            self._device._rollers.append(self._device._backend.Roller(self._device, index, **state))

        for index, state in enumerate(data.get("lights", [])):
            self._device._lights.append(self._device._backend.Light(self._device, index, **state))

        self._max_power = not data.get("max_power")
        self._mode = not data.get("mode")
        self._led_status = not data.get("led_status_disable", False)

        return data

    def max_power_setter(self, power):
        self._fetch(f"settings", {"max_power": power})

    def mode_setter(self, mode):
        self._fetch(f"settings", {"mode": mode})

    def led_status_setter(self, status):
        self._fetch(f"settings", {"led_status_disable": not power})

    def update(self) -> None:
        self._fetch(f"settings")
