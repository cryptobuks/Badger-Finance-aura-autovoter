import logging

from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(
        rich_tracebacks=True, markup=True,
        console=Console(),
    )],
)
logger = logging.getLogger("rich")
