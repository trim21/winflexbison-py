from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
import shlex

from pdm.backend.hooks import Context

ROOT_DIR = Path(__file__).parent.resolve()
SOURCE_DIR = ROOT_DIR / "upstream"
DEFAULT_BUILD_TYPE = os.environ.get("CMAKE_BUILD_TYPE", "Release")


def _run(command: list[str], *, env: dict[str, str]) -> None:
    print(f"pdm-build execute: {shlex.join(command)}")
    subprocess.run(command, check=True, env=env)


def pdm_build_hook_enabled(context: Context) -> bool:
    return context.target != "sdist"


def pdm_build_initialize(context: Context) -> None:
    context.ensure_build_dir()
    build_dir = Path(context.build_dir)
    cmake_dir = build_dir / "cmake-build"
    package_dest = build_dir / "winflexbison_bin"
    payload_root = package_dest / "_payload"

    # Ensure the wheel advertises a generic Python tag and no limited API usage.
    context.builder.config_settings = {
        "--python-tag": "py3",
        "--py-limited-api": "none",
        **context.builder.config_settings,
    }

    build_dir.mkdir(parents=True, exist_ok=True)
    if package_dest.exists():
        shutil.rmtree(package_dest)

    env = os.environ.copy()

    cmake_configure = [
        "cmake",
        "-S",
        str(SOURCE_DIR),
        "-B",
        str(cmake_dir),
        f"-DCMAKE_BUILD_TYPE={DEFAULT_BUILD_TYPE}",
    ]
    cmake_build = [
        "cmake",
        "--build",
        str(cmake_dir),
        "--config",
        DEFAULT_BUILD_TYPE,
        "--parallel",
    ]
    cmake_install = [
        "cmake",
        "--install",
        str(cmake_dir),
        "--config",
        DEFAULT_BUILD_TYPE,
        "--prefix",
        str(payload_root),
    ]

    _run(cmake_configure, env=env)
    _run(cmake_build, env=env)
    _run(cmake_install, env=env)

    shutil.copytree(
        ROOT_DIR.joinpath("src/winflexbison_bin"),
        build_dir.joinpath("winflexbison_bin"),
    )

    shutil.rmtree(cmake_dir, ignore_errors=True)


def pdm_build_finalize(context: "Context", artifact: Path) -> None:
    build_dir = Path(context.build_dir)
    for path in (
        build_dir / "cmake-build",
        build_dir / "stage",
        build_dir / "winflexbison_bin",
    ):
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
