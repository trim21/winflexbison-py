import pytest
from winflexbison import win_bison_path, win_flex_path


def test_executable_paths_exist_or_skip():
    flex = win_flex_path()
    bison = win_bison_path()
    missing = [p for p in (flex, bison) if not p.exists()]
    if missing:
        pytest.skip("executables not built yet in this environment")
    assert flex.exists()
    assert bison.exists()
    assert all(p.suffix.lower() == ".exe" for p in (flex, bison))
