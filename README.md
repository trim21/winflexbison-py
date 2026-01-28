# winflexbison Python wheel

Python packaging of [lexxmark/winflexbison](https://github.com/lexxmark/winflexbison).

## Install from PyPI
```
pip install winflexbison-bin
```

This installs lightweight console entry points (`win_flex`, `win_bison`) plus the actual binaries and bison pkgdata files inside the `winflexbison_bin` package.


```
win_flex.exe --help
win_bison.exe --help
```

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
