const manifest = {"name":"GCM-Launcher"};
const API_VERSION = 2;
const internalAPIConnection = window.__DECKY_SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED_deckyLoaderAPIInit;
if (!internalAPIConnection) {
    throw new Error('[@decky/api]: Failed to connect to the loader as as the loader API was not initialized. This is likely a bug in Decky Loader.');
}
let api;
try {
    api = internalAPIConnection.connect(API_VERSION, manifest.name);
}
catch {
    api = internalAPIConnection.connect(1, manifest.name);
    console.warn(`[@decky/api] Requested API version ${API_VERSION} but the running loader only supports version 1. Some features may not work.`);
}
if (api._version != API_VERSION) {
    console.warn(`[@decky/api] Requested API version ${API_VERSION} but the running loader only supports version ${api._version}. Some features may not work.`);
}
const callable = api.callable;
const toaster = api.toaster;
const definePlugin = (fn) => {
    return (...args) => {
        return fn(...args);
    };
};

var DefaultContext = {
  color: undefined,
  size: undefined,
  className: undefined,
  style: undefined,
  attr: undefined
};
var IconContext = SP_REACT.createContext && /*#__PURE__*/SP_REACT.createContext(DefaultContext);

var _excluded = ["attr", "size", "title"];
function _objectWithoutProperties(e, t) { if (null == e) return {}; var o, r, i = _objectWithoutPropertiesLoose(e, t); if (Object.getOwnPropertySymbols) { var n = Object.getOwnPropertySymbols(e); for (r = 0; r < n.length; r++) o = n[r], -1 === t.indexOf(o) && {}.propertyIsEnumerable.call(e, o) && (i[o] = e[o]); } return i; }
function _objectWithoutPropertiesLoose(r, e) { if (null == r) return {}; var t = {}; for (var n in r) if ({}.hasOwnProperty.call(r, n)) { if (-1 !== e.indexOf(n)) continue; t[n] = r[n]; } return t; }
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function ownKeys(e, r) { var t = Object.keys(e); if (Object.getOwnPropertySymbols) { var o = Object.getOwnPropertySymbols(e); r && (o = o.filter(function (r) { return Object.getOwnPropertyDescriptor(e, r).enumerable; })), t.push.apply(t, o); } return t; }
function _objectSpread(e) { for (var r = 1; r < arguments.length; r++) { var t = null != arguments[r] ? arguments[r] : {}; r % 2 ? ownKeys(Object(t), true).forEach(function (r) { _defineProperty(e, r, t[r]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function (r) { Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(t, r)); }); } return e; }
function _defineProperty(e, r, t) { return (r = _toPropertyKey(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: true, configurable: true, writable: true }) : e[r] = t, e; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == typeof i ? i : i + ""; }
function _toPrimitive(t, r) { if ("object" != typeof t || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r); if ("object" != typeof i) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === r ? String : Number)(t); }
function Tree2Element(tree) {
  return tree && tree.map((node, i) => /*#__PURE__*/SP_REACT.createElement(node.tag, _objectSpread({
    key: i
  }, node.attr), Tree2Element(node.child)));
}
function GenIcon(data) {
  return props => /*#__PURE__*/SP_REACT.createElement(IconBase, _extends({
    attr: _objectSpread({}, data.attr)
  }, props), Tree2Element(data.child));
}
function IconBase(props) {
  var elem = conf => {
    var attr = props.attr,
      size = props.size,
      title = props.title,
      svgProps = _objectWithoutProperties(props, _excluded);
    var computedSize = size || conf.size || "1em";
    var className;
    if (conf.className) className = conf.className;
    if (props.className) className = (className ? className + " " : "") + props.className;
    return /*#__PURE__*/SP_REACT.createElement("svg", _extends({
      stroke: "currentColor",
      fill: "currentColor",
      strokeWidth: "0"
    }, conf.attr, attr, svgProps, {
      className: className,
      style: _objectSpread(_objectSpread({
        color: props.color || conf.color
      }, conf.style), props.style),
      height: computedSize,
      width: computedSize,
      xmlns: "http://www.w3.org/2000/svg"
    }), title && /*#__PURE__*/SP_REACT.createElement("title", null, title), props.children);
  };
  return IconContext !== undefined ? /*#__PURE__*/SP_REACT.createElement(IconContext.Consumer, null, conf => elem(conf)) : elem(DefaultContext);
}

// THIS FILE IS AUTO GENERATED
function FaTrash (props) {
  return GenIcon({"attr":{"viewBox":"0 0 448 512"},"child":[{"tag":"path","attr":{"d":"M432 32H312l-9.4-18.7A24 24 0 0 0 281.1 0H166.8a23.72 23.72 0 0 0-21.4 13.3L136 32H16A16 16 0 0 0 0 48v32a16 16 0 0 0 16 16h416a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16zM53.2 467a48 48 0 0 0 47.9 45h245.8a48 48 0 0 0 47.9-45L416 128H32z"},"child":[]}]})(props);
}function FaSyncAlt (props) {
  return GenIcon({"attr":{"viewBox":"0 0 512 512"},"child":[{"tag":"path","attr":{"d":"M370.72 133.28C339.458 104.008 298.888 87.962 255.848 88c-77.458.068-144.328 53.178-162.791 126.85-1.344 5.363-6.122 9.15-11.651 9.15H24.103c-7.498 0-13.194-6.807-11.807-14.176C33.933 94.924 134.813 8 256 8c66.448 0 126.791 26.136 171.315 68.685L463.03 40.97C478.149 25.851 504 36.559 504 57.941V192c0 13.255-10.745 24-24 24H345.941c-21.382 0-32.09-25.851-16.971-40.971l41.75-41.749zM32 296h134.059c21.382 0 32.09 25.851 16.971 40.971l-41.75 41.75c31.262 29.273 71.835 45.319 114.876 45.28 77.418-.07 144.315-53.144 162.787-126.849 1.344-5.363 6.122-9.15 11.651-9.15h57.304c7.498 0 13.194 6.807 11.807 14.176C478.067 417.076 377.187 504 256 504c-66.448 0-126.791-26.136-171.315-68.685L48.97 471.03C33.851 486.149 8 475.441 8 454.059V320c0-13.255 10.745-24 24-24z"},"child":[]}]})(props);
}function FaGamepad (props) {
  return GenIcon({"attr":{"viewBox":"0 0 640 512"},"child":[{"tag":"path","attr":{"d":"M480.07 96H160a160 160 0 1 0 114.24 272h91.52A160 160 0 1 0 480.07 96zM248 268a12 12 0 0 1-12 12h-52v52a12 12 0 0 1-12 12h-24a12 12 0 0 1-12-12v-52H84a12 12 0 0 1-12-12v-24a12 12 0 0 1 12-12h52v-52a12 12 0 0 1 12-12h24a12 12 0 0 1 12 12v52h52a12 12 0 0 1 12 12zm216 76a40 40 0 1 1 40-40 40 40 0 0 1-40 40zm64-96a40 40 0 1 1 40-40 40 40 0 0 1-40 40z"},"child":[]}]})(props);
}function FaDownload (props) {
  return GenIcon({"attr":{"viewBox":"0 0 512 512"},"child":[{"tag":"path","attr":{"d":"M216 0h80c13.3 0 24 10.7 24 24v168h87.7c17.8 0 26.7 21.5 14.1 34.1L269.7 378.3c-7.5 7.5-19.8 7.5-27.3 0L90.1 226.1c-12.6-12.6-3.7-34.1 14.1-34.1H192V24c0-13.3 10.7-24 24-24zm296 376v112c0 13.3-10.7 24-24 24H24c-13.3 0-24-10.7-24-24V376c0-13.3 10.7-24 24-24h146.7l49 49c20.1 20.1 52.5 20.1 72.6 0l49-49H488c13.3 0 24 10.7 24 24zm-124 88c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20zm64 0c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20z"},"child":[]}]})(props);
}

const title = "GCM 启动器";
const errorMessage = (summary, error) => `${summary}\n原始错误：${String(error)}`;
const fetchStatus = callable("status");
const installGCM = callable("install");
const updateGCM = callable("update");
const chooseProton = callable("set_proton");
const createShortcut = callable("ensure_shortcut");
const deleteShortcut = callable("remove_shortcut");
const syncTrainers = callable("sync_trainers");
function Content() {
    const [status, setStatus] = SP_REACT.useState(null);
    const [busy, setBusy] = SP_REACT.useState(false);
    const refresh = async () => {
        setBusy(true);
        try {
            const result = await fetchStatus();
            if (result.backend_error) {
                throw new Error(result.backend_error);
            }
            setStatus(result);
        }
        catch (error) {
            toaster.toast({ title, body: errorMessage("获取状态失败。", error) });
        }
        finally {
            setBusy(false);
        }
    };
    SP_REACT.useEffect(() => {
        refresh();
    }, []);
    const run = async (successMessage, failureMessage, operation) => {
        setBusy(true);
        try {
            await operation();
            toaster.toast({ title, body: successMessage });
        }
        catch (error) {
            toaster.toast({ title, body: errorMessage(failureMessage, error) });
        }
        finally {
            setBusy(false);
            await refresh();
        }
    };
    const installed = status?.installed ?? false;
    const shortcut = status?.shortcut ?? false;
    const hasProton = (status?.proton_options.length ?? 0) > 0;
    return (SP_JSX.jsxs(DFL.PanelSection, { title: title, children: [SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsx("div", { style: { color: "#b8b8b8", marginBottom: "8px" }, children: status
                        ? installed
                            ? `已安装：${status.version || "版本未知"}`
                            : "尚未安装官方 GCM。"
                        : busy
                            ? "正在获取状态…"
                            : "暂时无法获取状态。" }) }), !installed && (SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsxs(DFL.ButtonItem, { layout: "below", disabled: busy || !hasProton, onClick: () => run("GCM 安装完成。", "安装 GCM 失败。", () => installGCM()), children: [SP_JSX.jsx(FaDownload, {}), " \u5B89\u88C5\u5B98\u65B9 GCM"] }) })), installed && (SP_JSX.jsxs(SP_JSX.Fragment, { children: [SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsxs(DFL.ButtonItem, { layout: "below", disabled: busy, onClick: () => run("GCM 更新完成。", "检查并更新 GCM 失败。", () => updateGCM()), children: [SP_JSX.jsx(FaSyncAlt, {}), " \u68C0\u67E5\u5E76\u66F4\u65B0"] }) }), SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsx(DFL.ButtonItem, { layout: "below", disabled: busy || shortcut, onClick: () => run("Steam 快捷方式已创建。重启 Steam 后即可在游戏库中看到。", "创建 Steam 快捷方式失败。", () => createShortcut()), children: shortcut ? "Steam 快捷方式已存在" : "创建 Steam 快捷方式" }) }), SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsxs(DFL.ButtonItem, { layout: "below", disabled: busy || !shortcut, onClick: () => run("Steam 快捷方式已移除。", "移除 Steam 快捷方式失败。", () => deleteShortcut()), children: [SP_JSX.jsx(FaTrash, {}), " \u79FB\u9664 Steam \u5FEB\u6377\u65B9\u5F0F"] }) })] })), SP_JSX.jsxs(DFL.PanelSection, { title: "Proton \u7248\u672C", children: [status?.proton_options.map((option) => (SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsxs(DFL.ButtonItem, { layout: "below", disabled: busy || status.proton_path === option.root, onClick: () => run(`已选择 ${option.display}。`, "选择 Proton 失败。", () => chooseProton(option.root)), children: [status.proton_path === option.root ? "✓ " : "", option.display] }) }, option.root))), !hasProton && (SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsx("div", { style: { color: "#b8b8b8" }, children: "\u672A\u68C0\u6D4B\u5230\u5DF2\u5B89\u88C5\u7684 Proton\u3002" }) }))] }), installed && status && (SP_JSX.jsxs(DFL.PanelSection, { title: "\u4FEE\u6539\u5668\u540C\u6B65", children: [SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsxs("div", { style: { color: "#b8b8b8" }, children: [SP_JSX.jsx("div", { children: "\u4FEE\u6539\u5668\u539F\u59CB\u76EE\u5F55" }), SP_JSX.jsx("div", { style: { overflowWrap: "anywhere" }, children: status.trainer_dir })] }) }), SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsxs("div", { style: { color: "#b8b8b8", overflowWrap: "anywhere" }, children: ["\u70B9\u51FB\u4E0B\u65B9\u6309\u94AE\uFF0C\u5C06\u4FEE\u6539\u5668\u540C\u6B65\u5230 ", status.export_dir, "\uFF0C\u518D\u5728 CheatDeck \u4E2D\u9009\u62E9\u5BF9\u5E94\u7684 Trainer.exe\u3002\u540C\u6B65\u540E\u7684\u6E38\u620F\u76EE\u5F55\u540D\u4E0D\u542B\u4E2D\u6587\u6216\u5355\u5F15\u53F7\uFF0C\u4FBF\u4E8E CheatDeck \u4F7F\u7528\u3002"] }) }), SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsxs(DFL.ButtonItem, { layout: "below", disabled: busy, onClick: () => run("修改器同步完成。", "同步修改器失败。", () => syncTrainers()), children: [SP_JSX.jsx(FaDownload, {}), " \u540C\u6B65\u4FEE\u6539\u5668"] }) })] })), SP_JSX.jsx(DFL.PanelSectionRow, { children: SP_JSX.jsxs(DFL.ButtonItem, { layout: "below", disabled: busy, onClick: () => refresh(), children: [SP_JSX.jsx(FaGamepad, {}), " \u5237\u65B0\u72B6\u6001"] }) })] }));
}
var index = definePlugin(() => {
    console.log("GCM Launcher frontend loaded");
    return {
        name: "GCM Launcher",
        titleView: SP_JSX.jsx("div", { className: DFL.staticClasses.Title, children: title }),
        content: SP_JSX.jsx(Content, {}),
        icon: SP_JSX.jsx(FaGamepad, {}),
        onDismount() {
            console.log("GCM Launcher frontend unloading");
        },
    };
});

export { index as default };
//# sourceMappingURL=index.js.map
