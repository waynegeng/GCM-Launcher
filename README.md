# GCM Launcher (Decky Plugin)

GCM Launcher installs the **official Windows Game Cheats Manager Portable**
build into user space and creates a Steam non-Steam shortcut that launches it
through Proton. Trainers are downloaded inside GCM itself and launched
per-game with CheatDeck.

The plugin deliberately does not reverse-engineer GCM, call its private data
service, or bundle a native Linux implementation.

## Layout

```text
gcm-launcher/
├── main.py                 # Decky backend entry point
├── plugin.json             # Decky metadata
├── py_modules/
│   ├── vdf/                # vendored ValvePython/vdf (MIT)
│   └── gcm_launcher_backend/
│       ├── service.py      # backend facade
│       ├── installer.py    # Portable zip install/update
│       ├── shortcuts.py    # shortcuts.vdf management
│       ├── launcher.py     # Proton wrapper generation
│       ├── proton.py       # Proton discovery
│       ├── releases.py     # GitHub release API
│       └── paths.py        # user-space layout
├── src/index.tsx           # React UI
├── package.json
└── rollup.config.js
```

Runtime data lives in `~/.local/share/gcm-launcher/`:

* `gcm/` — official GCM files (`gcm/Game Cheats Manager.exe`)
* `prefix/` — dedicated Proton prefix
* `bin/gcm-launcher` — wrapper used by the Steam shortcut
* `config.json`, `downloads/`, `logs/`, `backups/`

## Development

Backend tests:

```bash
cd ..
.venv/bin/python -m pytest gcm-launcher/tests -q
```

Frontend build (requires pnpm):

```bash
cd gcm-launcher
pnpm install
pnpm run build
```

Manual Decky install for development:

```bash
mkdir -p ~/homebrew/plugins/GCM-Launcher
cp -r gcm-launcher/* ~/homebrew/plugins/GCM-Launcher/
```

The built plugin zip layout (for distribution) is:

```text
dist/index.js
main.py
py_modules/
plugin.json
package.json
```

## Usage

1. Open the plugin and click **Install official GCM** (downloads the latest
   Portable zip from GitHub Releases).
2. Pick a Proton option (GE-Proton is detected first).
3. Click **Create Steam shortcut**, then restart Steam/Gaming Mode once.
4. Launch **Game Cheats Manager** from the Steam library.
5. Download trainers inside GCM, then in CheatDeck point a game at the
   Trainer.exe under `~/.local/share/gcm-launcher/prefix/.../GCM Trainers/`.

## License

Plugin code: GPL-3.0-or-later (same as this repository). Vendored
`py_modules/vdf` is MIT licensed (see `py_modules/VDF-LICENSE`). GCM itself is
downloaded from upstream at runtime and is not distributed by this plugin.
