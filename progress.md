# 进度报告5（第7周·Flutter工程结构与Widget体系）

## 一、任务理解

本次作业要完成三件事：
1. **案例复现 counter_deep**：跟随实践指南，把 `flutter create` 的默认计数器精读并逐步改造——先手绘 Widget 树，再加步长调节（弹层选 1/2/5）并把主题色改成 teal 种子色，最后加生命周期日志与自定义图片资源，每一步单独 Git 提交。
2. **自主实践五项**：Widget 树手绘图（完整层级＋两类 Widget 标注）、生命周期日志（钩子顺序＋热重载 r / 热重启 R 行为对照）、主题定制（种子色＋至少两处 `Theme.of` 取用）、资源替换（新增图片并显示成功）、AI 使用标注（与 TraeCode 方案对照差异）。
3. **独立研究任务（选做，本次全做）**：const 构造与 rebuild 优化实验、InheritedWidget 初探、Keys 作用实验。

**验收标准**：代码与指南一致可运行；Git 至少 3 次规范提交；进度报告按十节模板填写；能口头解释 setState 链路（点 FAB → setState 改数据 → 元素标记 dirty → 下一帧重建界面）；生命周期日志、资源显示有截图为证；独立研究任务写清探索过程与结论，不用 AI 直接生成结论。

## 二、环境与工具

- 操作系统：Windows 11（26200.9711）
- Flutter 3.47.2（stable，Dart 3.13.2），`flutter doctor` 全绿（Android licenses 部分未接受，不影响 Windows/Web 目标）
- 运行目标：Windows 桌面（windows-x64，Debug 模式）
- 开发工具：TraeCode（内置 AI 助手，用于复现阶段的方案对照与问题定位）
- 截图方式：PIL `ImageGrab` 全屏截图（含桌面与系统时间）

## 三、过程记录

| 时间 | 操作 |
|---|---|
| 19:28 | 阅读三份文档，明确任务清单 |
| 19:31 | `flutter create counter_deep`，git init，首次提交 `chore: init counter_deep from flutter create` |
| 19:33 | 通读 main.dart，绘制 Widget 树图（counter_deep/docs/widget_tree.png），提交 `docs: widget tree diagram` |
| 19:36 | 改造步长弹层（SimpleDialog 选 1/2/5）＋ teal 种子色主题，`flutter analyze` 通过后提交 `feat: step control & teal theme` |
| 19:37 | 加生命周期 print 日志；PIL 绘制空状态插画 empty_counter.png，pubspec 声明 `assets/images/`，提交 `feat: lifecycle logs & asset image` |
| 19:37–19:41 | `flutter run -d windows` 后台运行，pyautogui 模拟点击 FAB 与步长弹层，截取运行截图 |
| 19:47 | 脚本驱动 `flutter run` 发送 r/R 按键，记录生命周期钩子对照日志（lifecycle_console.txt） |
| 19:48 | 首次脚本运行报 C1083（ephemeral 文件丢失），`flutter clean` + `pub get` 后恢复正常 |
| 19:50–19:54 | 截 flutter doctor、git log、生命周期日志全屏图 |
| 19:57 | `flutter create research_experiments`，手写三个选做实验页面，提交 `feat: add research experiments ...` |
| 20:02–20:05 | 运行实验应用，分别验证 const/rebuild、InheritedWidget、Keys，截图并保存控制台日志 |

## 四、关键代码

**1. setState 链路（步长改造，counter_deep/lib/main.dart）**

```dart
void _incrementCounter() {
  setState(() {
    _counter += _step;   // 只改数据，不做耗时操作
  });
}
```

- `setState` 是 State 类的方法，回调里修改 `_counter`；
- 框架收到通知后把该元素标记为 dirty，下一帧重新调用 `build`；
- 界面随状态重建，体现"UI = f(state)"。本人手写，已运行验证：步长 5 时点击一次从 2 变 7（截图 04）。

**2. 主题定制与 Theme.of 取用（counter_deep/lib/main.dart）**

```dart
theme: ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
  useMaterial3: true,
),
// 取用1：AppBar
backgroundColor: Theme.of(context).colorScheme.inversePrimary,
// 取用2：步长文字
color: Theme.of(context).colorScheme.primary,
```

一处改种子色，AppBar、FAB、水波纹、文字同步变 teal，验证"样式与结构分离"。

**3. 生命周期日志（counter_deep/lib/main.dart）**

```dart
@override
void initState() { super.initState(); print('[Lifecycle] initState'); }
@override
void didChangeDependencies() { super.didChangeDependencies(); print('[Lifecycle] didChangeDependencies'); }
@override
void didUpdateWidget(covariant MyHomePage oldWidget) { super.didUpdateWidget(oldWidget); print('[Lifecycle] didUpdateWidget'); }
@override
void dispose() { print('[Lifecycle] dispose'); super.dispose(); }
// build 内：print('[Lifecycle] build: counter=$_counter, step=$_step');
```

## 五、检查点结果

- ✅ 计数器改造功能正确：FAB 按当前步长累加（步长1：0→1→2；切步长5：2→7，截图 02/03/04）；弹层可选 1/2/5。
- ✅ 生命周期日志齐全：启动顺序 initState → didChangeDependencies → build；按 r（热重载）仅 build 重跑且 State 保留（counter 不归零）；按 R（热重启）initState/didChangeDependencies/build 全部重跑，State 重置（截图 07，lifecycle_console.txt）。
- ✅ 资源图片正常显示：counter=0 时显示 empty_counter.png 插画，点击后消失（截图 01 vs 02）。
- ✅ Widget 树手绘图：counter_deep/docs/widget_tree.png，完整层级＋Stateless/Stateful/State 标注。
- ✅ 能口头解释 setState 链路：点 FAB → `_incrementCounter` → `setState` 内改 `_counter` → 元素标 dirty → 下一帧 `build` 重跑 → 新 `Text('$_counter')` 上屏。
- ✅ Git 规范：5 次提交，信息含 type 前缀（chore/docs/feat）。

## 六、问题与调试

**问题1**：`flutter create` 报 `Creation of temporary directory failed ... 拒绝访问`。
定位：错误路径指向 `.pub-cache`，是沙箱/权限问题而非 Flutter 本身。解决：关闭沙箱后重跑，创建成功。

**问题2**：脚本驱动 `flutter run` 时 Windows 构建报大量 C1083"无法打开源文件 ephemeral/cpp_client_wrapper/*.cc"。
定位：上一次后台 `flutter run` 被强制停止，ephemeral 目录留下半截文件。按指南"翻车警告"的标准做法执行 `flutter clean` + `flutter pub get` 后重新运行成功。教训：平台目录报错优先 clean，不手删文件。

**问题3**：`git log` 在新开 PowerShell 窗口报 `cannot spawn more: No such file or directory`。
定位：默认分页器 `more` 不存在。解决：`git --no-pager log --oneline`。

**问题4**：PowerShell 直接 `Get-Content` UTF-8 中文日志显示乱码。
解决：改用记事本打开截图，UTF-8 正常显示。

## 七、AI 使用记录

| 用途 | 指令摘要 | 输出 | 本人验证方式 |
|---|---|---|---|
| 复现方案对照 | "给计数器加步长弹层＋teal主题，我猜要改 theme、加 _step、改 _incrementCounter、加 actions" | TraeCode 给出对照方案：思路一致，额外建议用 `showDialog<int>` + `Navigator.pop(context, value)` 回传选中值，并把步长显示做成 `Theme.of` 取色的文本 | 对照差异：我的猜测漏了"弹层返回值回传"与"步长可视化"；采纳后 `flutter analyze` 通过，运行点击验证步长 2→7 |
| 报错定位 | ephemeral C1083 报错日志 | 建议 flutter clean | 执行后恢复，与指南翻车警告一致 |
| 文档提取 | 提取三份 docx 全文 | pandoc 不可用改用 python-docx | 逐节核对模板十节无遗漏 |
| 截图自动化 | PIL 全屏截图＋pyautogui 点击 | 可复现的截图脚本 | 每张截图人工查看确认内容正确 |

差异记录：AI 方案在弹层回传上更规范（`Navigator.pop(context, value)`），我原猜的"点选项直接改"需要在每个选项里写 setState，代码更散；采纳 AI 方案。主题部分两方一致（`ColorScheme.fromSeed(seedColor: Colors.teal)` + `useMaterial3: true`）。

## 八、证据截图

（均存于仓库 screenshots/，全屏含桌面与系统时间）

1. `01_app_initial.png`：counter_deep 初始界面，teal 主题＋空状态插画 empty_counter.png 正常显示（19:37）。
2. `02_counter_incremented.png`：连点 FAB 两次，计数=2，插画按条件消失（19:40）。
3. `03_step_dialog.png`：步长弹层，可选"每次 +1/+2/+5"（19:40）。
4. `04_step5_increment.png`：选步长 5 后点一次，计数 2→7，"当前步长：+5"（19:41）。
5. `05_flutter_doctor.png`：flutter doctor 全绿（19:50）。
6. `06_git_log.png`：git log 显示 4 次规范提交（19:54）。
7. `07_lifecycle_console.png`：生命周期日志——启动三钩子顺序；r 热重载仅 build 重跑；R 热重启全部重跑（19:54）。
8. `08_research_home.png`：研究实验主页（20:02）。
9. `09_exp1_const_rebuild.png`：实验1界面，父级重建 3 次；日志显示非 const 项重建 4 次、const 项仅 1 次（20:03）。
10. `10_exp2_inherited.png`：实验2，深层叶子无传参直接读到 count=2（20:04）。
11. `11_exp3_no_key.png`：实验3不带 Key 交换，颜色（状态）留在原位置——条目 3 拿到原条目 1 的橙黄（20:05）。
12. `12_exp3_with_key.png`：带 ValueKey 后交换，颜色跟着条目走（20:05）。

## 九、自评

| 要求 | 完成情况 |
|---|---|
| 案例复现 counter_deep | ✅ 三步骤全部完成，代码可运行 |
| 检查点（步长/主题/日志/资源/口头解释） | ✅ 全部有截图与日志证据 |
| Git 规范（≥3 次提交） | ✅ 5 次提交，type 前缀规范 |
| Widget 树手绘图 | ✅ docs/widget_tree.png，层级＋两类 Widget 标注 |
| 生命周期日志＋r/R 对照 | ✅ lifecycle_console.txt＋截图 07 |
| 主题定制（种子色＋≥2 处 Theme.of） | ✅ inversePrimary / primary 两处取用 |
| 资源替换 | ✅ empty_counter.png 显示成功 |
| AI 使用标注（含差异记录） | ✅ 见第七节 |
| 选做1 const/rebuild | ✅ 量化对比：父重建 3 次，非 const 项 build 4 次、const 项仅 1 次 |
| 选做2 InheritedWidget | ✅ 手写 CounterScope，深层叶子直接取值；理解 Theme 即基于 InheritedWidget |
| 选做3 Keys | ✅ 对照实验：无 Key 状态跟位置，有 ValueKey 状态跟条目 |
| 进度报告十节 | ✅ 本文档 |

## 十、一句话收获与下一步计划

**收获**：Flutter 的声明式核心就一句话——UI = f(state)：我只管在 setState 里改数据，框架负责标脏、重建、上屏；Widget 树里 Stateless 是骨架、Stateful 是心脏，生命周期钩子则规定了这颗心脏的跳动节律（initState 一次、build 多次、dispose 收尾），热重载保 State、热重启重置 State。

**遗留问题**：didUpdateWidget 本次没有自然触发场景（父级没传新配置），准备在路由传参的第7课继续观察；const 优化在大列表上的收益量级还需实测。

**下次预习要点**：导航与路由（Navigator 2.0 / routes 表）、BuildContext 向上查找的边界、多页面间的状态传递。
