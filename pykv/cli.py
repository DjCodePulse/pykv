import typer
from rich.console import Console
from rich.table import Table
from .store import KVStore
from .wal import WAL
from .config import settings

app = typer.Typer(help="pykv - Lightweight Key-Value Store")
console = Console()
store = KVStore()
wal = WAL(settings.wal_path)
wal.replay(store)

@app.command()
def set(key: str, value: str, ttl: int = None):
    """Set a key-value pair"""
    store.set(key, value, ttl)
    wal.log("SET", key, value, ttl)
    console.print(f"✅ [green]SET[/green] {key}")

@app.command()
def get(key: str):
    """Get value by key"""
    value = store.get(key)
    if value is None:
        console.print(f"[red]NIL[/red] {key}")
    else:
        console.print(f"[blue]{value}[/blue]")

@app.command()
def delete(key: str):
    """Delete a key"""
    if store.delete(key):
        wal.log("DELETE", key)
        console.print(f"🗑️ [yellow]DELETED[/yellow] {key}")
    else:
        console.print("[dim]Key not found[/dim]")

@app.command()
def list():
    """List all keys"""
    data = store.all()
    if not data:
        console.print("[dim]No data[/dim]")
        return

    table = Table(title="pykv Store")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")
    for k, v in data.items():
        table.add_row(k, str(v)[:100])
    console.print(table)

if __name__ == "__main__":
    app()
