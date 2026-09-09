from __future__ import annotations

from gcm_launcher_backend.config import Config
from gcm_launcher_backend.paths import Paths


def test_paths_layout(home) -> None:
    paths = Paths.create(home)
    paths.ensure()
    assert paths.gcm_dir.is_dir()
    assert paths.trainer_dir.name == "GCM Trainers"
    assert paths.launcher_path.name == "gcm-launcher"


def test_config_roundtrip(home) -> None:
    config = Config(home / "config.json")
    config.set("gcm_version", "v2.5.0")
    config.set("shortcut_appid", -55725736)
    config.save()
    loaded = Config(home / "config.json")
    assert loaded.get("gcm_version") == "v2.5.0"
    assert loaded.get("shortcut_appid") == -55725736
