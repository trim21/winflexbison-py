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
    stage_dir = build_dir / "stage"
    payload_root = build_dir / "winflexbison_bin" / "_payload"

    # Ensure the wheel advertises a generic Python tag and no limited API usage.
    context.builder.config_settings = {
        "--python-tag": "py3",
        "--py-limited-api": "none",
        **context.builder.config_settings,
    }

    build_dir.mkdir(parents=True, exist_ok=True)
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    if payload_root.exists():
        shutil.rmtree(payload_root)

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
        str(stage_dir),
    ]

    _run(cmake_configure, env=env)
    _run(cmake_build, env=env)
    _run(cmake_install, env=env)

    payload_root.mkdir(parents=True, exist_ok=True)

    def _copy_bison_data_files(*, install_root: Path, dest_payload_root: Path) -> None:
        # win_bison expects its pkgdata files under `data/` relative to the executable.
        marker_files = list(install_root.rglob("m4sugar.m4"))
        candidates: list[Path] = []
        for marker in marker_files:
            # Expect: <...>/data/m4sugar/m4sugar.m4
            if marker.parent.name != "m4sugar":
                continue
            if marker.parent.parent.name != "data":
                continue
            candidates.append(marker.parent.parent)

        if not candidates:
            raise FileNotFoundError(
                "winflexbison install did not contain expected bison pkgdata marker "
                "'data/m4sugar/m4sugar.m4'"
            )

        # Pick the shortest path (closest to prefix root) to avoid copying from nested build dirs.
        data_dir = sorted(candidates, key=lambda p: len(p.parts))[0]

        dest = dest_payload_root / "data"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(data_dir, dest)

    shutil.copy2(stage_dir.joinpath("win_bison.exe"), payload_root / "win_bison.exe")
    shutil.copy2(stage_dir.joinpath("win_flex.exe"), payload_root / "win_flex.exe")
    _copy_bison_data_files(install_root=stage_dir, dest_payload_root=payload_root)

    shutil.rmtree(stage_dir)
    shutil.rmtree(cmake_dir)


def pdm_build_finalize(context: "Context", artifact: Path) -> None:
    build_dir = Path(context.build_dir)
    for path in (
        build_dir / "cmake-build",
        build_dir / "stage",
        build_dir / "winflexbison_bin" / "_payload",
    ):
        if path.exists():
            shutil.rmtree(path)
