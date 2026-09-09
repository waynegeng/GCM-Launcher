"""User-space directory layout for GCM Launcher."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_HOME_NAME = "gcm-launcher"


def default_home() -> Path:
    configured = os.environ.get("GCM_LAUNCHER_HOME")
    if configured:
        return Path(configured)
    return Path.home() / ".local" / "share" / DEFAULT_HOME_NAME


@dataclass(frozen=True)
class Paths:
    home: Path

    @classmethod
    def create(cls, home: Path | str | None = None) -> Paths:
        return cls(home=Path(home) if home else default_home())

    @property
    def gcm_dir(self) -> Path:
        return self.home / "gcm"

    @property
    def gcm_exe(self) -> Path:
        return self.gcm_dir / "Game Cheats Manager.exe"

    @property
    def prefix_dir(self) -> Path:
        return self.home / "prefix"

    @property
    def bin_dir(self) -> Path:
        return self.home / "bin"

    @property
    def launcher_path(self) -> Path:
        return self.bin_dir / "gcm-launcher"

    @property
    def config_path(self) -> Path:
        return self.home / "config.json"

    @property
    def log_dir(self) -> Path:
        return self.home / "logs"

    @property
    def log_file(self) -> Path:
        return self.log_dir / "gcm-launcher.log"

    @property
    def download_dir(self) -> Path:
        return self.home / "downloads"

    @property
    def backup_dir(self) -> Path:
        return self.home / "backups"

    @property
    def trainer_dir(self) -> Path:
        return (
            self.prefix_dir
            / "pfx"
            / "drive_c"
            / "users"
            / "steamuser"
            / "AppData"
            / "Roaming"
            / "GCM Trainers"
        )

    @property
    def export_dir(self) -> Path:
        configured = os.environ.get("GCM_LAUNCHER_EXPORT_DIR")
        if configured:
            return Path(configured)
        return Path.home() / "GCM-Trainers"

    def ensure(self) -> None:
        for directory in (
            self.gcm_dir,
            self.prefix_dir,
            self.bin_dir,
            self.log_dir,
            self.download_dir,
            self.backup_dir,
            self.export_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)
