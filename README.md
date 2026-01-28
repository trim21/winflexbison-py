# winflexbison Python wheel

Python packaging of [lexxmark/winflexbison](https://github.com/lexxmark/winflexbison). The wheel builds the native `win_flex.exe` and `win_bison.exe` binaries.

## What you get
- A Python package `winflexbison_bin` containing `win_bison.exe`, `win_flex.exe`, and the required `data/` files.
- `win_bison` and `win_flex` console entry points that locate the packaged binaries and execute them.

## Install from PyPI
```
pip install winflexbison-bin
```
This installs lightweight console entry points (`win_flex`, `win_bison`) plus the actual binaries and bison pkgdata files inside the `winflexbison_bin` package.

## Build from source
Using any pep517 build frontend

```
pip -m build .
uv build .
```

## Usage
CLI:
```
win_flex --version
win_bison --version
```

## Licensing
This distribution bundles GPL-licensed code from winflexbison. See `winflexbison/licenses/` inside the wheel for full license texts.
