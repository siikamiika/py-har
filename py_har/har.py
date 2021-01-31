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
        self._hints = get_type_hints(self.signature) # pylint: disable=no-member
        for k, v in kwargs.items():
            if k not in self._hints:
                print(f'WARNING: extra argument: [{k}: {v}]', file=sys.stderr)
                continue
            self._items[k] = self._dict_to_value(self._hints[k], k, v)
        # check missing arguments
        try:
            self.signature(**{k: v for k, v in kwargs.items() if k in self._hints}) # pylint: disable=no-member
        except TypeError as e:
            raise Exception(f'{type(self).__name__}: {e}')

    def set(self, key, value):
        self._items[key] = self._dict_to_value(self._hints[key], key, value)

    def get(self, key):
        return self._items.get(key)

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
            return datetime.datetime.fromisoformat(value_raw.replace('Z', '+00:00'))
        if issubclass(hint, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            return ipaddress.ip_address(value_raw)
        if issubclass(hint, TypedClassDict):
            return hint(**value_raw)
        if not isinstance(value_raw, hint):
            raise TypeError(f'Type of {key} is {type(value_raw)} and not an instance of {hint}')
        return value_raw

    def items(self):
        return {**self._items}

    def to_dict(self):
        items = {}
        for k, hint in self._hints.items():
            value = self._items.get(k)
            if value is None: continue
            items[k] = self._value_to_dict(value)
        return items

    def flat_properties_to_dict(self, include_raw=False):
        items = {}
        # include None
        for k in self._hints:
            value = self._items.get(k)
            if isinstance(value, (TypedClassDict, list)):
                if include_raw:
                    items[k] = value
                continue
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
        onContentLoad: Union[int, float],
        onLoad: Union[int, float],
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
        blocked: Union[int, float, None]=None,
        dns: Union[int, float, None]=None,
        connect: Union[int, float, None]=None,
        send: Union[int, float, None]=None,
        wait: Union[int, float, None]=None,
        receive: Union[int, float, None]=None,
        ssl: Union[int, float, None]=None,
        comment: Optional[str]=None,
    ):
        pass

class Entry(TypedClassDict):
    def signature(
        self,
        pageref: str,
        startedDateTime: datetime.datetime,
        time: Union[int, float],
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
        pages: List[Page],
        entries: List[Entry],
        browser: Optional[Browser]=None,
        comment: Optional[str]=None,
    ):
        pass

class Har(TypedClassDict):
    def signature(
        self,
        log: Log,
    ):
        pass
