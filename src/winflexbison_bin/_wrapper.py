from __future__ import annotations

import sys
from pathlib import Path

from . import get_bison_path, get_flex_path


def _exec(binary: Path, argv: list[str]) -> None:
    import subprocess

    code = subprocess.call([str(binary), *argv])
    raise SystemExit(code)


def main_win_bison() -> None:
    binary = get_bison_path()
    if not binary.exists():
        raise SystemExit(f"win_bison binary not found at {binary}")
    _exec(binary, sys.argv[1:])


def main_win_flex() -> None:
    binary = get_flex_path()
    if not binary.exists():
        raise SystemExit(f"win_flex binary not found at {binary}")
    _exec(binary, sys.argv[1:])
