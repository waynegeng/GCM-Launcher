from __future__ import annotations

import json
import threading
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from gcm_launcher_backend.releases import ReleaseError, download_asset, fetch_latest


def _make_server(tmp_path: Path):
    zip_path = tmp_path / "portable.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("Game Cheats Manager.exe", b"MZ")
    payload = zip_path.read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/latest"):
                body = json.dumps(
                    {
                        "tag_name": "v2.5.0",
                        "assets": [
                            {
                                "name": "Game.Cheats.Manager.Portable.2.5.0.zip",
                                "size": len(payload),
                                "browser_download_url": f"http://127.0.0.1:{port}/portable.zip",
                            }
                        ],
                    }
                ).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)
            elif self.path == "/portable.zip":
                self.send_response(200)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_fetch_and_download_latest(tmp_path: Path) -> None:
    server, thread = _make_server(tmp_path)
    try:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        asset = fetch_latest(api_url=f"{base}/latest")
        assert asset.tag == "v2.5.0"
        assert "Portable" in asset.name
        target = download_asset(asset, tmp_path / "downloads")
        assert target.exists()
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_no_portable_asset_raises(tmp_path: Path) -> None:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = json.dumps({"tag_name": "v1", "assets": []}).encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        try:
            fetch_latest(api_url=f"http://127.0.0.1:{port}/latest")
        except ReleaseError as exc:
            assert "no Portable" in str(exc)
        else:
            raise AssertionError("expected ReleaseError")
    finally:
        server.shutdown()
        thread.join(timeout=5)
