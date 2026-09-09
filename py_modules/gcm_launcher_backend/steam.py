"""Locate the active Steam user's configuration directories."""

from __future__ import annotations

import os
from pathlib import Path


def find_steam_root() -> Path | None:
    configured = os.environ.get("GCM_LAUNCHER_STEAM_ROOT")
    if configured:
        root = Path(configured)
        return root if root.is_dir() else None
    candidates = [
        Path.home() / ".local" / "share" / "Steam",
        Path.home() / ".steam" / "steam",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def _active_account_id(steam_root: Path) -> int | None:
    login_users = steam_root / "config" / "loginusers.vdf"
    if login_users.exists():
        try:
            import vdf

            data = vdf.load(login_users.open(encoding="utf-8", errors="replace"))
        except Exception:  # noqa: BLE001
            data = None
        users = data.get("users", {}) if isinstance(data, dict) else {}
        if users:
            auto_login = [
                (sid, info)
                for sid, info in users.items()
                if isinstance(info, dict) and str(info.get("AutoLogin")) == "1"
            ]
            candidates = auto_login or sorted(
                users.items(),
                key=lambda pair: int(pair[1].get("Timestamp", "0"))
                if isinstance(pair[1], dict)
                else 0,
                reverse=True,
            )
            if candidates:
                try:
                    return int(candidates[0][0]) & 0xFFFFFFFF
                except (TypeError, ValueError):
                    pass

    userdata = steam_root / "userdata"
    if userdata.is_dir():
        account_dirs = sorted(
            (item for item in userdata.iterdir() if item.is_dir()),
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        )
        if account_dirs:
            try:
                return int(account_dirs[0].name)
            except ValueError:
                pass
    return None


def resolve_user_config_dir(steam_root: Path | str | None = None) -> Path | None:
    root = Path(steam_root) if steam_root else find_steam_root()
    if root is None:
        return None
    account_id = _active_account_id(root)
    if account_id is None:
        return None
    return root / "userdata" / str(account_id) / "config"
