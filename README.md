# winflexbison Python wheel

Python packaging of [lexxmark/winflexbison](https://github.com/lexxmark/winflexbison). The wheel builds the native `win_flex.exe` and `win_bison.exe` binaries.

## What you get
- `win_flex` and `win_bison` executables built from upstream.

## Install from PyPI
```
pip install winflexbison
```
This installs the native `win_flex.exe` and `win_bison.exe` into your Python Scripts directory (no Python wrappers).

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
