"""
Sane project configuration.

https://leontrolski.github.io/sane-config.html
"""
import dataclasses
import functools
from pathlib import Path


@dataclasses.dataclass
class Config:
    """Project configuration."""

    DB_PATH: Path
    MOCK_PATH: Path


@functools.cache
def get_config() -> Config:
    """Return constants."""
    return Config(
        DB_PATH=Path("data/database.db"),
        MOCK_PATH=Path("MOCK_DATA.json"),
    )
