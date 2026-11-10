# -*- coding: utf-8 -*-
"""產生 學習單 2 份 + 測驗卷（docx）"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from content import *

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT, "學習單"), exist_ok=True)
ACCENT = RGBColor(0x1F, 0x6E, 0x54)

def set_font(run, name="微軟正黑體", size=11, bold=False):
    run.font.name = name; run.font.size = Pt(size); run.font.bold = bold
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)

def para(doc, text, size=11, bold=False, align=None, space_after=6, color=None):
    p = doc.add_paragraph()
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    set_font(r, size=size, bold=bold)
    if color is not None:
        r.font.color.rgb = color
    return p

def title(doc, text, sub=None):
    para(doc, text, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=ACCENT, space_after=2)
    if sub:
        para(doc, sub, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

def table(doc, rows, cols, widths=None, header=None):
    t = doc.add_table(rows=rows, cols=cols); t.style = "Table Grid"
    if widths:
        for i, w in enumerate(widths):
            for c in t.columns[i].cells: c.width = Cm(w)
    if header:
        for j, h in enumerate(header):
            c = t.rows[0].cells[j]; c.paragraphs[0].text = ""
            set_font(c.paragraphs[0].add_run(h), size=10.5, bold=True)
    return t

def fill(cell, text, bold=False, size=10.5):
    cell.paragraphs[0].text = ""
    set_font(cell.paragraphs[0].add_run(text), size=size, bold=bold)

# ==================== 學習單 1 ====================
doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2); s.bottom_margin = Cm(2); s.left_margin = Cm(2); s.right_margin = Cm(2)
title(doc, "學習單 1：你迷「網」了嗎？", "國小健體六上・網路不沉迷　班級：______　座號：______")

para(doc, "一、網路使用習慣自我篩檢量表", bold=True, size=13)
para(doc, "符合的打「✓」，誠實作答才能幫助自己。", size=9.5)
checks = [
    "我曾經上網時間比原本打算的還久（說好 30 分鐘卻玩了 1 小時以上）。",
    "爸媽叫我關掉電腦或手機時，我會覺得煩躁或不高興。",
    "我曾經為了上網而熬夜、隔天上課想睡覺。",
    "我曾經因為玩遊戲或看影片而沒寫完作業。",
    "不上網的時候，我會一直想著網路上的事情。",
    "我曾經因為上網而減少和家人朋友相處或運動的時間。",
    "我會用上網來逃避不開心的事情或壓力。",
    "我曾經偷偷上網，或隱瞞自己上網做的事。",
]
t = table(doc, len(checks) + 1, 3, widths=[1.2, 12, 2.8], header=None)
fill(t.rows[0].cells[0], "題號", bold=True); fill(t.rows[0].cells[1], "檢核項目", bold=True); fill(t.rows[0].cells[2], "符合（✓）", bold=True)
for i, c in enumerate(checks, 1):
    fill(t.rows[i].cells[0], str(i)); fill(t.rows[i].cells[1], c)
para(doc, "計分：✓ 有 0～2 個＝習慣健康　｜　3～5 個＝要注意囉　｜　6 個以上＝該請爸媽老師幫忙", size=10, bold=True, space_after=10)

para(doc, "二、我的放學後作息時間表", bold=True, size=13)
para(doc, "規劃一天從放學到睡覺的作息，並標出上網時段（限時！）。", size=9.5)
t = table(doc, 9, 4, widths=[3, 5, 4, 4])
for j, h in enumerate(["時間", "活動", "是否上網（限時）", "做完打 ✓"]):
    fill(t.rows[0].cells[j], h, bold=True)
for i in range(1, 9):
    for j in range(4): fill(t.rows[i].cells[j], "")
doc.save(os.path.join(ROOT, "學習單", "學習單1_自我篩檢與作息表.docx"))

# ==================== 學習單 2 ====================
doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2); s.bottom_margin = Cm(2); s.left_margin = Cm(2); s.right_margin = Cm(2)
title(doc, "學習單 2：我們家的網路使用規範", "國小健體六上・網路不沉迷　請和家人一起完成　班級：______　座號：______")

para(doc, "一、我訊息練習", bold=True, size=13)
para(doc, "句型：當你（事件）……，我覺得（感受）……，因為（影響）……，我希望（期望）……", size=10.5)
situations = [
    "情境：哥哥晚上 11 點還在打遊戲，隔天早上爬不起來。",
    "情境：妹妹用平板看短影音，一看到吃飯時間都不放下。",
    "情境：爸爸吃飯時一直滑手機，全家都安靜無聲。",
]
for i, s in enumerate(situations, 1):
    para(doc, s, size=10.5, bold=True, space_after=2)
    para(doc, f"我的我訊息：當你＿＿＿＿＿＿，我覺得＿＿＿＿＿＿，因為＿＿＿＿＿＿，我希望＿＿＿＿＿＿。", size=10.5, space_after=10)

para(doc, "二、我們家的網路使用規範（親子共同約定）", bold=True, size=13)
t = table(doc, 7, 2, widths=[6, 10])
fill(t.rows[0].cells[0], "約定項目", bold=True); fill(t.rows[0].cells[1], "我們的約定", bold=True)
items = ["平日每天上網時間（建議不超過 30～60 分鐘）", "假日每天上網時間", "可以使用網路的時段與場合（如：晚餐時不用）", "主要用途（查資料／遊戲／影片……）", "時間到沒做完該做的事怎麼辦", "違反約定的處理方式"]
for i, it in enumerate(items, 1):
    fill(t.rows[i].cells[0], it)
    fill(t.rows[i].cells[1], "")
para(doc, "學生簽名：________　家人簽名：________　日期：________", size=10.5, space_after=4)
doc.save(os.path.join(ROOT, "學習單", "學習單2_規範與我訊息.docx"))

# ==================== 測驗卷 ====================
doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2); s.bottom_margin = Cm(2); s.left_margin = Cm(2); s.right_margin = Cm(2)
title(doc, "「網路不沉迷」隨堂測驗", "國小健體六上　班級：______　座號：______　得分：______")
para(doc, "一、選擇題（每題 10 分，共 100 分）", bold=True, size=12)
LETTER = "ABCD"
for i, q in enumerate(QUIZ, 1):
    para(doc, f"（　）{i}. {q['q']}", size=11, bold=False, space_after=2)
    for j, opt in enumerate(q["options"]):
        para(doc, f"　　　{LETTER[j]}. {opt}", size=11, space_after=1)
    para(doc, "", size=4, space_after=2)

doc.add_page_break()
para(doc, "【教師用】答案與解析", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=ACCENT)
t = table(doc, 2, 11, widths=[2] + [1.3] * 10)
fill(t.rows[0].cells[0], "題號", bold=True)
fill(t.rows[1].cells[0], "答案", bold=True)
for j in range(10):
    fill(t.rows[0].cells[j + 1], str(j + 1), bold=True)
    fill(t.rows[1].cells[j + 1], LETTER[QUIZ[j]["answer"]], bold=True)
para(doc, "", space_after=6)
for i, q in enumerate(QUIZ, 1):
    para(doc, f"{i}. （{q['level']}）{q['explain']}", size=10, space_after=3)
doc.save(os.path.join(ROOT, "學習單", "測驗卷_網路不沉迷.docx"))

print("OK 學習單x2 + 測驗卷")
