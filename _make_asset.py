# -*- coding: utf-8 -*-
"""Create a custom teal illustration used as empty-state image in counter_deep."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 640, 360
img = Image.new("RGB", (W, H), "#E0F2F1")
d = ImageDraw.Draw(img)

# decorative circles
for cx, cy, r, c in [(90, 80, 55, "#B2DFDB"), (560, 300, 70, "#B2DFDB"),
                     (570, 60, 35, "#80CBC4"), (80, 300, 30, "#80CBC4")]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

# counter card
d.rounded_rectangle([200, 70, 440, 290], radius=24, fill="white", outline="#00897B", width=5)
# plus button
d.ellipse([285, 190, 355, 260], fill="#00897B")
d.rectangle([312, 205, 328, 245], fill="white")
d.rectangle([297, 217, 343, 233], fill="white")

f_big = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 64)
f_sm = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 26)
t1 = "0"
d.text((320 - d.textlength(t1, font=f_big) / 2, 95), t1, font=f_big, fill="#004D40")
t2 = "counter_deep"
d.text((320 - d.textlength(t2, font=f_sm) / 2, 285), t2, font=f_sm, fill="#00695C")

os.makedirs(r"c:\Users\lenovo\lecture5\counter_deep\assets\images", exist_ok=True)
img.save(r"c:\Users\lenovo\lecture5\counter_deep\assets\images\empty_counter.png")
print("saved")
