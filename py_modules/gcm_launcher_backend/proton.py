"""Discover Proton compatibility tools installed for Steam."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .steam import find_steam_root


@dataclass(frozen=True)
class ProtonOption:
    root: Path
    name: str
    display: str

    @property
    def proton_script(self) -> Path:
        return self.root / "proton"

    @property
    def is_ge(self) -> bool:
        return "ge-proton" in self.display.lower() or self.name.lower().startswith("ge-")


def _scan_proton_dirs(root: Path) -> list[ProtonOption]:
    options: list[ProtonOption] = []
    scan_roots = [
        root / "compatibilitytools.d",
        root / "steamapps" / "common",
    ]
    seen: set[Path] = set()
    for scan_root in scan_roots:
        if not scan_root.is_dir():
            continue
        for candidate in sorted(scan_root.iterdir()):
            if not candidate.is_dir() or candidate in seen:
                continue
            if not (candidate / "proton").is_file():
                continue
            seen.add(candidate)
            display = candidate.name
            name = candidate.name
            manifest = candidate / "compatibilitytool.vdf"
            if manifest.exists():
                try:
                    import vdf

                    data = vdf.load(manifest.open(encoding="utf-8", errors="replace"))
                    tools = (
                        data.get("compatibilitytools", {}).get("compat_tools", {})
                        if isinstance(data, dict)
                        else {}
                    )
                    if tools and isinstance(tools, dict):
                        name = next(iter(tools))
                        display = (
                            tools[name].get("display_name", name)
                            if isinstance(tools[name], dict)
                            else name
                        )
                except Exception:  # noqa: BLE001
                    pass
            options.append(ProtonOption(root=candidate, name=name, display=display))
    return options


def discover_proton_options(steam_root: Path | str | None = None) -> list[ProtonOption]:
    root = Path(steam_root) if steam_root else find_steam_root()
    if root is None:
        return []
    options = _scan_proton_dirs(root)
    ge = [option for option in options if option.is_ge]
    if ge:
        ge.sort(key=lambda item: item.display, reverse=True)
        return ge + [option for option in options if not option.is_ge]
    options.sort(key=lambda item: item.display)
    return options


def default_proton(steam_root: Path | str | None = None) -> ProtonOption | None:
    options = discover_proton_options(steam_root)
    return options[0] if options else None
