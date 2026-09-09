from __future__ import annotations

from pathlib import Path

from gcm_launcher_backend.paths import Paths


def test_service_status_without_gcm(service, fake_steam_root) -> None:
    status = service.status(include_latest=False)
    assert status["installed"] is False
    assert status["shortcut"] is False
    assert "GCM Trainers" in status["trainer_dir"]


def test_service_ensure_shortcut_and_remove(service, fake_steam_root, monkeypatch) -> None:
    proton_root = fake_steam_root / "compatibilitytools.d" / "GE-Proton11-6"
    proton_root.mkdir(parents=True)
    (proton_root / "proton").write_text("#!/bin/sh\n", encoding="utf-8")
    (proton_root / "compatibilitytool.vdf").write_text(
        '"compatibilitytools"\n{\n\t"compat_tools"\n\t{\n\t\t"GE-Proton11-6-x86_64"'
        '\n\t\t{\n\t\t\t"display_name" "GE-Proton11-6"\n\t\t}\n\t}\n}\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("GCM_LAUNCHER_STEAM_ROOT", str(fake_steam_root))
    result = service.set_proton(str(proton_root))
    assert result["proton_path"] == str(proton_root)
    shortcut = service.ensure_shortcut()
    assert shortcut["restart_required"] is True
    assert service.status(include_latest=False)["shortcut"] is True
    assert service.remove_shortcut()["removed"] is True


def test_launcher_script_points_to_gcm(service, fake_steam_root, monkeypatch) -> None:
    from gcm_launcher_backend.launcher import write_launcher

    monkeypatch.setenv("GCM_LAUNCHER_STEAM_ROOT", str(fake_steam_root))
    paths = Paths.create(service.paths.home)
    paths.ensure()
    launcher = write_launcher(paths, str(fake_steam_root / "proton"), str(fake_steam_root))
    content = launcher.read_text(encoding="utf-8")
    assert "Game Cheats Manager.exe" in content
    assert launcher.stat().st_mode & 0o111


def test_sync_trainers_creates_clean_export_path(service) -> None:
    source = (
        service.paths.trainer_dir
        / "[风灵]《漫威蜘蛛侠：重制版》修改器"
    )
    source.mkdir(parents=True)
    (source / "Marvel's Spider-Man Remastered Trainer.exe").write_bytes(b"MZ")
    (source / "gcm_info.json").write_text(
        '{"game_name": "Marvel\'s Spider-Man Remastered", "origin": "fling_main", '
        '"version": "2023.06.22"}',
        encoding="utf-8",
    )
    exported = service.sync_trainers()
    assert len(exported) == 1
    folder = Path(exported[0]["folder"])
    assert folder.parent == service.paths.export_dir
    assert folder.name == "Marvels-Spider-Man-Remastered"
    assert (folder / "Trainer.exe").is_file()
