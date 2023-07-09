from typing import Optional, Dict, Union, List
from urllib.request import build_opener
from urllib.request import (
    HTTPDigestAuthHandler, HTTPPasswordMgrWithDefaultRealm
)   
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from hashlib import sha256
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

_PAYLOAD_COUNTER = 0

# Default urllib digest handler does not support SHA-256
class ShellyDigestAuthHandler(HTTPDigestAuthHandler):
    def get_algorithm_impls(self, algorithm):
        if algorithm == "SHA-256":
            H = lambda x: sha256(x.encode("ascii")).hexdigest()
        else:
            return super().get_algorithm_impls(algorithm)
        KD = lambda s, d: H("%s:%s" % (s, d))
        return H, KD

class Request:

    def __init__(self, device: Device):
        self.auth = None
        self.device = device

    @staticmethod
    def get_payload_id():
        global _PAYLOAD_COUNTER

        _PAYLOAD_COUNTER += 1
        return _PAYLOAD_COUNTER

    @staticmethod
    def sha256(inp: str) -> str:
        return sha256(str.encode()).hexdigest()

    def post(self, method: str, params: PARA_TYPE = None):
        hostname = self.device.hostname
        port = self.device.port or "80"
        url = f"http://{hostname}:{port}/rpc"

        payload_id = self.get_payload_id()
        payload = {
            "jsonrpc": "2.0",
            "id": payload_id,
            "method": method,
        }

        if params is not None:
            payload["params"] = params

        if self.device._debug:
            str_params = ", ".join([f"{k}={v}" for k,v in params.items()])
            print(f"[DEBUG] {method}({str_params})")

        opener = build_opener()

        raw_payload = json.dumps(payload)
        raw_payload_bytes = raw_payload.encode('utf-8')   # needs to be bytes

        opener.addheaders = [
            ('Content-Type', 'application/json; charset=utf-8'),
            ('Content-Length', len(raw_payload_bytes))
        ]

        try:
            if not self.device._credentials:
                raise ValueError()

            username, password = "admin", self.device._credentials[1]

            passman = HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, username, password)

            authhandler = ShellyDigestAuthHandler(passman)
            opener.add_handler(authhandler)
        except (TypeError, IndexError):
            # can't unpack
            pass

        try:
            with opener.open(url, data=raw_payload_bytes, timeout=self.device.timeout) as f:
                result = f.read().decode()

                try:
                    data = json.loads(result)
                except Exception as e:
                    data = json.dumps(result)
                    if (len(data) > EXC_DATA_LIMIT):
                        data = f"{data[:EXC_DATA_LIMIT]}..."
                    raise ValueError(f"Expected JSON, received {data}") from None

                if (data["id"] != payload_id):
                    raise ValueError("Invalid payload ID")

                try:
                    return data["result"]
                except KeyError:
                    raise InvalidRequestException(data["error"]["message"])

        except HTTPError as e:
            if e.status == 401:
                raise UnauthorizedException() from None

            raise InvalidRequestException()

        except URLError as e:
            raise ConnectionRefusedException(e.reason) from None

    def json_post(self, *args, **kwargs):
        return self.post(*args, **kwargs)
