"""High-level backend facade used by the Decky Plugin class and CLI."""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import Config
from .installer import InstallError, install_portable, installed_version
from .launcher import write_launcher
from .paths import Paths
from .proton import ProtonOption, default_proton, discover_proton_options
from .releases import ReleaseAsset, download_asset, fetch_latest
from .shortcuts import ensure_shortcut, remove_shortcut, shortcut_exists, signed_appid
from .steam import find_steam_root, resolve_user_config_dir


@dataclass
class Service:
    paths: Paths
    config: Config

    @classmethod
    def create(cls, home: Path | str | None = None) -> Service:
        paths = Paths.create(home)
        paths.ensure()
        config = Config(paths.config_path)
        return cls(paths=paths, config=config)

    def log(self) -> logging.Logger:
        logger = logging.getLogger("gcm_launcher")
        if not logger.handlers:
            self.paths.log_dir.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(self.paths.log_file, encoding="utf-8")
            handler.setFormatter(
                logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            )
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    @property
    def steam_root(self) -> Path | None:
        configured = self.config.get("steam_root")
        if configured:
            return Path(configured)
        return find_steam_root()

    def proton_options(self) -> list[dict[str, str]]:
        root = self.steam_root
        if root is None:
            return []
        return [
            {"root": str(option.root), "name": option.name, "display": option.display}
            for option in discover_proton_options(root)
        ]

    def selected_proton(self) -> ProtonOption | None:
        configured = self.config.get("proton_path")
        if configured:
            option = ProtonOption(
                root=Path(configured),
                name=Path(configured).name,
                display=Path(configured).name,
            )
            if option.proton_script.is_file():
                return option
        root = self.steam_root
        return default_proton(root) if root else None

    def status(self, include_latest: bool = False) -> dict[str, Any]:
        installed = self.paths.gcm_exe.exists()
        version = installed_version(self.paths)
        config_dir = resolve_user_config_dir(self.steam_root) if self.steam_root else None
        appid = self.config.get("shortcut_appid")
        if appid is None and installed:
            appid = signed_appid(str(self.paths.launcher_path))
        latest: ReleaseAsset | None = None
        latest_error = ""
        if include_latest:
            try:
                latest = fetch_latest()
            except Exception as exc:  # noqa: BLE001
                latest_error = str(exc)
        return {
            "installed": installed,
            "version": version,
            "latest": {"tag": latest.tag, "name": latest.name} if latest else None,
            "latest_error": latest_error,
            "shortcut": bool(appid and config_dir and shortcut_exists(config_dir, appid)),
            "shortcut_appid": appid,
            "proton_options": self.proton_options(),
            "proton_path": str(self.selected_proton().root) if self.selected_proton() else "",
            "trainer_dir": str(self.paths.trainer_dir),
            "export_dir": str(self.paths.export_dir),
            "log_file": str(self.paths.log_file),
            "home": str(self.paths.home),
        }

    def latest_status(self) -> dict[str, Any]:
        try:
            asset = fetch_latest()
            return {"tag": asset.tag, "name": asset.name}
        except Exception as exc:  # noqa: BLE001
            return {"error": str(exc)}

    def sync_trainers(self) -> list[dict[str, Any]]:
        """Copy GCM trainers to a simple, CheatDeck-friendly export folder.

        Each trainer is exported as ``~/GCM-Trainers/<game-slug>/`` with a
        ``Trainer.exe`` alias whose path avoids apostrophes and CJK text.
        """
        source_root = self.paths.trainer_dir
        export_root = self.paths.export_dir
        export_root.mkdir(parents=True, exist_ok=True)
        if not source_root.is_dir():
            return []

        def slugify(value: str) -> str:
            value = value.replace("'", "").replace("’", "")
            slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
            return slug or "trainer"

        results: list[dict[str, Any]] = []
        for source_dir in sorted(source_root.iterdir()):
            if not source_dir.is_dir():
                continue
            info_path = source_dir / "gcm_info.json"
            if not info_path.exists():
                continue
            try:
                info = json.loads(info_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            game_name = str(info.get("game_name") or source_dir.name)
            version = str(info.get("version") or "")
            origin = str(info.get("origin") or "gcm")
            slug = slugify(game_name)
            target = export_root / slug
            marker_path = target / ".gcm-export.json"

            stale = True
            if marker_path.exists():
                try:
                    marker = json.loads(marker_path.read_text(encoding="utf-8"))
                    stale = marker.get("version") != version
                except (OSError, ValueError):
                    stale = True
            if not stale and target.exists():
                results.append(
                    {
                        "game": game_name,
                        "origin": origin,
                        "version": version,
                        "folder": str(target),
                        "trainer": str(target / "Trainer.exe"),
                        "changed": False,
                    }
                )
                continue

            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source_dir, target)
            exes = [
                item
                for item in target.rglob("*.exe")
                if item.name.lower() not in {"uninstall.exe"}
            ]
            alias = target / "Trainer.exe"
            if exes and not alias.exists():
                primary = max(exes, key=lambda item: item.stat().st_size)
                if alias.resolve() != primary.resolve():
                    try:
                        os.link(primary, alias)
                    except OSError:
                        shutil.copy2(primary, alias)
            marker_path.write_text(
                json.dumps(
                    {
                        "game_name": game_name,
                        "origin": origin,
                        "version": version,
                        "source": str(source_dir),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            results.append(
                {
                    "game": game_name,
                    "origin": origin,
                    "version": version,
                    "folder": str(target),
                    "trainer": str(target / "Trainer.exe") if exes else "",
                    "changed": True,
                }
            )

        for target in sorted(export_root.iterdir()):
            marker_path = target / ".gcm-export.json"
            if not target.is_dir() or not marker_path.exists():
                continue
            try:
                marker = json.loads(marker_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            source_missing = not Path(str(marker.get("source", ""))).exists()
            expected_slug = slugify(str(marker.get("game_name") or target.name))
            if source_missing or expected_slug != target.name:
                shutil.rmtree(target)
        return results

    def install(self) -> dict[str, Any]:
        logger = self.log()
        asset = fetch_latest()
        logger.info("installing GCM %s from %s", asset.tag, asset.name)
        zip_path = download_asset(asset, self.paths.download_dir)
        try:
            install_portable(self.paths, zip_path, asset.tag)
        except InstallError:
            zip_path.unlink(missing_ok=True)
            raise
        zip_path.unlink(missing_ok=True)
        self.config.set("gcm_version", asset.tag)
        self.config.save()
        return {"version": asset.tag, "exe": str(self.paths.gcm_exe)}

    def set_proton(self, proton_root: str) -> dict[str, str]:
        proton = Path(proton_root)
        if not (proton / "proton").is_file():
            raise ValueError(f"proton binary not found under {proton_root}")
        steam_root = self.steam_root
        if steam_root is not None:
            self.config.set("steam_root", str(steam_root))
        self.config.set("proton_path", str(proton))
        self.config.save()
        return {"proton_path": str(proton)}

    def ensure_shortcut(self) -> dict[str, Any]:
        steam_root = self.steam_root
        if steam_root is None:
            raise RuntimeError("Steam installation not found")
        proton = self.selected_proton()
        if proton is None:
            raise RuntimeError("no Proton compatibility tool found")
        launcher = write_launcher(self.paths, str(proton.root), str(steam_root))
        result = ensure_shortcut(self.paths, steam_root, str(launcher))
        appid = int(result["appid"])
        self.config.set("shortcut_appid", appid)
        self.config.set("launcher_path", str(launcher))
        self.config.save()
        return result

    def remove_shortcut(self) -> dict[str, bool]:
        steam_root = self.steam_root
        appid = self.config.get("shortcut_appid")
        if steam_root is None or appid is None:
            return {"removed": False}
        removed = remove_shortcut(self.paths, steam_root, int(appid))
        self.config.set("shortcut_appid", None)
        self.config.save()
        return {"removed": removed}
