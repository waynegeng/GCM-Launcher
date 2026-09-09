"""JSON settings for the plugin."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

DEFAULTS: dict[str, Any] = {
    "gcm_version": "",
    "proton_path": "",
    "steam_root": "",
    "shortcut_appid": None,
    "launcher_path": "",
}


class Config:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.values: dict[str, Any] = dict(DEFAULTS)
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    self.values.update(loaded)
            except (OSError, ValueError):
                pass

    def __getitem__(self, key: str):
        return self.values.get(key)

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.values[key] = value

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, raw = tempfile.mkstemp(prefix=".config-", suffix=".tmp", dir=self.path.parent)
        os.close(fd)
        temp_path = Path(raw)
        temp_path.write_text(
            json.dumps(self.values, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_path.replace(self.path)
