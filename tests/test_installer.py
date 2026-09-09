from __future__ import annotations

import zipfile
from pathlib import Path

from gcm_launcher_backend.installer import install_portable, installed_version
from gcm_launcher_backend.paths import Paths


def _portable_zip(path: Path, version: str, content: str = "MZ") -> None:
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("_internal/Game Cheats Manager.exe", content.encode())
        zf.writestr("readme.txt", f"v{version}")


def test_install_and_update(home: Path, tmp_path: Path) -> None:
    paths = Paths.create(home)
    paths.ensure()
    first = tmp_path / "gcm-v2.5.0.zip"
    _portable_zip(first, "2.5.0")
    install_portable(paths, first, "v2.5.0")
    assert paths.gcm_exe.is_file()
    assert installed_version(paths) == "v2.5.0"

    second = tmp_path / "gcm-v2.6.0.zip"
    _portable_zip(second, "2.6.0", content="NEW-MZ")
    install_portable(paths, second, "v2.6.0")
    assert installed_version(paths) == "v2.6.0"
    assert paths.gcm_exe.read_text(encoding="utf-8") == "NEW-MZ"


def test_install_missing_exe_raises(home: Path, tmp_path: Path) -> None:
    paths = Paths.create(home)
    paths.ensure()
    bad = tmp_path / "bad.zip"
    with zipfile.ZipFile(bad, "w") as zf:
        zf.writestr("random.txt", "not a game")
    try:
        install_portable(paths, bad, "v1")
    except Exception as exc:
        assert "Game Cheats Manager.exe" in str(exc)
    else:
        raise AssertionError("expected InstallError")
