from typing import Optional, Dict, Union, List
from urllib.request import build_opener
from urllib.request import (
    HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
)   
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
import json

from .....base import Device
from .....exceptions import (
    UnauthorizedException,
    InvalidRequestException,
    ConnectionRefusedException,
)

PARA_TYPE = Optional[
    Dict[
        str,
        Union[
            str,
            int,
            float,
            bool,
            List[str]
        ]
    ]
]

EXC_DATA_LIMIT = 0xF

class Request:

    def __init__(self, device: Device):
        self.device = device

    def post(self, path: str, parameter: PARA_TYPE = None):
        if parameter is None:
            parameter = {}

        while path.startswith("/"):
            path = path[1:]

        hostname = self.device.hostname
        port = self.device.port or "80"
        params = urlencode(parameter)
        url = f"http://{hostname}:{port}/{path}"
        if params:
            url += f"?{params}"

        if self.device._debug:
            print(f"[DEBUG] {url}")

        opener = build_opener()
        try:
            if not self.device._credentials:
                raise ValueError()

            username, password = self.device._credentials

            passman = HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, username, password)

            authhandler = HTTPBasicAuthHandler(passman)
            opener.add_handler(authhandler)
        except (TypeError, ValueError):
            # can't unpack
            pass

        try:
            with opener.open(url, timeout=self.device.timeout) as f:
                return f.read().decode()
        except HTTPError as e:
            if e.status == 401:
                raise UnauthorizedException() from None

            raise InvalidRequestException()

        except URLError as e:
            raise ConnectionRefusedException(e.reason) from None

    def json_post(self, *args, **kwargs):
        data = self.post(*args, **kwargs)
        try:
            return json.loads(data)
        except Exception as e:
            data = json.dumps(data)
            if (len(data) > EXC_DATA_LIMIT):
                data = f"{data[:EXC_DATA_LIMIT]}..."
            raise ValueError(f"Expected JSON, received {data}") from None
