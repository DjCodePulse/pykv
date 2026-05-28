from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from .store import KVStore
from .wal import WAL
from .config import settings

app = FastAPI(title="pykv API", version="0.1.0")

store = KVStore()
wal = WAL(settings.wal_path)
wal.replay(store)

class KVItem(BaseModel):
    value: str
    ttl: Optional[int] = None

@app.get("/health")
async def health():
    return {"status": "healthy", "size": store.size()}

@app.post("/set/{key}")
async def set_key(key: str, item: KVItem):
    store.set(key, item.value, item.ttl)
    wal.log("SET", key, item.value, item.ttl)
    return {"status": "OK"}

@app.get("/get/{key}")
async def get_key(key: str):
    value = store.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}

@app.delete("/delete/{key}")
async def delete_key(key: str):
    if store.delete(key):
        wal.log("DELETE", key)
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Key not found")

@app.get("/all")
async def get_all() -> Dict[str, str]:
    return store.all()
