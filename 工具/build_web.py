# -*- coding: utf-8 -*-
"""把 教學網頁/index.html 從磁鐵模板改寫成「網路不沉迷」版本。
每個替換都 assert 恰好發生一次，可重跑（重跑前須還原模板，或只影響已替換內容時為冪等）。
"""
import sys, os, json, shutil, re, io
sys.path.insert(0, os.path.dirname(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from content import QUIZ, VIDEOS, FLOW, OBJECTIVES, MISCONCEPTIONS, CURRICULUM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "教學網頁")
PATH = os.path.join(WEB, "index.html")

html = open(PATH, encoding="utf-8").read()
n_before = html

def rep(old, new, count=1):
    global html
    assert html.count(old) == count, f"pattern not unique ({html.count(old)}): {old[:60]}"
    html = html.replace(old, new)

# ---------- 1. title / brand ----------
rep("<title>植物的構造和生長｜翰林版三上自然・教學專欄</title>",
    "<title>網路不沉迷｜康軒版六上健體・教學專欄</title>")
rep('<div class="brand">植物的構造和生長<span>。</span><span class="full" style="color:var(--muted);font-weight:400;font-size:13px"> 三上自然</span></div>',
    '<div class="brand">網路不沉迷<span>。</span><span class="full" style="color:var(--muted);font-weight:400;font-size:13px"> 六上健體</span></div>')

# ---------- 2. hero ----------
rep('<div class="eyebrow">翰林版・自然科學・三年級上學期・第一單元</div>',
    '<div class="eyebrow">康軒版・健康與體育・六年級上學期・單元一「健康用網路」第 1 課</div>')
rep("<h1>植物的構造和生長</h1>", "<h1>網路不沉迷</h1>")
rep("<p class=\"lead\">根吸水、莖運送、葉製造，花果種子繁衍下一代。兩節課的完整教學資源：教案、21 頁簡報（4 段旁白動畫）、10 題互動測驗、抽籤與計時器，以及最下方兩人一室的植物生長對戰。</p>",
    "<p class=\"lead\">用網路是工具，失控才是問題。三節課的完整教學資源：教案、22 頁簡報（4 段旁白動畫）、10 題互動測驗、抽籤與計時器，以及最下方兩人對戰的「網路不沉迷對戰」。</p>")
rep('<span class="chip g">根</span><span class="chip g">莖</span><span class="chip g">葉</span>',
    '<span class="chip g">正向使用</span><span class="chip g">自我篩檢</span><span class="chip g">遠離沉迷</span>')
rep('<span class="chip o">花</span><span class="chip o">果實</span><span class="chip o">種子</span>',
    '<span class="chip o">我訊息</span><span class="chip o">自我管理</span><span class="chip o">親子規範</span>')
rep('<span class="chip">80 分鐘</span><span class="chip">2 節課</span>',
    '<span class="chip">120 分鐘</span><span class="chip">3 節課</span>')

# ---------- 3. 教案區（整段換） ----------
perf_codes = "、".join(c for c, _ in CURRICULUM["學習表現"])
content_codes = "、".join(c for c, _ in CURRICULUM["學習內容"]) + "｜議題：" + "、".join(c for c, _ in CURRICULUM["議題"])

def lesson_block(f, first=False):
    rows = "".join(
        f'<tr><td class="time">{m} 分</td><td>{name}</td><td>{desc}</td></tr>'
        for name, m, desc in f["activities"])
    return (
        f'<details class="acc{" open" if first else ""}">\n'
        f'      <summary>{f["lesson"]}｜{f["title"]}（{f["minutes"]} 分鐘）</summary>\n'
        f'      <div class="body">\n        <div class="tbl-wrap">\n          <table>\n'
        f'            <thead><tr><th>時間</th><th>活動</th><th>教學說明</th></tr></thead>\n'
        f'            <tbody>\n              {rows}\n            </tbody>\n'
        f'          </table>\n        </div>\n      </div>\n    </details>')

myth_rows = "".join(f"<tr><td>{m}</td><td>{fix}</td></tr>" for m, fix in MISCONCEPTIONS)
obj_lis = "".join(f"<li>{o}</li>" for o in OBJECTIVES)

PLAN = f'''<section id="plan">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="kicker">LESSON PLAN</div>
        <h2>教案</h2>
        <p>三節課 120 分鐘。第一節正向使用與自我覺察；第二節沉迷影響與遠離方法；第三節「我訊息」溝通與自我管理。</p>
      </div>
      <a class="btn dark small" href="downloads/教案_網路不沉迷.docx" download>下載 Word 教案</a>
    </div>

    <div class="grid2" style="margin-bottom:16px">
      <div class="info-card">
        <h3><span class="num">i</span>課程資訊</h3>
        <dl class="kv">
          <dt>領域／科目</dt><dd>健康與體育（健康課）</dd>
          <dt>版本／單元</dt><dd>康軒版 六上 單元一「健康用網路」第 1 課</dd>
          <dt>教學年級</dt><dd>國小六年級（第三學習階段）</dd>
          <dt>節數</dt><dd>3 節（120 分鐘）</dd>
          <dt>課綱對照</dt><dd>{perf_codes}<br>學習內容：{content_codes}</dd>
        </dl>
      </div>
      <div class="info-card">
        <h3><span class="num">◎</span>學習目標</h3>
        <ul class="clean">
          {obj_lis}
        </ul>
      </div>
    </div>

    {lesson_block(FLOW[0], first=True)}

    {lesson_block(FLOW[1])}

    {lesson_block(FLOW[2])}

    <details class="acc">
      <summary>常見迷思與澄清</summary>
      <div class="body">
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>學生常見想法</th><th>教學澄清</th></tr></thead>
            <tbody>
              {myth_rows}
            </tbody>
          </table>
        </div>
      </div>
    </details>

    <details class="acc">
      <summary>評量設計與差異化</summary>
      <div class="body">
        <p><strong>評量方式：</strong>口頭發表（各活動中）、自我篩檢量表的完成與討論（第一節）、作息時間表與我訊息演練（實作評量）、隨堂測驗 10 題（第三節末，答對 7 題以上通過）。</p>
        <p><strong>需要協助的學生：</strong>提供作息表範例與「我訊息」句型提示卡，先完成「一個方法＋一句我訊息」即可；規範學習單可改與導師或同學互相約定。</p>
        <p><strong>學有餘力的學生：</strong>設計一份給全校的「網路健康」宣導海報或短劇，比較不同做法的長期效果。</p>
        <p style="margin-bottom:0"><strong>課後延伸：</strong>一週網路健康計畫（記錄上網時間、週末與家人回顧簽名）、和家人一起看一部推薦影片並討論家裡可以訂什麼規範。</p>
      </div>
    </details>
  </div>
</section>'''

html, n = re.subn(r'<section id="plan">.*?</section>', lambda m: PLAN, html, count=1, flags=re.S)
assert n == 1, "plan section"

# ---------- 4. 簡報區 ----------
rep("SLIDES · 21 PAGES", "SLIDES · 22 PAGES")
rep("<p>用左右鍵或下方縮圖換頁。第 4、7、9、14 頁是含旁白的動畫，點播放即可。</p>",
    "<p>用左右鍵或下方縮圖換頁。第 9、12、16、18 頁是含旁白的動畫，點播放即可。</p>")
rep('href="downloads/植物的構造和生長_教學簡報.pptx"', 'href="downloads/網路不沉迷_教學簡報.pptx"')
rep('<span class="counter" id="counter">1 / 21</span>', '<span class="counter" id="counter">1 / 22</span>')

# ---------- 5. 測驗區 ----------
rep("<p>每題答完立刻看解析。10 題滿分 100 分，答對 8 題以上就是植物小達人。</p>",
    "<p>每題答完立刻看解析。10 題滿分 100 分，答對 7 題以上就過關，成為「網路小達人」。</p>")

# ---------- 6. 影片區 ----------
rep("<p style=\"color:var(--muted); font-size:13px; margin-top:20px\">建議順序：根 → 莖 → 葉 → 花／果實／種子 → 統整。可作為課前預習或課後複習。</p>",
    "<p style=\"color:var(--muted); font-size:13px; margin-top:20px\">建議順序：藍光人（覺察）→ 我的第二人生（影響）→ 毒不添下（方法）→ 我訊息（溝通）→ 新北市宣導（總結）。可作為課前預習或課後複習。</p>")

# ---------- 7. 對戰區 ----------
rep("<h2>植物生長對戰</h2>", "<h2>網路不沉迷對戰</h2>")
rep('title="植物生長對戰" loading="lazy"', 'title="網路不沉迷對戰" loading="lazy"')

# ---------- 8. footer ----------
rep("<div><b>植物的構造和生長</b>｜翰林版三上自然・教學專欄</div>\n    <div>教案 Word ・ 簡報 21 頁 ・ 4 段旁白動畫 ・ 10 題測驗</div>",
    "<div><b>網路不沉迷</b>｜康軒版六上健體・教學專欄</div>\n    <div>教案 Word ・ 簡報 22 頁 ・ 4 段旁白動畫 ・ 10 題測驗</div>")

# ---------- 9. 測驗結果文案 ----------
rep("{ msg = '植物小達人！'; sub = '根莖葉花果實種子，你全都掌握了。'; }",
    "{ msg = '網路小達人！'; sub = '方法＋規範＋溝通，你全都掌握了。'; }")
rep("{ msg = '不錯，再加油！'; sub = '回到簡報看看各構造的功能，再挑戰一次。'; }",
    "{ msg = '不錯，再加油！'; sub = '回到簡報看看「遠離迷「網」五招」，再挑戰一次。'; }")
rep("{ msg = '再來一次！'; sub = '先看一遍簡報 p3–p18，你會發現簡單很多。'; }",
    "{ msg = '再來一次！'; sub = '先看一遍簡報 p3–p22，你會發現簡單很多。'; }")

# ---------- 10. 資料陣列 ----------
ANIM = {9: "p09", 12: "p12", 16: "p16", 18: "p18"}
slides_js = "const SLIDES = [\n" + ",\n".join(
    '  { img:"slides/slide%02d.jpg"%s }' % (i, ', video:"media/%s.mp4"' % ANIM[i] if i in ANIM else "")
    for i in range(1, 23)) + "\n];"

def jstr(s):
    return json.dumps(s, ensure_ascii=False)

quiz_js = "const QUIZ = [\n" + ",\n".join(
    "  { q:%s, o:[%s], a:%d,\n    e:%s }" % (
        jstr(q["q"]), ",".join(jstr(o) for o in q["options"]), q["answer"], jstr(q["explain"]))
    for q in QUIZ) + "\n];"

videos_js = "const VIDEOS = [\n" + ",\n".join(
    "  { t:%s, d:%s, u:%s, id:%s, s:%s }" % (
        jstr(v["title"]), jstr(v["source"] + "｜" + v["use"]),
        jstr("https://www.youtube.com/watch?v=" + v["id"]), jstr(v["id"]), jstr("YouTube"))
    for v in VIDEOS) + "\n];"

html, n = re.subn(r"const SLIDES = \[.*?\n\];", lambda m: slides_js, html, count=1, flags=re.S)
assert n == 1, "SLIDES"
html, n = re.subn(r"const QUIZ = \[.*?\n\];", lambda m: quiz_js, html, count=1, flags=re.S)
assert n == 1, "QUIZ"
html, n = re.subn(r"const VIDEOS = \[.*?\n\];", lambda m: videos_js, html, count=1, flags=re.S)
assert n == 1, "VIDEOS"

open(PATH, "w", encoding="utf-8", newline="").write(html)

# ---------- 11. 複製可下載檔 ----------
dl = os.path.join(WEB, "downloads")
os.makedirs(dl, exist_ok=True)
pairs = [
    ("教案/教案_網路不沉迷.docx", "教案_網路不沉迷.docx"),
    ("簡報/網路不沉迷_教學簡報.pptx", "網路不沉迷_教學簡報.pptx"),
    ("學習單/學習單1_自我篩檢與作息表.docx", "學習單1_自我篩檢與作息表.docx"),
    ("學習單/學習單2_規範與我訊息.docx", "學習單2_規範與我訊息.docx"),
    ("學習單/測驗卷_網路不沉迷.docx", "測驗卷_網路不沉迷.docx"),
    ("學習單/測驗卷_網路不沉迷.pdf", "測驗卷_網路不沉迷.pdf"),
]
for src, dst in pairs:
    s = os.path.join(ROOT, src.replace("/", os.sep))
    assert os.path.exists(s), "missing " + s
    shutil.copy2(s, os.path.join(dl, dst))
print("OK index.html 改寫完成 + downloads", len(pairs), "檔")
