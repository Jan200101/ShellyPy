from typing import Optional
from importlib import import_module

from ...base import Device as BaseDevice
from ...exceptions import InvalidBackend, InvalidRequestException
from ...utils.attribute_list import AttributeList
from ...utils import property_fetcher

class Device(BaseDevice):
    __backends__ = [
        "json_rpc",
    ]

    def _load_any_backend(self):
        for backend in self.__backends__:
            try:
                return self._load_backend(backend)
            except Exception as e:
                continue

        raise Exception("Failed to load any backend")

    def _load_backend(self, backend_name: str):
        module_name = ".".join(self.__class__.__module__.split(".")[:-1])
        return import_module(f".backends.{backend_name}", module_name)

    def _create_attributes(self):
        self._find_relays()
        self._find_rollers()
        self._find_lights()
        self._find_meters()

        self._settings = self._backend.Settings(self)
        self._settings.update()

    @property
    @property_fetcher(update_method="_find_relays")
    def relays(self):
        return super().relays

    def _find_relays(self):
        self._relays = AttributeList() # Switch

        relay_index = 0
        while True:
            relay = self._backend.Relay(self, relay_index)
            try:
                relay.update()
            except InvalidRequestException:
                break
            self._relays.append(relay)
            relay_index += 1

    @property
    @property_fetcher(update_method="_find_rollers")
    def rollers(self):
        return super().rollers

    def _find_rollers(self):
        self._rollers = AttributeList() # Cover

        roller_index = 0
        while True:
            roller = self._backend.Roller(self, roller_index)
            try:
                roller.update()
            except InvalidRequestException:
                break
            self._rollers.append(roller)
            roller_index += 1

    @property
    @property_fetcher(update_method="_find_lights")
    def lights(self):
        return super().lights

    def _find_lights(self):
        self._lights = AttributeList()

        light_index = 0
        while True:
            light = self._backend.Light(self, light_index)
            try:
                light.update()
            except InvalidRequestException:
                break
            self._lights.append(light)
            light_index += 1

    @property
    @property_fetcher(update_method="_find_meters")
    def meters(self):
        return super().meters

    def _find_meters(self):
        self._meters = AttributeList()

        meter_index = 0
        while True:
            meter = self._backend.Meter(self, meter_index)
            try:
                meter.update()
            except InvalidRequestException as e:
                break
            self._meters.append(meter)
            meter_index += 1
