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
};

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
      setStatus(await fetchStatus());
    } catch (error) {
      toaster.toast({ title: "GCM Launcher", body: String(error) });
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const run = async (label: string, operation: () => Promise<unknown>) => {
    setBusy(true);
    try {
      await operation();
      toaster.toast({ title: "GCM Launcher", body: label });
    } catch (error) {
      toaster.toast({ title: "GCM Launcher", body: String(error) });
    } finally {
      setBusy(false);
      await refresh();
    }
  };

  const installed = status?.installed ?? false;
  const shortcut = status?.shortcut ?? false;
  const hasProton = (status?.proton_options.length ?? 0) > 0;

  return (
    <PanelSection title="GCM Launcher">
      <PanelSectionRow>
        <div style={{ color: "#b8b8b8", marginBottom: "8px" }}>
          {status
            ? installed
              ? `Installed: ${status.version || "unknown"}`
              : "Official GCM is not installed yet."
            : busy
              ? "Loading status…"
              : "Status unavailable."}
        </div>
      </PanelSectionRow>

      {!installed && (
        <PanelSectionRow>
          <ButtonItem
            layout="below"
            disabled={busy || !hasProton}
            onClick={() => run("GCM installed", () => installGCM())}
          >
            <FaDownload /> Install official GCM
          </ButtonItem>
        </PanelSectionRow>
      )}

      {installed && (
        <>
          <PanelSectionRow>
            <ButtonItem layout="below" disabled={busy} onClick={() => run("GCM updated", () => updateGCM())}>
              <FaSyncAlt /> Check for updates / update
            </ButtonItem>
          </PanelSectionRow>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              disabled={busy || shortcut}
              onClick={() =>
                run("Steam shortcut created. Restart Steam to see it.", () => createShortcut())
              }
            >
              {shortcut ? "Steam shortcut exists" : "Create Steam shortcut"}
            </ButtonItem>
          </PanelSectionRow>
          <PanelSectionRow>
            <ButtonItem layout="below" disabled={busy || !shortcut} onClick={() => run("Shortcut removed", () => deleteShortcut())}>
              <FaTrash /> Remove Steam shortcut
            </ButtonItem>
          </PanelSectionRow>
        </>
      )}

      <PanelSection title="Proton">
        {status?.proton_options.map((option) => (
          <PanelSectionRow key={option.root}>
            <ButtonItem
              layout="below"
              disabled={busy || status.proton_path === option.root}
              onClick={() =>
                run(`Proton set to ${option.display}`, () => chooseProton(option.root))
              }
            >
              {status.proton_path === option.root ? "✓ " : ""}
              {option.display}
            </ButtonItem>
          </PanelSectionRow>
        ))}
        {!hasProton && (
          <PanelSectionRow>
            <div style={{ color: "#b8b8b8" }}>No Proton installation detected.</div>
          </PanelSectionRow>
        )}
      </PanelSection>

      {installed && status && (
        <PanelSection title="Trainer side-loading">
          <PanelSectionRow>
            <div style={{ color: "#b8b8b8", overflowWrap: "anywhere" }}>{status.trainer_dir}</div>
          </PanelSectionRow>
          <PanelSectionRow>
            <div style={{ color: "#b8b8b8" }}>
              Copy trainers to {status.export_dir} with clean paths, then point CheatDeck at the .exe there.
            </div>
          </PanelSectionRow>
          <PanelSectionRow>
            <ButtonItem
              layout="below"
              disabled={busy}
              onClick={() => run("Trainers synced", () => syncTrainers())}
            >
              <FaDownload /> Sync trainers to ~/GCM-Trainers
            </ButtonItem>
          </PanelSectionRow>
        </PanelSection>
      )}

      <PanelSectionRow>
        <ButtonItem layout="below" disabled={busy} onClick={() => refresh()}>
          <FaGamepad /> Refresh status
        </ButtonItem>
      </PanelSectionRow>
    </PanelSection>
  );
}

export default definePlugin(() => {
  console.log("GCM Launcher frontend loaded");
  return {
    name: "GCM Launcher",
    titleView: <div className={staticClasses.Title}>GCM Launcher</div>,
    content: <Content />,
    icon: <FaGamepad />,
    onDismount() {
      console.log("GCM Launcher frontend unloading");
    },
  };
});
