# GCM 启动器（Decky 插件）

GCM 启动器将**官方 Windows 版 Game Cheats Manager Portable（便携版）**安装到用户目录，并在 Steam 中创建一个非 Steam 游戏快捷方式，通过 Proton 启动 GCM。修改器在 GCM 内下载，再通过 CheatDeck 随对应的游戏启动。

本插件不对 GCM 进行逆向工程，不调用其私有数据服务，也不附带原生 Linux 实现。

## 目录结构

```text
gcm-launcher/
├── main.py                 # Decky 后端入口
├── plugin.json             # Decky 插件信息
├── py_modules/
│   ├── vdf/                # 随插件附带的 ValvePython/vdf（MIT）
│   └── gcm_launcher_backend/
│       ├── service.py      # 后端服务接口
│       ├── installer.py    # 便携版 ZIP 的安装与更新
│       ├── shortcuts.py    # shortcuts.vdf 管理
│       ├── launcher.py     # Proton 启动脚本生成
│       ├── proton.py       # 查找已安装的 Proton
│       ├── releases.py     # GitHub Release 接口
│       └── paths.py        # 用户目录中的数据路径
├── src/index.tsx           # React 页面
├── package.json
└── rollup.config.js
```

运行数据保存在 `~/.local/share/gcm-launcher/`：

* `gcm/` — 官方 GCM 文件（`gcm/Game Cheats Manager.exe`）
* `prefix/` — GCM 专用的 Proton 运行目录
* `bin/gcm-launcher` — Steam 快捷方式使用的启动脚本
* `config.json`、`downloads/`、`logs/`、`backups/`

## 开发

后端测试：

```bash
cd ..
.venv/bin/python -m pytest gcm-launcher/tests -q
```

生成页面（需要 pnpm）：

```bash
cd gcm-launcher
pnpm install
pnpm run build
```

开发环境中手动安装到 Decky：

```bash
mkdir -p ~/homebrew/plugins/GCM-Launcher
cp -r gcm-launcher/* ~/homebrew/plugins/GCM-Launcher/
```

完整插件 ZIP（用于分发）的目录结构：

```text
dist/index.js
main.py
py_modules/
plugin.json
package.json
```

## 使用方法

1. 打开插件，点击**安装官方 GCM**，从 GitHub Releases 下载最新的便携版 ZIP。
2. 选择一个 Proton 版本（优先检测 GE-Proton）。
3. 点击**创建 Steam 快捷方式**，然后重启一次 Steam 或游戏模式。
4. 在 Steam 游戏库中启动 **Game Cheats Manager**。
5. 在 GCM 内下载修改器，然后在 CheatDeck 中为游戏选择 `~/.local/share/gcm-launcher/prefix/.../GCM Trainers/` 下的 Trainer.exe。

## 许可证

插件代码采用 GPL-3.0-or-later，与本仓库一致。随插件附带的 `py_modules/vdf` 采用 MIT 许可证（见 `py_modules/VDF-LICENSE`）。GCM 本体在使用时从上游下载，不随本插件分发。
