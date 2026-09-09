"""Fetch GCM Portable release metadata/downloads from GitHub Releases."""

from __future__ import annotations

import json
import os
import re
import shutil
import ssl
import tempfile
import urllib.request
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from urllib.parse import quote, unquote

RELEASES_API = "https://api.github.com/repos/dyang886/Game-Cheats-Manager/releases/latest"
GITHUB_RELEASES_PAGE = "https://github.com/dyang886/Game-Cheats-Manager/releases/latest"
GITHUB_HEADERS = {"User-Agent": "gcm-launcher-decky/0.1"}


def _ssl_context() -> ssl.SSLContext:
    """Create a TLS context using certifi's CA bundle when available."""
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        return ssl.create_default_context()


class ReleaseError(RuntimeError):
    """Raised when the latest release cannot be resolved or downloaded."""


@dataclass(frozen=True)
class ReleaseAsset:
    tag: str
    name: str
    url: str
    size: int


def _latest_from_release_page(timeout: int = 30) -> ReleaseAsset:
    request = urllib.request.Request(GITHUB_RELEASES_PAGE, headers=GITHUB_HEADERS)
    try:
        with urllib.request.urlopen(
            request, timeout=timeout, context=_ssl_context()
        ) as response:
            final_url = response.geturl()
    except Exception as exc:  # noqa: BLE001
        raise ReleaseError(f"could not fetch latest release page: {exc}") from exc
    tag_match = re.search(r"/releases/tag/([^/?\"']+)", final_url)
    tag = unquote(tag_match.group(1)) if tag_match else "unknown"
    expanded_url = (
        "https://github.com/dyang886/Game-Cheats-Manager/releases/expanded_assets/"
        + quote(tag, safe="")
    )
    expanded_request = urllib.request.Request(expanded_url, headers=GITHUB_HEADERS)
    try:
        with urllib.request.urlopen(
            expanded_request, timeout=timeout, context=_ssl_context()
        ) as response:
            fragment = response.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        raise ReleaseError(f"could not load release assets for {tag}: {exc}") from exc
    links = re.findall(r'href="([^"]*?/releases/download/[^"]+)"', fragment)
    candidates = []
    for href in links:
        name = unquote(Path(href).name)
        if "Portable" in name and name.lower().endswith(".zip"):
            candidates.append((name, unescape(href)))
    if not candidates:
        raise ReleaseError(f"no Portable zip asset found on release page {tag}")
    # Prefer the latest (first) matching asset on the page.
    name, href = candidates[0]
    url = href if href.startswith("http") else f"https://github.com{href}"
    return ReleaseAsset(tag=tag, name=name, url=url, size=0)


def fetch_latest(
    api_url: str = RELEASES_API,
    timeout: int = 30,
    allow_page_fallback: bool = True,
) -> ReleaseAsset:
    request = urllib.request.Request(api_url, headers=GITHUB_HEADERS)
    try:
        with urllib.request.urlopen(
            request, timeout=timeout, context=_ssl_context()
        ) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        if not allow_page_fallback or api_url != RELEASES_API:
            raise ReleaseError(f"could not fetch latest release: {exc}") from exc
        return _latest_from_release_page(timeout=timeout)

    tag = str(payload.get("tag_name") or "unknown")
    assets = payload.get("assets") or []
    for asset in assets:
        name = str(asset.get("name") or "")
        if "Portable" in name and name.lower().endswith(".zip"):
            return ReleaseAsset(
                tag=tag,
                name=name,
                url=str(asset.get("browser_download_url") or ""),
                size=int(asset.get("size") or 0),
            )
    if not allow_page_fallback or api_url != RELEASES_API:
        raise ReleaseError(f"no Portable zip asset found in release {tag}")
    return _latest_from_release_page(timeout=timeout)


def download_asset(asset: ReleaseAsset, destination: Path, chunk_size: int = 128 * 1024) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / asset.name
    request = urllib.request.Request(asset.url, headers=GITHUB_HEADERS)
    fd, raw_temp = tempfile.mkstemp(prefix=f".{asset.name}.", suffix=".part", dir=destination)
    os.close(fd)
    temp_path = Path(raw_temp)
    try:
        with urllib.request.urlopen(
            request, timeout=120, context=_ssl_context()
        ) as response, temp_path.open("wb") as out:
            shutil.copyfileobj(response, out, length=chunk_size)
        temp_path.replace(target)
        return target
    except Exception as exc:  # noqa: BLE001
        temp_path.unlink(missing_ok=True)
        raise ReleaseError(f"download failed for {asset.name}: {exc}") from exc
