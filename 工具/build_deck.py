# -*- coding: utf-8 -*-
"""產生 簡報/網路不沉迷_教學簡報.pptx（21+ 頁 16:9）
字型：微軟正黑體（補 a:ea，避免中文掉字型）
配色：米白 #F7F3E9／墨綠 #1F6E54／橙 #E8641B
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from content import *

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "簡報", "網路不沉迷_教學簡報.pptx")

INK = RGBColor(0x1F, 0x6E, 0x54)      # 墨綠
ORANGE = RGBColor(0xE8, 0x64, 0x1B)   # 橙
CREAM = RGBColor(0xF7, 0xF3, 0xE9)    # 米白
DARK = RGBColor(0x33, 0x33, 0x33)
RED = RGBColor(0xC0, 0x39, 0x2B)

def _set_ea(run):
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        rPr.append(ea)
    ea.set("typeface", "微軟正黑體")

def add_text(slide, x, y, w, h, text, size=20, bold=False, color=DARK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="微軟正黑體"):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.name = font
    r.font.color.rgb = color
    _set_ea(r)
    return tb

def add_bullets(slide, x, y, w, h, items, size=18, gap=1.0, color=DARK):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(10 * gap)
        r = p.add_run(); r.text = "• " + it
        r.font.size = Pt(size); r.font.name = "微軟正黑體"; r.font.color.rgb = color
        _set_ea(r)
    return tb

def bg(slide, color=CREAM):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def band(slide, y=6.6, color=INK, h=0.9, text=None, tcolor=CREAM):
    from pptx.util import Inches as I
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, I(0), I(y), I(13.333), I(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = color; shp.line.fill.background()
    if text:
        tf = shp.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = text
        r.font.size = Pt(14); r.font.name = "微軟正黑體"; r.font.color.rgb = tcolor
        _set_ea(r)

def page_title(slide, text, color=INK):
    add_text(slide, 0.6, 0.35, 12.1, 1.0, text, size=30, bold=True, color=color)

def new_slide(prs, color=CREAM):
    s = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    bg(s, color)
    return s

def chip(slide, x, y, w, h, text, fill_color=INK, tcolor=CREAM, size=16, bold=True):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill_color
    shp.line.fill.background()
    tf = shp.text_frame; tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r = tf.paragraphs[0].add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.name = "微軟正黑體"; r.font.color.rgb = tcolor
    _set_ea(r)
    return shp

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

# ---------- p1 封面 ----------
s = new_slide(prs, INK)
add_text(s, 1, 2.2, 11.3, 1.6, "網路不沉迷", size=66, bold=True, color=CREAM, align=PP_ALIGN.CENTER)
add_text(s, 1, 3.9, 11.3, 0.8, "康軒國小健體六上・單元一「健康用網路」第 1 課", size=22, color=CREAM, align=PP_ALIGN.CENTER)
add_text(s, 1, 4.7, 11.3, 0.6, "3 節課｜用網路是工具・失控才是問題", size=18, color=RGBColor(0xFF, 0xC8, 0x96), align=PP_ALIGN.CENTER)
band(s, y=6.6, text="健康與體育　教學簡報")

# ---------- p2 學習目標 ----------
s = new_slide(prs)
page_title(s, "這三節課，我們要學會……")
add_bullets(s, 0.9, 1.7, 11.5, 4.6, OBJECTIVES, size=19, gap=1.2)
band(s, text="學習目標｜對應課綱 1a-Ⅲ-3、1b-Ⅲ-1、1b-Ⅲ-4、2a-Ⅲ-2、2b-Ⅲ-2、4a-Ⅲ-2、Fa-Ⅲ-4、Fb-Ⅲ-1、資E11")

# ---------- p3 暖身 ----------
s = new_slide(prs)
page_title(s, "暖身：你今天的網路足跡", ORANGE)
add_text(s, 0.9, 1.8, 11.5, 1.2, "今天從起床到現在，你用網路做了哪些事？", size=24, bold=True)
add_bullets(s, 0.9, 3.0, 11.5, 3.0, [
    "查資料？傳訊息？看影片？玩遊戲？聽音樂？",
    "想一想：這些使用，哪些「幫助了你」？哪些「好像有點失控」？",
], size=20)
band(s, text="第一節｜活動 1　網路的正向使用")

# ---------- p4 四大正向功能 ----------
s = new_slide(prs)
page_title(s, "網路的四大正向功能")
cards = [("查詢", "查資料、找答案"), ("聯繫", "和家人朋友視訊、傳訊息"), ("學習", "線上課程、聽故事、學才藝"), ("休閒", "聽音樂、看影片、玩遊戲（有限度）")]
for i, (t1, t2) in enumerate(cards):
    x = 0.75 + (i % 2) * 6.1; y = 1.8 + (i // 2) * 2.2
    chip(s, x, y, 5.6, 1.7, f"{t1}｜{t2}", fill_color=(INK if i % 2 == 0 else ORANGE), size=20)
band(s, text="網路是工具，用對地方就是好幫手")

# ---------- p5 迷思破解 ----------
s = new_slide(prs)
page_title(s, "迷思破解：用網路 ＝ 沉迷？", RED)
chip(s, 0.9, 1.9, 11.5, 1.3, "✗ 迷思：每天用網路就是沉迷", fill_color=RED, size=22)
chip(s, 0.9, 3.5, 11.5, 1.3, "✓ 事實：沉迷的關鍵是「失控＋影響生活」，不是有沒有使用", fill_color=INK, size=22)
add_text(s, 0.9, 5.2, 11.5, 1.0, "重點：怎麼用、用多久、有沒有停得下來。", size=20, bold=True, color=ORANGE)
band(s, text="第一節｜概念澄清")

# ---------- p6 沉迷警訊 ----------
s = new_slide(prs)
page_title(s, "你迷「網」了嗎？沉迷的警訊")
add_bullets(s, 0.9, 1.7, 11.5, 4.6, [
    "時間越用越長：說好 10 分鐘，玩了 3 小時",
    "停不下來：想停卻停不了，被阻止就煩躁",
    "作息亂掉：熬夜上網、上課打瞌睡",
    "該做的事沒做：作業、複習被犧牲",
    "不上網就渾身不對勁：一直想著網路上的事",
], size=20, gap=1.1, color=DARK)
band(s, text="第一節｜活動 2　你迷「網」了嗎？")

# ---------- p7 自我篩檢 ----------
s = new_slide(prs)
page_title(s, "網路使用習慣自我篩檢量表")
add_bullets(s, 0.9, 1.7, 11.5, 3.6, [
    "拿出學習單 1，誠實勾選 8 題檢核項目",
    "0～2 個 ✓：習慣健康，繼續保持",
    "3～5 個 ✓：要注意囉，試著調整",
    "6 個以上 ✓：請爸媽或老師幫忙，一起訂方法",
], size=20, gap=1.1)
add_text(s, 0.9, 5.6, 11.5, 0.8, "自我篩檢是「自我管理」的第一步：先覺察，才能改變。", size=18, bold=True, color=INK)
band(s, text="第一節｜學習單 1")

# ---------- p8 小傑的故事 ----------
s = new_slide(prs)
page_title(s, "小傑的故事", ORANGE)
add_text(s, 0.9, 1.8, 11.5, 3.6,
         "小傑放學一回家就打開遊戲，玩到深夜才睡。\n上課打瞌睡、功課寫不完，成績一直退步。\n他被爸媽念、被老師提醒，心情很差，\n就更躲進遊戲裡……", size=22, bold=False)
add_text(s, 0.9, 5.4, 11.5, 0.9, "想一想：小傑下一步會怎樣？這個循環停得住嗎？", size=20, bold=True, color=RED)
band(s, text="第二節｜活動 3　網路沉迷的影響")

# ---------- p9 惡性循環（動畫頁） ----------
s = new_slide(prs)
page_title(s, "網路沉迷的惡性循環")
steps = ["壓力大\n（被念、退步）", "上網逃避\n（打遊戲）", "進度落後\n（該做的沒做）", "壓力更大\n（表現更差）"]
pos = [(4.9, 1.55), (8.3, 3.3), (4.9, 5.0), (1.5, 3.3)]
for (x, y), txt, c in zip(pos, steps, [RED, ORANGE, INK, RGBColor(0x8E, 0x44, 0x13)]):
    chip(s, x, y, 3.2, 1.25, txt, fill_color=c, size=16)
band(s, text="第二節｜（此頁附旁白動畫 p09）循環一旦啟動，會越陷越深")

# ---------- p10 沉迷的影響 ----------
s = new_slide(prs)
page_title(s, "沉迷影響的不只是眼睛")
cards = [("生理", "視力變差、睡眠不足、體能下降"), ("心理", "情緒煩躁、壓力更大、依賴網路"), ("社會", "課業退步、和家人朋友疏遠")]
for i, (t1, t2) in enumerate(cards):
    chip(s, 0.9, 1.8 + i * 1.6, 11.5, 1.25, f"{t1}｜{t2}", fill_color=[RED, ORANGE, INK][i], size=20)
add_text(s, 0.9, 6.0, 11.5, 0.6, "健康＝生理＋心理＋社會的安適狀態，沉迷會同時衝擊三個層面。", size=16, bold=True, color=ORANGE)
band(s, text="第二節｜影響統整")

# ---------- p11 影片頁 ----------
s = new_slide(prs, INK)
page_title(s, "影片：我的第二人生", CREAM)
add_text(s, 0.9, 2.2, 11.5, 1.2, "看完想一想：主角的生活和你像不像？", size=26, bold=True, color=CREAM)
add_bullets(s, 0.9, 3.6, 11.5, 2.4, [
    "虛擬世界裡的成就，能取代現實生活嗎？",
    "如果繼續這樣過一個月，他會失去什麼？",
], size=20, color=CREAM)
band(s, text="第二節｜影片討論（影片清單見教學網頁 #videos）")

# ---------- p12 遠離五招（動畫頁） ----------
s = new_slide(prs)
page_title(s, "遠離迷「網」五招")
moves = [("1", "訂時間：設定鬧鐘或計時器，時間到就停"), ("2", "先做事：功課與該做的事完成才上網"), ("3", "替代活動：運動、閱讀、和家人玩"), ("4", "睡前不用：手機不放床頭、不入臥室"), ("5", "定時休息：每 30 分鐘起來動一動、看遠方")]
for i, (n, t1) in enumerate(moves):
    chip(s, 0.9, 1.6 + i * 0.98, 1.0, 0.8, n, fill_color=ORANGE, size=20)
    add_text(s, 2.1, 1.68 + i * 0.98, 10.4, 0.8, t1, size=19, bold=True)
band(s, text="第二節｜活動 4（此頁附旁白動畫 p12）")

# ---------- p13 作息時間表 ----------
s = new_slide(prs)
page_title(s, "我的放學後作息時間表")
add_bullets(s, 0.9, 1.7, 11.5, 4.4, [
    "打開學習單 1，寫下放學到睡覺的每個時段",
    "標出「上網時段」並寫清楚限時幾分鐘",
    "至少安排一個非 3C 的替代活動",
    "做完一項打一個 ✓，明天檢查達成率",
], size=20, gap=1.1)
band(s, text="第二節｜學習單 1 完成頁")

# ---------- p14 親子規範 ----------
s = new_slide(prs)
page_title(s, "和爸媽一起訂「網路使用規範」")
add_bullets(s, 0.9, 1.7, 11.5, 4.4, [
    "時間：平日／假日各用多久？",
    "場合：哪些時段、地點不能用？（例：晚餐時、臥室）",
    "用途：主要用來做什麼？遊戲須家長知情",
    "違約處理：沒做到怎麼辦？先說好不吵架",
], size=20, gap=1.1)
add_text(s, 0.9, 5.8, 11.5, 0.7, "規範是保護線，不是處罰——和家人共同約定，減少衝突。", size=18, bold=True, color=INK)
band(s, text="第二節作業｜學習單 2（親子共同完成）")

# ---------- p15 影片頁 2 ----------
s = new_slide(prs, INK)
page_title(s, "影片：網路成癮教學動畫", CREAM)
add_bullets(s, 0.9, 2.2, 11.5, 3.4, [
    "為什麼會「越玩越想玩」？大腦的獎賞機制",
    "動畫裡的角色用了哪些方法自救？",
], size=22, color=CREAM)
band(s, text="第三節開場｜影片討論")

# ---------- p16 我訊息（動畫頁） ----------
s = new_slide(prs)
page_title(s, "溝通方法：「我訊息」")
parts = [("事件", "當你……", INK), ("感受", "我覺得……", ORANGE), ("影響", "因為……", RGBColor(0x8E, 0x44, 0x13)), ("期望", "我希望……", RGBColor(0x4A, 0x8F, 0x3C))]
for i, (t1, t2, c) in enumerate(parts):
    chip(s, 0.9 + i * 3.05, 1.9, 2.8, 1.35, f"{t1}\n{t2}", fill_color=c, size=18)
add_text(s, 0.9, 3.7, 11.5, 1.6,
         "例：「當你熬夜玩手機，我很擔心，因為你上課會沒精神，我希望你十點前休息。」", size=19, bold=True, color=DARK)
add_text(s, 0.9, 5.4, 11.5, 0.7, "描述事件與感受，不指責——比責罵更容易被聽進去。", size=18, bold=True, color=ORANGE)
band(s, text="第三節｜活動 5（此頁附旁白動畫 p16）")

# ---------- p17 演練 ----------
s = new_slide(prs)
page_title(s, "上臺演練：跟家人溝通上網時間", ORANGE)
add_bullets(s, 0.9, 1.8, 11.5, 4.2, [
    "兩人一組，一人扮演家長、一人扮演孩子",
    "情境：你上網超過約定時間，家長來提醒",
    "用完整的我訊息（事件→感受→影響→期望）回應",
    "交換角色再練一次；請 2 組上臺發表",
], size=20, gap=1.1)
band(s, text="第三節｜活動 5 演練")

# ---------- p18 自我管理（動畫頁） ----------
s = new_slide(prs)
page_title(s, "改進習慣三步驟：自我管理與監督")
steps = [("訂目標", "寫下最想改進的一個上網習慣"), ("做記錄", "記下每天實際使用的時間"), ("檢討修正", "每週回顧：達成了嗎？怎麼調整？")]
for i, (t1, t2) in enumerate(steps):
    chip(s, 0.9 + i * 4.1, 2.2, 3.7, 1.6, f"{i+1}. {t1}\n{t2}", fill_color=[INK, ORANGE, RGBColor(0x8E, 0x44, 0x13)][i], size=17)
add_text(s, 0.9, 4.6, 11.5, 0.8, "習慣的改變需要反覆檢視與修正——改一次沒成功，再調整再試。", size=18, bold=True, color=INK)
band(s, text="第三節｜活動 6（此頁附旁白動畫 p18）")

# ---------- p19 我的網路健康計畫 ----------
s = new_slide(prs)
page_title(s, "我的網路健康計畫（一週）")
add_bullets(s, 0.9, 1.8, 11.5, 4.2, [
    "每天記錄上網時間（學習單或筆記本）",
    "完成作息表上的打 ✓ 達成率",
    "週末和家人一起回顧，請家長簽名",
    "下週上課分享：最容易做到的一招是什麼？",
], size=20, gap=1.1)
band(s, text="課後延伸作業")

# ---------- p20 概念圖 ----------
s = new_slide(prs)
page_title(s, "總複習：一張圖記住這一課")
chip(s, 5.2, 1.6, 3.0, 1.0, "用網路是工具", fill_color=INK, size=20)
chip(s, 5.2, 3.0, 3.0, 1.0, "失控才是問題", fill_color=RED, size=20)
chip(s, 0.9, 4.5, 3.6, 1.3, "方法\n五招＋計時", fill_color=ORANGE, size=17)
chip(s, 4.9, 4.5, 3.6, 1.3, "規範\n親子共同約定", fill_color=RGBColor(0x8E, 0x44, 0x13), size=17)
chip(s, 8.9, 4.5, 3.6, 1.3, "溝通\n我訊息", fill_color=RGBColor(0x4A, 0x8F, 0x3C), size=17)
band(s, text="方法＋規範＋溝通＝健康的數位生活")

# ---------- p21 測驗 ----------
s = new_slide(prs)
page_title(s, "隨堂測驗：10 題挑戰", ORANGE)
add_bullets(s, 0.9, 1.8, 11.5, 4.0, [
    "紙本測驗卷或線上測驗（教學網頁 #quiz）",
    "10 題選擇題，答對 7 題以上過關",
    "線上版每題都有解析，答錯記得看「錯在哪裡」",
    "挑戰：和家人玩「網路不沉迷對戰」，10 題搶答！",
], size=20, gap=1.1)
band(s, text="評量｜了解自己的學習成果")

# ---------- p22 總結 ----------
s = new_slide(prs, INK)
add_text(s, 1, 2.0, 11.3, 1.2, "記得這句話", size=30, bold=True, color=CREAM, align=PP_ALIGN.CENTER)
add_text(s, 1, 3.0, 11.3, 1.4, "用網路是工具，失控才是問題。", size=40, bold=True, color=RGBColor(0xFF, 0xC8, 0x96), align=PP_ALIGN.CENTER)
add_text(s, 1, 4.6, 11.3, 0.8, "方法＋規範＋溝通，做網路的主人！", size=24, color=CREAM, align=PP_ALIGN.CENTER)
band(s, text="網路不沉迷｜康軒國小健體六上 單元一 第 1 課")

prs.save(OUT)
print("OK", OUT, "slides:", len(prs.slides._sldIdLst))
