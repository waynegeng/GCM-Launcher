#!/usr/bin/env python3
"""Host-side CLI for the GCM Launcher backend (outside Decky)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY_MODULES = ROOT / "py_modules"
if str(PY_MODULES) not in sys.path:
    sys.path.insert(0, str(PY_MODULES))

from gcm_launcher_backend.service import Service  # noqa: E402


def _print(payload) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


def main() -> int:
    parser = argparse.ArgumentParser(prog="gcm_launcher_cli")
    parser.add_argument("--home", default=None, help="override runtime home")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("install")
    sub.add_parser("ensure-shortcut")
    sub.add_parser("remove-shortcut")
    proton_parser = sub.add_parser("set-proton")
    proton_parser.add_argument("proton_root")
    args = parser.parse_args()

    service = Service.create(args.home)
    if args.command == "status":
        _print(service.status())
    elif args.command == "install":
        _print(service.install())
    elif args.command == "ensure-shortcut":
        _print(service.ensure_shortcut())
    elif args.command == "remove-shortcut":
        _print(service.remove_shortcut())
    elif args.command == "set-proton":
        _print(service.set_proton(args.proton_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
