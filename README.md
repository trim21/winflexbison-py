# winflexbison Python wheel

Python packaging of [lexxmark/winflexbison](https://github.com/lexxmark/winflexbison). The wheel builds the native `win_flex.exe` and `win_bison.exe` binaries with CMake and ships them directly (no Python wrappers).

## What you get
- `win_flex` and `win_bison` executables built from upstream 2.5.25
- `winflexbison` Python module exposing helper functions to locate and run the tools
- Bundled bison `data` directory, Flex headers, upstream custom build rules, and license files

## Requirements
- Windows with the Visual Studio C/C++ toolchain
- CMake 3.25+ (fetched via build dependencies)
- Python 3.8+

## Install from PyPI
```
pip install winflexbison
```
This installs the native `win_flex.exe` and `win_bison.exe` into your Python Scripts directory (no Python wrappers).

## Build from source
Using uv (preferred):
```
uv venv
uv pip install --upgrade pip
uv pip install -e .
```
Or plain pip:
```
python -m venv .venv
.venv\\Scripts\\activate
pip install --upgrade pip
pip install -e .
```
A CMake configure and build will run as part of installation to produce the executables.

## Build a wheel
From a prepared virtualenv:
```
pip wheel . -w dist
```
Upload the resulting wheel to PyPI with `twine upload dist/*.whl`.

## Usage
CLI:
```
win_flex --version
win_bison --version
```

## Package layout
- Python Scripts directory — `win_flex.exe`, `win_bison.exe`, and `data/`
- `winflexbison/include/` — `FlexLexer.h`
- `winflexbison/custom_build_rules/` — Visual Studio build rules from upstream
- `winflexbison/licenses/` — License files for bundled components
- `winflexbison/doc/` — Upstream README and changelog

## Licensing
This distribution bundles GPL-licensed code from winflexbison. See `winflexbison/licenses/` inside the wheel for full license texts.
