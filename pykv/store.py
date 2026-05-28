from collections import OrderedDict
from typing import Dict, Optional
import time

class KVStore:
    def __init__(self):
        self._data: Dict[str, dict] = OrderedDict()  # value + metadata

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        expiry = time.time() + ttl if ttl else None
        self._data[key] = {"value": value, "expiry": expiry}

    def get(self, key: str) -> Optional[str]:
        if key not in self._data:
            return None
        data = self._data[key]
        if data["expiry"] and data["expiry"] < time.time():
            self.delete(key)
            return None
        return data["value"]

    def delete(self, key: str) -> bool:
        return self._data.pop(key, None) is not None

    def exists(self, key: str) -> bool:
        self.get(key)  # clean expired
        return key in self._data

    def all(self) -> Dict[str, str]:
        return {k: v["value"] for k, v in self._data.items() if not v["expiry"] or v["expiry"] > time.time()}

    def size(self) -> int:
        return len(self.all())