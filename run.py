import uvicorn
import asyncio
from pykv.config import settings

async def main():
    print(f"🚀 pykv started!")
    print(f"   HTTP  → http://127.0.0.1:{settings.http_port}")
    print(f"   TCP   → {settings.host}:{settings.tcp_port} (coming soon)")

    config = uvicorn.Config("pykv.api:app", host="0.0.0.0", port=settings.http_port, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())