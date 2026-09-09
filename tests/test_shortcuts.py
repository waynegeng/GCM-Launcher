from __future__ import annotations

from pathlib import Path

import vdf
from gcm_launcher_backend.paths import Paths
from gcm_launcher_backend.shortcuts import (
    ensure_shortcut,
    read_shortcuts,
    remove_shortcut,
    signed_appid,
)

DEFAULT_LAUNCHER = "/home/deck/.local/share/gcm-launcher/bin/gcm-launcher"


def test_appid_is_deterministic() -> None:
    assert signed_appid(DEFAULT_LAUNCHER) == -55725736
    assert signed_appid(DEFAULT_LAUNCHER) == signed_appid(DEFAULT_LAUNCHER)


def test_ensure_and_remove_shortcut_preserves_foreign_entries(
    tmp_path: Path, fake_steam_root: Path
) -> None:
    paths = Paths.create(tmp_path / "home")
    paths.ensure()
    config_dir = fake_steam_root / "userdata" / "278144106" / "config"
    original = {
        "shortcuts": {
            "0": {
                "appid": -123,
                "AppName": "Another Game",
                "Exe": '"/usr/bin/something"',
                "StartDir": '""',
                "LaunchOptions": "",
                "tags": {"0": "user"},
            }
        }
    }
    (config_dir / "shortcuts.vdf").write_bytes(vdf.binary_dumps(original))

    result = ensure_shortcut(paths, fake_steam_root, DEFAULT_LAUNCHER)
    assert result["restart_required"] is True
    data = read_shortcuts(config_dir)
    inner = data["shortcuts"]
    assert any(entry.get("appid") == -123 for entry in inner.values())
    assert any(
        entry.get("appid") == -55725736
        and entry.get("LaunchOptions") == "gcm:launch"
        for entry in inner.values()
    )

    assert remove_shortcut(paths, fake_steam_root, -55725736) is True
    data = read_shortcuts(config_dir)
    assert not any(entry.get("appid") == -55725736 for entry in data["shortcuts"].values())
    assert any(entry.get("appid") == -123 for entry in data["shortcuts"].values())
