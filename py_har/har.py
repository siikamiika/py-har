from typing import Union
from typing import Optional
from typing import List
from typing import get_type_hints

import datetime
import ipaddress
import sys

# TODO explore typing.TypedDict
class TypedClassDict:
    def __init__(self, **kwargs):
        self._items = {}
        hints = get_type_hints(self.signature) # pylint: disable=no-member
        for k, v in kwargs.items():
            if k not in hints:
                print(f'WARNING: extra argument: [{k}: {v}]', file=sys.stderr)
                continue
            self._items[k] = self._dict_to_value(hints[k], k, v)
        # check missing arguments
        try:
            self.signature(**{k: v for k, v in kwargs.items() if k in hints}) # pylint: disable=no-member
        except TypeError as e:
            raise Exception(f'{type(self).__name__}: {e}')

    def _dict_to_value(self, hint, key, value_raw):
        if hasattr(hint, '__origin__'):
            if hint.__origin__ == Union:
                for hint2 in hint.__args__:
                    try:
                        return self._dict_to_value(hint2, key, value_raw)
                    except Exception as e: # TODO handle errors
                        print(e, file=sys.stderr)
                        continue
            if hint.__origin__ == list:
                hint2 = hint.__args__[0]
                return [self._dict_to_value(hint2, f'{key}[{i}]', v) for i, v in enumerate(value_raw)]
        if issubclass(hint, datetime.datetime):
            return datetime.datetime.fromisoformat(value_raw)
        if issubclass(hint, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            return ipaddress.ip_address(value_raw)
        if issubclass(hint, TypedClassDict):
            return hint(**value_raw)
        if not isinstance(value_raw, hint):
            raise TypeError(f'Type of {key} is {type(value_raw)} and not an instance of {hint}')
        return value_raw

    def to_dict(self):
        items = {}
        hints = get_type_hints(self.signature) # pylint: disable=no-member
        for k, hint in hints.items():
            value = self._items.get(k)
            if value is None: continue
            items[k] = self._value_to_dict(value)
        return items

    def _value_to_dict(self, value):
        if isinstance(value, list):
            return [self._value_to_dict(v) for v in value]
        if isinstance(value, TypedClassDict):
            return value.to_dict()
        if isinstance(value, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            return str(value)
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        return value

class Creator(TypedClassDict):
    def signature(
        self,
        name: str,
        version: str,
        comment: Optional[str]=None,
    ):
        pass

class Browser(TypedClassDict):
    def signature(
        self,
        name: str,
        version: str,
        comment: Optional[str]=None,
    ):
        pass

class PageTimings(TypedClassDict):
    def signature(
        self,
        onContentLoad: int,
        onLoad: int,
        comment: Optional[str]=None,
    ):
        pass

class Page(TypedClassDict):
    def signature(
        self,
        startedDateTime: datetime.datetime,
        id: str,
        title: str,
        pageTimings: PageTimings,
        comment: Optional[str]=None,
    ):
        pass

class Cookie(TypedClassDict):
    def signature(
        self,
        name: str,
        value: str,
        domain: Optional[str]=None,
        expires: Optional[datetime.datetime]=None,
        httpOnly: Optional[bool]=None,
        secure: Optional[bool]=None,
        path: Optional[str]=None,
        comment: Optional[str]=None,
    ):
        pass

class Header(TypedClassDict):
    def signature(
        self,
        name: str,
        value: str,
        comment: Optional[str]=None,
    ):
        pass

class QueryParam(TypedClassDict):
    def signature(
        self,
        name: str,
        value: Optional[str]=None,
        fileName: Optional[str]=None,
        contentType: Optional[str]=None,
        comment: Optional[str]=None,
    ):
        pass

class PostData(TypedClassDict):
    def signature(
        self,
        mimeType: str,
        params: List[QueryParam],
        text: str,
        comment: Optional[str]=None,
    ):
        pass

class Request(TypedClassDict):
    def signature(
        self,
        method: str,
        url: str,
        httpVersion: str,
        cookies: List[Cookie],
        headers: List[Header],
        queryString: List[QueryParam],
        headersSize: int,
        bodySize: int,
        postData: Optional[PostData]=None,
        comment: Optional[str]=None,
    ):
        pass

class Content(TypedClassDict):
    def signature(
        self,
        size: int=0,
        mimeType: str='',
        compression: Optional[int]=None,
        text: Optional[str]=None,
        encoding: Optional[str]=None,
        comment: Optional[str]=None,
    ):
        pass

class Response(TypedClassDict):
    def signature(
        self,
        status: int,
        statusText: str,
        httpVersion: str,
        cookies: List[Cookie],
        headers: List[Header],
        content: Content,
        redirectURL: str,
        bodySize: int,
        headersSize: int=-1,
        comment: Optional[str]=None,
    ):
        pass

class Cache(TypedClassDict):
    def signature(
        self,
        beforeRequest: Optional[object]=None, # TODO
        afterRequest: Optional[object]=None, # TODO
    ):
        pass

class Timings(TypedClassDict):
    def signature(
        self,
        blocked: Optional[int]=None,
        dns: Optional[int]=None,
        connect: Optional[int]=None,
        send: Optional[int]=None,
        wait: Optional[int]=None,
        receive: Optional[int]=None,
        ssl: Optional[int]=None,
        comment: Optional[str]=None,
    ):
        pass

class Entry(TypedClassDict):
    def signature(
        self,
        pageref: str,
        startedDateTime: datetime.datetime,
        time: int,
        request: Request,
        response: Response,
        cache: Cache,
        timings: Timings,
        connection: Optional[str]=None,
        serverIPAddress: Union[ipaddress.IPv4Address, ipaddress.IPv6Address, None]=None,
        _securityState: Optional[str]=None,
        comment: Optional[str]=None,
    ):
        pass

class Log(TypedClassDict):
    def signature(
        self,
        version: str,
        creator: Creator,
        browser: Browser,
        pages: List[Page],
        entries: List[Entry],
        comment: Optional[str]=None,
    ):
        pass

class Har(TypedClassDict):
    def signature(
        self,
        log: Log,
    ):
        pass
