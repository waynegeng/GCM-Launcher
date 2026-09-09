"""GCM Launcher Decky plugin entry point."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

PLUGIN_DIR = Path(os.environ.get("DECKY_PLUGIN_DIR", str(Path(__file__).parent)))
PY_MODULES = PLUGIN_DIR / "py_modules"
if PY_MODULES.is_dir():
    sys.path.insert(0, str(PY_MODULES))

import decky  # noqa: E402
from gcm_launcher_backend.service import Service  # noqa: E402


class Plugin:
    def __init__(self) -> None:
        self.service: Service | None = None

    async def _main(self) -> None:
        self.service = Service.create()
        decky.logger.info("GCM Launcher ready (home=%s)", self.service.paths.home)

    async def _unload(self) -> None:
        decky.logger.info("GCM Launcher unloading")

    async def _uninstall(self) -> None:
        decky.logger.info("GCM Launcher uninstall")

    def _require_service(self) -> Service:
        if self.service is None:
            self.service = Service.create()
        return self.service

    def _log_error(self, method: str, exc: Exception) -> None:
        decky.logger.error(
            "GCM Launcher RPC %s failed: %s", method, exc, exc_info=True
        )

    async def status(self) -> dict:
        service = self._require_service()
        try:
            return await asyncio.to_thread(service.status)
        except Exception as exc:  # noqa: BLE001
            self._log_error("status", exc)
            return {
                "installed": False,
                "version": "",
                "latest": None,
                "latest_error": "",
                "shortcut": False,
                "shortcut_appid": None,
                "proton_options": [],
                "proton_path": "",
                "trainer_dir": "",
                "log_file": "",
                "home": "",
                "backend_error": str(exc),
            }

    async def check_latest(self) -> dict:
        service = self._require_service()
        try:
            return await asyncio.to_thread(service.latest_status)
        except Exception as exc:  # noqa: BLE001
            self._log_error("check_latest", exc)
            return {"error": str(exc)}

    async def install(self) -> dict:
        service = self._require_service()
        try:
            return await asyncio.to_thread(service.install)
        except Exception as exc:  # noqa: BLE001
            self._log_error("install", exc)
            raise

    async def update(self) -> dict:
        service = self._require_service()
        try:
            return await asyncio.to_thread(service.install)
        except Exception as exc:  # noqa: BLE001
            self._log_error("update", exc)
            raise

    async def set_proton(self, proton_root: str) -> dict:
        service = self._require_service()
        try:
            return await asyncio.to_thread(service.set_proton, proton_root)
        except Exception as exc:  # noqa: BLE001
            self._log_error("set_proton", exc)
            raise

    async def ensure_shortcut(self) -> dict:
        service = self._require_service()
        try:
            return await asyncio.to_thread(service.ensure_shortcut)
        except Exception as exc:  # noqa: BLE001
            self._log_error("ensure_shortcut", exc)
            raise

    async def remove_shortcut(self) -> dict:
        service = self._require_service()
        try:
            return await asyncio.to_thread(service.remove_shortcut)
        except Exception as exc:  # noqa: BLE001
            self._log_error("remove_shortcut", exc)
            raise

    async def sync_trainers(self) -> list:
        service = self._require_service()
        try:
            return await asyncio.to_thread(service.sync_trainers)
        except Exception as exc:  # noqa: BLE001
            self._log_error("sync_trainers", exc)
            raise

    async def get_trainer_path(self) -> str:
        return str(self._require_service().paths.trainer_dir)

    async def get_logs(self) -> str:
        return str(self._require_service().paths.log_file)
