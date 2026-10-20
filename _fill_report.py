# -*- coding: utf-8 -*-
"""Fill mapp-progress-report-5 template with answers, save to lecture5."""
from docx import Document
from docx.oxml.ns import qn
from copy import deepcopy

SRC = r"c:\Users\lenovo\Desktop\mapp-progress-report-5.docx"
DST = r"c:\Users\lenovo\lecture5\mapp-progress-report-5.docx"

answers = {
    "一、任务理解": [
        "本次作业要完成：①案例复现 counter_deep——flutter create 默认计数器精读并逐 Step 改造：手绘 Widget 树、步长弹层(1/2/5)＋teal 种子色主题、生命周期日志＋自定义图片资源，每步单独 Git 提交；②自主实践五项：Widget 树手绘图(完整层级＋两类 Widget 标注)、生命周期日志(钩子顺序＋热重载 r/热重启 R 行为对照)、主题定制(种子色＋至少两处 Theme.of 取用)、资源替换(新增图片并显示成功)、AI 使用标注(与 TraeCode 方案对照差异)；③独立研究任务(选做，本次全做)：const/rebuild 优化、InheritedWidget 初探、Keys 作用实验。",
        "验收标准：代码可运行且与指南一致；Git≥3 次规范提交；报告按十节填写；能口头解释 setState 链路(点 FAB→setState 改数据→元素标 dirty→下一帧重建)；日志与资源显示有截图；选做任务写清探索过程与结论。",
    ],
    "二、环境与工具": [
        "Windows 11(26200.9711)；Flutter 3.47.2 stable(Dart 3.13.2)，flutter doctor 全绿；运行目标 Windows 桌面(windows-x64 Debug)；开发工具 TraeCode(内置 AI，用于复现方案对照与报错定位)；PIL ImageGrab 全屏截图(含桌面与系统时间)。",
    ],
    "三、过程记录": [
        "19:31 flutter create counter_deep → git init → 提交 chore: init counter_deep from flutter create；19:33 通读 main.dart、绘制 Widget 树(docs/widget_tree.png) → 提交 docs: widget tree diagram；19:36 步长弹层(SimpleDialog 选 1/2/5)＋teal 主题，analyze 通过 → 提交 feat: step control & teal theme；19:37 生命周期 print＋PIL 绘制 empty_counter.png、pubspec 声明 assets/images/ → 提交 feat: lifecycle logs & asset image；19:37-19:41 flutter run -d windows 后台运行，点击 FAB/步长弹层并截图；19:47 脚本驱动 flutter run 发送 r/R 按键，记录钩子对照日志；19:48 遇 C1083(ephemeral 半截文件)，flutter clean+pub get 恢复；19:50-19:54 截 flutter doctor/git log/生命周期日志；19:57 flutter create research_experiments，手写三个实验 → 提交 feat: add research experiments；20:02-20:05 运行验证三实验并截图；随后提交截图日志、progress.md、README 并推送 GitHub，共 7 次提交。",
    ],
    "四、关键代码": [
        "①setState 链路(本人手写，已运行验证)：void _incrementCounter() { setState(() { _counter += _step; }); } ——setState 是 State 的方法，回调内只改数据；框架标脏后下一帧重跑 build，体现 UI=f(state)。步长 5 时点击 2→7(截图04)。",
        "②主题定制(与 AI 方案一致)：theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal), useMaterial3: true)；取用两处——AppBar 的 backgroundColor: Theme.of(context).colorScheme.inversePrimary，步长文字 color: Theme.of(context).colorScheme.primary。一处改种子色全应用同步变 teal。",
        "③生命周期日志(本人手写)：initState/didChangeDependencies/didUpdateWidget/dispose 各一行 print，build 内 print('[Lifecycle] build: counter=$_counter, step=$_step')；日志验证启动三钩子顺序及 r/R 差异。",
    ],
    "五、检查点结果": [
        "计数器改造功能正确：FAB 按当前步长累加(0→1→2；切步长5后 2→7)；弹层可选 1/2/5(截图02/03/04)。",
        "生命周期日志齐全：启动 initState→didChangeDependencies→build；按 r 热重载仅 build 重跑、State 保留(counter 不归零)；按 R 热重启三钩子全部重跑、State 重置(截图07、lifecycle_console.txt)。",
        "资源图片正常显示：counter=0 时显示 empty_counter.png 空状态插画，点击后消失(截图01 vs 02)；Widget 树手绘图存 counter_deep/docs/widget_tree.png。",
        "能口头解释 setState 链路：点 FAB→_incrementCounter→setState 内改 _counter→元素标 dirty→下一帧 build 重跑→新 Text 上屏。Git 共 7 次提交，信息含 type 前缀。",
    ],
    "六、问题与调试": [
        "①flutter create 报 Creation of temporary directory failed/拒绝访问：定位为 pub 缓存目录权限(沙箱)问题，关闭沙箱重跑成功。",
        "②脚本驱动 flutter run 时 Windows 构建报大量 C1083 无法打开 ephemeral/cpp_client_wrapper/*.cc：定位为上一次后台运行被强停留下半截文件；按指南翻车警告执行 flutter clean+flutter pub get 后恢复。教训：平台目录报错优先 clean，不手删文件。",
        "③新开 PowerShell 执行 git log 报 cannot spawn more：默认分页器 more 不存在，改 git --no-pager log。④PowerShell 直接显示 UTF-8 中文日志乱码，改用记事本打开截图。",
    ],
    "七、AI使用记录": [
        "①复现方案对照(用途：步长弹层＋主题改造)：我先猜改 theme、加 _step、改 _incrementCounter、加 actions 四处；TraeCode 方案思路一致，额外用 showDialog<int>＋Navigator.pop(context, value) 回传选中值，并把步长显示做成 Theme.of 取色文本。差异：我漏了弹层回传与步长可视化，采纳后 analyze 通过、运行验证 2→7。",
        "②报错定位：C1083 报错日志→AI 建议 flutter clean，执行恢复。③文档提取：pandoc 不可用改 python-docx 提取三份 docx。④截图自动化：PIL 全屏截图＋pyautogui 点击脚本，每张截图人工查看确认。AI 输出均经本人运行验证，未直接提交未验证代码。",
    ],
    "八、证据截图": [
        "均存仓库 screenshots/，全屏含桌面与系统时间。01 初始界面(teal 主题＋空状态插画，19:37)；02 连点 FAB 计数=2、插画消失(19:40)；03 步长弹层 1/2/5(19:40)；04 步长5后 2→7、当前步长+5(19:41)；05 flutter doctor 全绿(19:50)；06 git log 四次提交(19:54)；07 生命周期日志：启动三钩子、r 仅 build 重跑、R 全部重跑(19:54)；08 实验主页(20:02)；09 实验1父重建3次界面(日志：非const项重建4次、const项仅1次，20:03)；10 实验2深层叶子读到 count=2(20:04)；11 实验3不带Key交换后颜色留在原位置(20:05)；12 带ValueKey后颜色跟条目走(20:05)。",
    ],
    "九、自评": [
        "案例复现✅三步骤完成可运行；检查点✅证据齐全；Git 规范✅7 次提交；Widget 树图✅层级＋两类标注；生命周期 r/R 对照✅；主题定制✅种子色＋两处 Theme.of；资源替换✅图片显示成功；AI 使用标注✅含差异记录；选做1✅量化对比(父重建3次：非const 4次、const 1次)；选做2✅手写 CounterScope 深层取值，理解 Theme 即基于 InheritedWidget；选做3✅对照实验(无Key状态跟位置、有ValueKey状态跟条目)；报告十节✅。",
    ],
    "十、一句话收获": [
        "收获：Flutter 声明式核心即 UI=f(state)——setState 里只管改数据，框架负责标脏重建上屏；Stateless 是骨架、Stateful 是心脏，生命周期钩子规定跳动节律(initState 一次、build 多次、dispose 收尾)，热重载保 State、热重启重置 State。",
        "遗留问题：didUpdateWidget 本次无自然触发场景，准备在第7课路由传参中继续观察；const 优化在大列表上的收益量级待实测。下次预习：导航与路由(Navigator/routes)、BuildContext 向上查找边界、跨页面状态传递。",
    ],
}

doc = Document(SRC)

# find the first empty paragraph style to clone; use normal style
def insert_after(paragraph, text):
    new_p = deepcopy(paragraph._p)
    # clear runs
    for r in new_p.findall(qn('w:r')):
        new_p.remove(r)
    paragraph._p.addnext(new_p)
    from docx.text.paragraph import Paragraph
    np = Paragraph(new_p, paragraph._parent)
    np.add_run(text)
    return np

# iterate over a static list since we modify the tree
paras = list(doc.paragraphs)
for p in paras:
    for key, texts in answers.items():
        if p.text.strip().startswith(key):
            anchor = p
            for t in texts:
                anchor = insert_after(anchor, t)
            break

doc.save(DST)
print("saved", DST)
