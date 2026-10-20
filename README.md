# lecture5 — 第7周 Flutter 工程结构与 Widget 体系

仓库地址：https://github.com/XiYuhang-alex/lecture5

## 目录结构

| 路径 | 内容 |
|---|---|
| `counter_deep/` | 案例复现：默认计数器精读与改造（步长弹层 1/2/5、teal 主题、生命周期日志、空状态插画） |
| `counter_deep/docs/widget_tree.png` | Widget 树图（完整层级＋Stateless/Stateful 标注） |
| `research_experiments/` | 独立研究（选做）：实验1 const/rebuild 优化、实验2 InheritedWidget、实验3 Keys 作用 |
| `screenshots/` | 全屏证据截图（运行、弹层、生命周期日志、flutter doctor、git log、三个实验）与控制台日志 |
| `progress.md` | 进度报告5（十节） |

## 运行方式

```powershell
cd counter_deep
flutter pub get
flutter run -d windows   # 或 -d chrome
```

```powershell
cd research_experiments
flutter pub get
flutter run -d windows
```

## 提交记录

- `chore: init counter_deep from flutter create`
- `docs: widget tree diagram`
- `feat: step control & teal theme`
- `feat: lifecycle logs & asset image`
- `feat: add research experiments (const rebuild, InheritedWidget, Keys)`
- `docs: add run & experiment screenshots, console logs`
- `docs: progress report & README`
