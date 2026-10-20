# -*- coding: utf-8 -*-
"""Draw the widget tree of counter_deep default counter app as PNG."""
from PIL import Image, ImageDraw, ImageFont

FONT = r"C:\Windows\Fonts\msyh.ttc"
f_title = ImageFont.truetype(FONT, 40)
f_node = ImageFont.truetype(FONT, 24)
f_tag = ImageFont.truetype(FONT, 20)

# node: (x_center, y_top, w, h, label, kind) kind: root/stateless/stateful/state/leaf
nodes = [
    (640, 120, 300, 60, "MyApp（StatelessWidget）", "stateless"),
    (640, 250, 300, 60, "MaterialApp", "stateless"),
    (640, 380, 340, 60, "MyHomePage（StatefulWidget）", "stateful"),
    (640, 510, 340, 60, "_MyHomePageState（State）", "state"),
    (640, 640, 300, 60, "Scaffold", "stateless"),
    (260, 780, 260, 60, "AppBar", "stateless"),
    (640, 780, 260, 60, "body: Center", "stateless"),
    (1020, 780, 340, 60, "FloatingActionButton", "stateless"),
    (260, 910, 260, 60, "Text(title)", "leaf"),
    (640, 910, 260, 60, "Column", "stateless"),
    (1020, 910, 340, 60, "Icon(Icons.add)", "leaf"),
    (440, 1040, 300, 60, "Text(提示文案, const)", "leaf"),
    (840, 1040, 300, 60, "Text('$_counter')", "leaf"),
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (4, 5), (4, 6), (4, 7),
    (5, 8), (6, 9), (7, 10),
    (9, 11), (9, 12),
]

colors = {
    "stateless": ("#D5E8F0", "#1F6F8B"),
    "stateful": ("#FFE0B2", "#E65100"),
    "state": ("#F8BBD0", "#AD1457"),
    "leaf": ("#E8F5E9", "#2E7D32"),
    "root": ("#D5E8F0", "#1F6F8B"),
}

W, H = 1280, 1200
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

title = "counter_deep 默认计数器 Widget 树（手绘整理版）"
tw = d.textlength(title, font=f_title)
d.text(((W - tw) / 2, 40), title, font=f_title, fill="black")

def bottom(i):
    x, y, w, h, *_ = nodes[i]
    return (x, y + h)

def top(i):
    x, y, w, h, *_ = nodes[i]
    return (x, y)

for a, b in edges:
    d.line([bottom(a), top(b)], fill="#555555", width=3)

for x, y, w, h, label, kind in nodes:
    fill, outline = colors[kind]
    d.rounded_rectangle([x - w/2, y, x + w/2, y + h], radius=12, fill=fill, outline=outline, width=3)
    lw = d.textlength(label, font=f_node)
    d.text((x - lw/2, y + h/2 - 16), label, font=f_node, fill="black")

# legend
ly = 1140
items = [("StatelessWidget", "stateless"), ("StatefulWidget", "stateful"), ("State 对象", "state"), ("叶子展示节点", "leaf")]
lx = 120
for text, kind in items:
    fill, outline = colors[kind]
    d.rounded_rectangle([lx, ly, lx + 30, ly + 24], radius=6, fill=fill, outline=outline, width=2)
    d.text((lx + 40, ly - 2), text, font=f_tag, fill="black")
    lx += 40 + d.textlength(text, font=f_tag) + 50

img.save(r"c:\Users\lenovo\lecture5\counter_deep\docs\widget_tree.png")
print("saved")
