"""Read/write Steam non-Steam shortcuts (shortcuts.vdf)."""

from __future__ import annotations

import binascii
import os
import tempfile
import time
from pathlib import Path
from typing import Any

import vdf

from .paths import Paths
from .steam import resolve_user_config_dir

LAUNCH_OPTIONS = "gcm:launch"
OWNER_TAG = "GCM Launcher"
APP_NAME = "Game Cheats Manager"


def signed_appid(launcher_path: str) -> int:
    """Steam/Unifideck-compatible non-Steam shortcut appid."""
    key = f"{launcher_path}|{LAUNCH_OPTIONS}"
    crc = binascii.crc32(key.encode("utf-8")) | 0x80000000
    if crc > 0x7FFFFFFF:
        crc -= 0x100000000
    return crc


def build_entry(launcher_path: str, appid: int, start_dir: str = "") -> dict[str, Any]:
    return {
        "appid": appid,
        "AppName": APP_NAME,
        "Exe": f'"{launcher_path}"',
        "StartDir": f'"{start_dir}"' if start_dir else '""',
        "icon": "",
        "ShortcutPath": "",
        "LaunchOptions": LAUNCH_OPTIONS,
        "IsHidden": 0,
        "AllowDesktopConfig": 1,
        "AllowOverlay": 1,
        "OpenVR": 0,
        "Devkit": 0,
        "DevkitGameID": "",
        "DevkitOverrideAppID": 0,
        "LastPlayTime": 0,
        "FlatpakAppID": "",
        "tags": {"0": OWNER_TAG},
    }


def read_shortcuts(config_dir: Path) -> dict[str, Any]:
    shortcuts_path = config_dir / "shortcuts.vdf"
    if not shortcuts_path.exists():
        return {"shortcuts": {}}
    try:
        data = vdf.binary_loads(shortcuts_path.read_bytes())
    except Exception:  # noqa: BLE001
        raise ValueError(f"could not parse {shortcuts_path}") from None
    if not isinstance(data, dict) or not isinstance(data.get("shortcuts"), dict):
        return {"shortcuts": {}}
    return data


def _write_shortcuts(paths: Paths, config_dir: Path, data: dict[str, Any]) -> Path:
    shortcuts_path = config_dir / "shortcuts.vdf"
    config_dir.mkdir(parents=True, exist_ok=True)
    original_mode = shortcuts_path.stat().st_mode if shortcuts_path.exists() else 0o100644

    backup_dir = paths.backup_dir
    backup_dir.mkdir(parents=True, exist_ok=True)
    if shortcuts_path.exists():
        backup = backup_dir / f"shortcuts.vdf.bak.{int(time.time())}"
        backup.write_bytes(shortcuts_path.read_bytes())

    fd, raw = tempfile.mkstemp(prefix=".shortcuts-", suffix=".tmp", dir=config_dir)
    os.close(fd)
    temp_path = Path(raw)
    temp_path.write_bytes(vdf.binary_dumps(data))
    temp_path.chmod(original_mode & 0o7777)
    temp_path.replace(shortcuts_path)
    return shortcuts_path


def ensure_shortcut(paths: Paths, steam_root: Path, launcher_path: str) -> dict[str, Any]:
    config_dir = resolve_user_config_dir(steam_root)
    if config_dir is None:
        raise RuntimeError("could not locate active Steam user config directory")
    data = read_shortcuts(config_dir)
    inner = data.setdefault("shortcuts", {})
    appid = signed_appid(launcher_path)

    existing_key: str | None = None
    for key, entry in inner.items():
        if isinstance(entry, dict) and entry.get("appid") == appid:
            existing_key = str(key)
            break
    entry = build_entry(launcher_path, appid, start_dir=str(Path(launcher_path).parent))
    if existing_key is not None:
        inner[existing_key] = entry
    else:
        numeric = [int(key) for key in inner if str(key).isdigit()]
        next_key = str(max(numeric, default=-1) + 1)
        inner[next_key] = entry
    _write_shortcuts(paths, config_dir, data)
    return {
        "appid": appid,
        "shortcuts_path": str(config_dir / "shortcuts.vdf"),
        "restart_required": True,
    }


def remove_shortcut(paths: Paths, steam_root: Path, appid: int) -> bool:
    config_dir = resolve_user_config_dir(steam_root)
    if config_dir is None:
        raise RuntimeError("could not locate active Steam user config directory")
    data = read_shortcuts(config_dir)
    inner = data.setdefault("shortcuts", {})
    removed = False
    for key in list(inner):
        entry = inner[key]
        if isinstance(entry, dict) and entry.get("appid") == appid:
            del inner[key]
            removed = True
    if removed:
        _write_shortcuts(paths, config_dir, data)
    return removed


def shortcut_exists(config_dir: Path, appid: int) -> bool:
    try:
        data = read_shortcuts(config_dir)
    except ValueError:
        return False
    for entry in data.get("shortcuts", {}).values():
        if isinstance(entry, dict) and entry.get("appid") == appid:
            return True
    return False
