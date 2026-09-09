from __future__ import annotations

from gcm_launcher_backend.proton import default_proton, discover_proton_options


def _install_ge(root, name: str = "GE-Proton11-6") -> None:
    ge = root / "compatibilitytools.d" / name
    ge.mkdir(parents=True)
    (ge / "proton").write_text("#!/bin/sh\n", encoding="utf-8")
    (ge / "compatibilitytool.vdf").write_text(
        '"compatibilitytools"\n{\n\t"compat_tools"\n\t{\n'
        '\t\t"GE-Proton11-6-x86_64"\n\t\t{\n\t\t\t"install_path" "."\n'
        '\t\t\t"display_name" "GE-Proton11-6"\n\t\t}\n\t}\n}\n',
        encoding="utf-8",
    )


def test_detects_ge_as_default(fake_steam_root) -> None:
    _install_ge(fake_steam_root)
    options = discover_proton_options(fake_steam_root)
    assert options
    assert default_proton(fake_steam_root).is_ge
    assert options[0].name == "GE-Proton11-6-x86_64"
