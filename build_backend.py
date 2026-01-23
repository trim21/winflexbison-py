from __future__ import annotations

import zipfile
from pathlib import Path

from packaging.utils import parse_wheel_filename
from scikit_build_core.build import (
    build_editable,
    build_sdist,
    get_requires_for_build_editable,
    get_requires_for_build_sdist,
    get_requires_for_build_wheel,
    prepare_metadata_for_build_wheel,
)
from scikit_build_core.build import build_wheel as _sb_build_wheel


def _inject_bison_data(wheel_path: Path) -> None:
    dist, version, build_tag, tags = parse_wheel_filename(wheel_path.name)
    scripts_prefix = f"{dist}-{version}.data/scripts/"
    # Look for data inside the wheel first (platlib/purelib or already packaged module),
    # then fall back to copying from the source tree.
    staged_prefixes = [
        f"{dist}-{version}.data/platlib/winflexbison/data/",
        f"{dist}-{version}.data/purelib/winflexbison/data/",
        "winflexbison/data/",
    ]

    with zipfile.ZipFile(wheel_path, "a") as zf:
        print(f"winflexbison: injecting bison data into {wheel_path.name}")
        existing_scripts = {
            n
            for n in zf.namelist()
            if n.startswith(scripts_prefix + "data/") and not n.endswith("/")
        }
        if existing_scripts:
            sample = sorted(existing_scripts)[:5]
            print(
                "winflexbison: scripts/data already present "
                f"({len(existing_scripts)} files, sample {sample})"
            )
            return

        for prefix in staged_prefixes:
            staged = [
                n for n in zf.namelist() if n.startswith(prefix) and not n.endswith("/")
            ]
            if not staged:
                continue
            print(f"winflexbison: found staged data at {prefix} ({len(staged)} files)")
            for name in staged:
                rel = name[len(prefix) :]
                target = scripts_prefix + "data/" + rel
                if target in existing_scripts:
                    continue
                zf.writestr(target, zf.read(name))
                existing_scripts.add(target)
            sample = sorted(existing_scripts)[:5]
            print(
                "winflexbison: injected {count} files into scripts/data (sample {sample})".format(
                    count=len(existing_scripts), sample=sample
                )
            )
            return

        # Fallback to copying directly from the source tree if nothing was staged in the wheel.
        data_root = Path(__file__).parent / "upstream" / "bison" / "data"
        if not data_root.is_dir():
            return
        print(f"winflexbison: falling back to source data at {data_root}")
        for file in data_root.rglob("*"):
            if not file.is_file():
                continue
            arcname = scripts_prefix + "data/" + file.relative_to(data_root).as_posix()
            if arcname in existing_scripts:
                continue
            zf.write(file, arcname)
            existing_scripts.add(arcname)
        print(
            f"winflexbison: injected {len(existing_scripts)} files into scripts/data from source"
        )


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    wheel_path = Path(
        _sb_build_wheel(
            wheel_directory,
            config_settings=config_settings,
            metadata_directory=metadata_directory,
        )
    )
    _inject_bison_data(wheel_path)
    return str(wheel_path)


__all__ = [
    "build_wheel",
    "build_sdist",
    "build_editable",
    "get_requires_for_build_wheel",
    "get_requires_for_build_sdist",
    "get_requires_for_build_editable",
    "prepare_metadata_for_build_wheel",
]
