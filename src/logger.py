from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("rich")

def log_success(message):
    console.print(f"[green]✔ {message}[/green]")

def log_error(message):
    console.print(f"[red]✖ {message}[/red]")

def log_info(message):
    console.print(f"[blue]ℹ {message}[/blue]")