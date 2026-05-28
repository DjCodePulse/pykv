import json
from datetime import datetime
from typing import Optional
import os

class WAL:
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        if not os.path.exists(filepath):
            open(filepath, 'a').close()

    def log(self, op: str, key: str, value: Optional[str] = None, ttl: Optional[int] = None):
        entry = {
            "ts": datetime.now().isoformat(),
            "op": op,
            "key": key,
            "value": value,
            "ttl": ttl
        }
        with open(self.filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def replay(self, store) -> None:
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, "r") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    e = json.loads(line)
                    if e["op"] == "SET":
                        store.set(e["key"], e["value"], e.get("ttl"))
                except:
                    continue
            