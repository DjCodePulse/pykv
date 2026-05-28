import os
from dataclasses import dataclass

@dataclass
class Settings:
    host: str = "127.0.0.1"
    tcp_port: int = 6379
    http_port: int = 8000
    data_dir: str = "data"
    wal_file: str = "wal.log"

    @property
    def wal_path(self) -> str:
        os.makedirs(self.data_dir, exist_ok=True)
        return os.path.join(self.data_dir, self.wal_file)

# Global settings object
settings = Settings()
