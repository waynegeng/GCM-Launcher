import { ButtonItem, PanelSection, PanelSectionRow, staticClasses } from "@decky/ui";
import { callable, definePlugin, toaster } from "@decky/api";
import { useEffect, useState } from "react";
import { FaGamepad, FaDownload, FaSyncAlt, FaTrash } from "react-icons/fa";

type ProtonOption = {
  root: string;
  name: string;
  display: string;
};

type Status = {
  installed: boolean;
  version: string;
  latest: { tag: string; name: string } | null;
  latest_error: string;
  shortcut: boolean;
  shortcut_appid: number | null;
  proton_options: ProtonOption[];
  proton_path: string;
  trainer_dir: string;
  export_dir: string;
  log_file: string;
  home: string;
  backend_error?: string;
};

const title = "GCM 启动器";
const errorMessage = (summary: string, error: unknown) =>
  `${summary}\n原始错误：${String(error)}`;

const fetchStatus = callable<[], Status>("status");
const installGCM = callable<[], { version: string; exe: string }>("install");
const updateGCM = callable<[], { version: string; exe: string }>("update");
const chooseProton = callable<[root: string], { proton_path: string }>("set_proton");
const createShortcut = callable<[], { appid: number; shortcuts_path: string; restart_required: boolean }>(
  "ensure_shortcut"
);
const deleteShortcut = callable<[], { removed: boolean }>("remove_shortcut");
const syncTrainers = callable<[], { game: string; trainer: string }[]>("sync_trainers");

function Content() {
  const [status, setStatus] = useState<Status | null>(null);
  const [busy, setBusy] = useState<boolean>(false);

  const refresh = async () => {
    setBusy(true);
    try {
      const result = await fetchStatus();
      if (result.backend_error) {
        throw new Error(result.backend_error);
      }
      setStatus(result);
    } catch (error) {
      toaster.toast({ title, body: errorMessage("获取状态失败。", error) });
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const run = async (
    successMessage: string,
    failureMessage: string,
    operation: () => Promise<unknown>
  ) => {
    setBusy(true);
    try {
      await operation();
      toaster.toast({ title, body: successMessage });
    } catch (error) {
      toaster.toast({ title, body: errorMessage(failureMessage, error) });
    } finally {
      setBusy(false);
      await refresh();
    }
  };

  const installed = status?.installed ?? false;
  const shortcut = status?.shortcut ?? false;
  const hasProton = (status?.proton_options.length ?? 0) > 0;

  return (
    <PanelSection title={title}>
      <PanelSectionRow>
        <div style={{ color: "#b8b8b8", marginBottom: "8px" }}>
          {status
            ? installed
              ? `已安装：${status.version || "版本未知"}`
              : "尚未安装官方 GCM。"
            : busy
              ? "正在获取状态…"
              : "暂时无法获取状态。"}
        </div>
      </PanelSectionRow>

      {!installed && (
        <PanelSectionRow>
          <ButtonItem
            layout="below"
            disabled={busy || !hasProton}
            onClick={() => run("GCM 安装完成。", "安装 GCM 失败。", () => installGCM())}
          >
            <FaDownload /> 安装官方 GCM
          </ButtonItem>
        </PanelSectionRow>
      )}

      {installed && (
        <>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              disabled={busy}
              onClick={() => run("GCM 更新完成。", "检查并更新 GCM 失败。", () => updateGCM())}
            >
              <FaSyncAlt /> 检查并更新
            </ButtonItem>
          </PanelSectionRow>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              disabled={busy || shortcut}
              onClick={() =>
                run(
                  "Steam 快捷方式已创建。重启 Steam 后即可在游戏库中看到。",
                  "创建 Steam 快捷方式失败。",
                  () => createShortcut()
                )
              }
            >
              {shortcut ? "Steam 快捷方式已存在" : "创建 Steam 快捷方式"}
            </ButtonItem>
          </PanelSectionRow>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              disabled={busy || !shortcut}
              onClick={() =>
                run("Steam 快捷方式已移除。", "移除 Steam 快捷方式失败。", () => deleteShortcut())
              }
            >
              <FaTrash /> 移除 Steam 快捷方式
            </ButtonItem>
          </PanelSectionRow>
        </>
      )}

      <PanelSection title="Proton 版本">
        {status?.proton_options.map((option) => (
          <PanelSectionRow key={option.root}>
            <ButtonItem
              layout="below"
              disabled={busy || status.proton_path === option.root}
              onClick={() =>
                run(
                  `已选择 ${option.display}。`,
                  "选择 Proton 失败。",
                  () => chooseProton(option.root)
                )
              }
            >
              {status.proton_path === option.root ? "✓ " : ""}
              {option.display}
            </ButtonItem>
          </PanelSectionRow>
        ))}
        {!hasProton && (
          <PanelSectionRow>
            <div style={{ color: "#b8b8b8" }}>未检测到已安装的 Proton。</div>
          </PanelSectionRow>
        )}
      </PanelSection>

      {installed && status && (
        <PanelSection title="修改器同步">
          <PanelSectionRow>
            <div style={{ color: "#b8b8b8" }}>
              <div>修改器原始目录</div>
              <div style={{ overflowWrap: "anywhere" }}>{status.trainer_dir}</div>
            </div>
          </PanelSectionRow>
          <PanelSectionRow>
            <div style={{ color: "#b8b8b8", overflowWrap: "anywhere" }}>
              点击下方按钮，将修改器同步到 {status.export_dir}，再在 CheatDeck 中选择对应的
              Trainer.exe。同步后的游戏目录名不含中文或单引号，便于 CheatDeck 使用。
            </div>
          </PanelSectionRow>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              disabled={busy}
              onClick={() => run("修改器同步完成。", "同步修改器失败。", () => syncTrainers())}
            >
              <FaDownload /> 同步修改器
            </ButtonItem>
          </PanelSectionRow>
        </PanelSection>
      )}

      <PanelSectionRow>
        <ButtonItem layout="below" disabled={busy} onClick={() => refresh()}>
          <FaGamepad /> 刷新状态
        </ButtonItem>
      </PanelSectionRow>
    </PanelSection>
  );
}

export default definePlugin(() => {
  console.log("GCM Launcher frontend loaded");
  return {
    name: "GCM Launcher",
    titleView: <div className={staticClasses.Title}>{title}</div>,
    content: <Content />,
    icon: <FaGamepad />,
    onDismount() {
      console.log("GCM Launcher frontend unloading");
    },
  };
});
