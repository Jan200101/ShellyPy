from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Optional, Tuple, List

from ..utils import property_fetcher, AttributeList

from .hints import transition

if TYPE_CHECKING:
    from .settings import Settings
    from .relay import Relay
    from .roller import Roller
    from .light import Light
    from .meter import Meter

class Device(metaclass=ABCMeta):
    __backends__: List = []

    _hostname: str
    _port: Optional[int]

    _name: Optional[str]
    _type: Optional[str]
    _mac: Optional[str]
    _firmware: Optional[str]

    _timeout: transition
    _credentials: Optional[Tuple[str, str]]

    _debug: bool
    #_backend: object

    _settings: Optional["Settings"] = None
    _relays: Optional[List["Relay"]] = None
    _rollers: Optional[List["Roller"]] = None
    _lights: Optional[List["Light"]] = None
    _meters: Optional[List["Meter"]] = None

    def __init__(self, hostname: str, port: Optional[int] = None, backend: Optional[str] = None, *args, **kwargs):
        self._hostname = hostname
        self._port = port
        # to be filled at runtime
        self._name = None
        self._type = None
        self._mac = None
        self._firmware = None

        self._timeout = kwargs.get("timeout", 5)

        creds = kwargs.get("credentials")

        self.credentials = kwargs.get("credentials", None)

        self._debug = bool(kwargs.get("debug", False))

        if not backend:
            backend_impl = self._load_any_backend()
        else:
            backend_impl = self._load_backend(backend)

        if not backend_impl:
            raise Exception("No suitable backend found")

        self._backend = backend_impl
        self._request = self._backend.Request(self)

        if kwargs.get("preload"):
            self._create_attributes()

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}({self.name or self.type})"

    @abstractmethod
    def _load_any_backend(self):
        pass

    @abstractmethod
    def _load_backend(self, backend_name: str):
        pass

    @abstractmethod
    def _create_attributes(self):
        pass

    @property
    def hostname(self):
        return self._hostname

    @property
    def port(self):
        return self._port

    @property
    @property_fetcher(update_method="_create_attributes")
    def name(self):
        return self._name

    @property
    @property_fetcher(update_method="_create_attributes")
    def type(self):
        return self._type

    @property
    @property_fetcher(update_method="_create_attributes")
    def mac(self):
        return self._mac

    @property
    @property_fetcher(update_method="_create_attributes")
    def firmware(self):
        return self._firmware

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value: int):
        self._timeout = value

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, val):
        if not isinstance(val, tuple) or len(val) != 2:
            val = ()

        self._credentials = val

    @property
    def backend(self):
        return self._backend

    @property
    def request(self):
        return self._request

    @property
    @property_fetcher(update_method="_create_attributes")
    def settings(self):
        return self._settings

    @property
    @property_fetcher(update_method="_create_attributes")
    def relays(self):
        return self._relays

    @property
    @property_fetcher(update_method="_create_attributes")
    def rollers(self):
        return self._rollers

    @property
    @property_fetcher(update_method="_create_attributes")
    def lights(self):
        return self._lights

    @property
    @property_fetcher(update_method="_create_attributes")
    def meters(self):
        return self._meters

    @classmethod
    def connect(cls, *args, **kwargs):
        return cls(*args, **kwargs)
