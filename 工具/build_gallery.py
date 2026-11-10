# -*- coding: utf-8 -*-
"""產生 教學網頁/media/ 概念圖庫：img/*.jpg（600x400）＋ thumb/*.jpg（240 寬）＋ images.js
不需要 AI 生圖 key，純 Pillow 繪製，配色與簡報一致。
"""
import sys, os, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(ROOT, "教學網頁", "media")
IMG = os.path.join(MEDIA, "img")
THUMB = os.path.join(MEDIA, "thumb")
os.makedirs(IMG, exist_ok=True); os.makedirs(THUMB, exist_ok=True)

F_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
F_REG = r"C:\Windows\Fonts\msjh.ttc"

GROUPS = {"01": ("概念", (31, 110, 84)), "02": ("警訊與方法", (232, 100, 27)), "03": ("溝通與規範", (142, 68, 19))}
CARDS = [
    ("01", "c01", "網路的正向使用", "查詢・聯繫・學習・休閒"),
    ("01", "c02", "網路沉迷的徵兆", "失控＋影響生活"),
    ("01", "c03", "惡性循環", "壓力→逃避→落後→壓力更大"),
    ("01", "c04", "遠離迷「網」", "五個好方法"),
    ("01", "c05", "網路使用規範", "親子共同約定"),
    ("01", "c06", "「我訊息」", "事件→感受→影響→期望"),
    ("01", "c07", "自我管理與監督", "訂目標→做記錄→檢討"),
    ("02", "w01", "警訊 1", "時間越用越長"),
    ("02", "w02", "警訊 2", "想停卻停不下來"),
    ("02", "w03", "警訊 3", "作息亂掉、熬夜上網"),
    ("02", "w04", "警訊 4", "該做的事沒做完"),
    ("02", "w05", "警訊 5", "不上網就煩躁"),
    ("02", "m01", "第 1 招", "訂時間：設鬧鐘或計時器"),
    ("02", "m02", "第 2 招", "先做事：功課完成才上網"),
    ("02", "m03", "第 3 招", "替代活動：運動、閱讀"),
    ("02", "m04", "第 4 招", "睡前不用：手機不入臥室"),
    ("02", "m05", "第 5 招", "定時休息：每 30 分鐘動一動"),
    ("03", "i01", "我訊息 ① 事件", "當你……"),
    ("03", "i02", "我訊息 ② 感受", "我覺得……"),
    ("03", "i03", "我訊息 ③ 影響", "因為……"),
    ("03", "i04", "我訊息 ④ 期望", "我希望……"),
    ("03", "r01", "規範怎麼訂", "平日 30 分鐘・晚餐時不用"),
]

W, H = 600, 400
def font(path, size):
    return ImageFont.truetype(path, size)

entries = []
for g, code, title, sub in CARDS:
    gname, (r, gr, b) = GROUPS[g]
    img = Image.new("RGB", (W, H), (r, gr, b))
    d = ImageDraw.Draw(img)
    # 半透明深色條（用實色近似）
    d.rectangle([0, 0, W, 64], fill=(int(r*0.8), int(gr*0.8), int(b*0.8)))
    d.text((24, 14), f"網路不沉迷・{gname}", font=font(F_REG, 26), fill=(247, 243, 233))
    # 標題置中
    tf = font(F_BOLD, 56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 150), title, font=tf, fill=(255, 255, 255))
    ts = font(F_REG, 30)
    tw2 = d.textlength(sub, font=ts)
    d.text(((W - tw2) / 2, 240), sub, font=ts, fill=(255, 240, 220))
    # 底部裝飾線
    d.rectangle([60, 330, W - 60, 336], fill=(255, 255, 255))
    p = os.path.join(IMG, code + ".jpg")
    img.save(p, quality=88)
    img.thumbnail((240, 160))
    img.save(os.path.join(THUMB, code + ".jpg"), quality=85)
    entries.append({"code": code, "group": g, "title": f"{title}｜{sub}",
                    "img": f"media/img/{code}.jpg", "thumb": f"media/thumb/{code}.jpg"})

js = "const GALLERY = " + json.dumps(entries, ensure_ascii=False, indent=2).replace('"code": ', '"code":') + ";\n"
open(os.path.join(MEDIA, "images.js"), "w", encoding="utf-8").write(js)
print("OK 圖庫", len(entries), "張 →", MEDIA)
