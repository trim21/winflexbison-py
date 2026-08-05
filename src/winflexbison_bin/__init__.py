from __future__ import annotations

from pathlib import Path

__all__ = [
    "get_bison_path",
    "get_flex_path",
    "get_payload_root",
]


def get_payload_root() -> Path:
    """Return the root directory containing the packaged winflexbison payload."""
    return Path(__file__).resolve().parent / "_payload"


def get_bison_path() -> Path:
    """Return the path to the packaged win_bison executable."""
    return get_payload_root() / "win_bison.exe"


def get_flex_path() -> Path:
    """Return the path to the packaged win_flex executable."""
    return get_payload_root() / "win_flex.exe"
