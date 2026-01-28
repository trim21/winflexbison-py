from __future__ import annotations

import sys
from pathlib import Path

__all__ = [
    "get_payload_root",
    "get_bison_path",
    "get_flex_path",
]


def get_payload_root() -> Path:
    """Return the root directory containing the packaged winflexbison payload."""
    return Path(__file__).resolve().parent / "_payload"


def get_bison_path() -> Path:
    """Return the path to the packaged win_bison executable."""
    return get_payload_root() / "bin" / "Release" / "win_bison.exe"


def get_flex_path() -> Path:
    """Return the path to the packaged win_flex executable."""
    return get_payload_root() / "bin" / "Release" / "win_flex.exe"


def _exec(binary: Path, argv: list[str]) -> None:
    import subprocess

    code = subprocess.call([str(binary), *argv])
    raise SystemExit(code)


def _main_win_bison() -> None:
    binary = get_bison_path()
    if not binary.exists():
        raise SystemExit(f"win_bison binary not found at {binary}")
    _exec(binary, sys.argv[1:])


def _main_win_flex() -> None:
    binary = get_flex_path()
    if not binary.exists():
        raise SystemExit(f"win_flex binary not found at {binary}")
    _exec(binary, sys.argv[1:])
