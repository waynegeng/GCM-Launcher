from __future__ import annotations

import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PY_MODULES = PLUGIN_ROOT / "py_modules"
if str(PY_MODULES) not in sys.path:
    sys.path.insert(0, str(PY_MODULES))

from gcm_launcher_backend.service import Service  # noqa: E402


@pytest.fixture
def home(tmp_path: Path) -> Path:
    return tmp_path / "gcm-launcher-home"


@pytest.fixture
def service(home: Path) -> Service:
    return Service.create(home)


@pytest.fixture
def fake_steam_root(tmp_path: Path) -> Path:
    root = tmp_path / "steam"
    config = root / "config"
    config.mkdir(parents=True)
    account_dir = root / "userdata" / "278144106" / "config"
    account_dir.mkdir(parents=True)
    (config / "loginusers.vdf").write_text(
        '"users"\n{\n\t"76561198238409834"\n\t{\n\t\t"AccountName" "waynegeng"\n'
        '\t\t"AutoLogin" "1"\n\t\t"Timestamp" "1788949971"\n\t}\n}\n',
        encoding="utf-8",
    )
    return root
