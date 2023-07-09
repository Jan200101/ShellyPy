from typing import Optional
from importlib import import_module

from ...base import Device as BaseDevice
from ...exceptions import InvalidBackend
from ...utils.attribute_list import AttributeList
from ...utils import property_fetcher

class Device(BaseDevice):
    __backends__ = [
        "http",
    ]

    def _load_any_backend(self):
        for backend in self.__backends__:
            try:
                return self._load_backend(backend)
            except:
                continue

        raise Exception("Failed to load any backend")

    def _load_backend(self, backend_name: str):
        module_name = ".".join(self.__class__.__module__.split(".")[:-1])
        return import_module(f".backends.{backend_name}", module_name)

    def _create_attributes(self):
        self._relays = AttributeList()
        self._rollers = AttributeList()
        self._lights = AttributeList()
        self._meters = AttributeList()
        self._loaded_meters = False

        # settings populate attributes
        self._settings = self._backend.Settings(self)
        self._settings.update()

    @property
    @property_fetcher(update_method="_create_attributes")
    def meters(self):
        if not self._loaded_meters:
            self._loaded_meters = True
            # there is no way to query meters without brute force
            meter_index = 0
            while True:
                
                meter = self._backend.Meter(self._request, meter_index)
                try:
                    meter.update()
                except:
                    break

                self.meter.append(meter)
                meter_index += 1

        return super().meters
