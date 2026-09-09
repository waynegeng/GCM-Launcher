"""Install/update the official GCM Portable build into user space."""

from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path

from .paths import Paths


class InstallError(RuntimeError):
    pass


def _locate_exe(root: Path) -> Path | None:
    direct = root / "Game Cheats Manager.exe"
    if direct.is_file():
        return direct
    matches = list(root.rglob("Game Cheats Manager.exe"))
    if matches:
        return matches[0]
    return None


def install_portable(paths: Paths, archive: Path, version: str) -> Path:
    """Extract an official Portable zip and atomically replace ``gcm/``."""
    archive = Path(archive)
    if not archive.is_file():
        raise InstallError(f"archive not found: {archive}")
    staging = Path(tempfile.mkdtemp(prefix="gcm-extract-"))
    try:
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(staging)
        exe = _locate_exe(staging)
        if exe is None:
            raise InstallError("archive does not contain Game Cheats Manager.exe")
        source_root = exe.parent

        paths.ensure()
        backup: Path | None = None
        if paths.gcm_exe.exists() or paths.gcm_dir.exists():
            backup = paths.gcm_dir.with_name("gcm.old")
            shutil.rmtree(backup, ignore_errors=True)
            shutil.move(str(paths.gcm_dir), str(backup))
        try:
            shutil.copytree(source_root, paths.gcm_dir)
            if backup is not None:
                shutil.rmtree(backup, ignore_errors=True)
        except Exception:
            if paths.gcm_dir.exists():
                shutil.rmtree(paths.gcm_dir, ignore_errors=True)
            if backup is not None and backup.exists():
                shutil.move(str(backup), str(paths.gcm_dir))
            raise
        if not paths.gcm_exe.exists():
            raise InstallError("installation completed but GCM executable is missing")
        marker = paths.gcm_dir / ".gcm_version"
        marker.write_text(version, encoding="utf-8")
        return paths.gcm_exe
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def installed_version(paths: Paths) -> str:
    marker = paths.gcm_dir / ".gcm_version"
    if marker.exists():
        try:
            return marker.read_text(encoding="utf-8").strip()
        except OSError:
            return ""
    return ""
