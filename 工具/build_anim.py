# -*- coding: utf-8 -*-
"""產生 4 段旁白動畫專案：影片/p09 惡性循環、p12 遠離五招、p16 我訊息、p18 自我管理
用法：python build_anim.py gen   （產 VO + HTML）
      之後用 hyperframes check / snapshot / render
"""
import sys, os, subprocess, math, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID = os.path.join(ROOT, "影片")
MEDIA = os.path.join(ROOT, "教學網頁", "media")
os.makedirs(MEDIA, exist_ok=True)

VOICE = "zh-TW-HsiaoChenNeural"

PAGES = {
    "p09": {
        "title": "網路沉迷的惡性循環",
        "vo": "小傑壓力大就用打電動逃避，結果功課越積越多、成績退步，壓力反而更大，只好再躲進網路裡。這就是網路沉迷的惡性循環，會讓人越陷越深。",
        "steps": [("壓力大", "被念、成績退步"), ("上網逃避", "打遊戲、滑影片"), ("進度落後", "該做的沒做"), ("壓力更大", "表現更差")],
        "end": "循環一旦啟動，會越陷越深",
        "color_seq": ["#C0392B", "#E8641B", "#1F6E54", "#8E4413"],
    },
    "p12": {
        "title": "遠離迷「網」五招",
        "vo": "遠離沉迷有五招：訂時間設鬧鐘、先做完功課、安排替代活動、睡前不碰手機、每三十分鐘起來動一動。做網路的主人！",
        "steps": [("1", "訂時間：設定鬧鐘或計時器"), ("2", "先做事：功課完成才上網"), ("3", "替代活動：運動、閱讀、和家人玩"), ("4", "睡前不用：手機不入臥室"), ("5", "定時休息：每 30 分鐘起來動一動")],
        "end": "做網路的主人",
        "color_seq": ["#1F6E54", "#E8641B", "#8E4413", "#4A8F3C", "#C0392B"],
    },
    "p16": {
        "title": "溝通方法：「我訊息」",
        "vo": "跟家人溝通上網時間，用我訊息：說事件、說感受、說影響、說期望。例如：當你熬夜玩手機，我很擔心，因為上課會沒精神，希望你早點休息。",
        "steps": [("事件", "當你……"), ("感受", "我覺得……"), ("影響", "因為……"), ("期望", "我希望……")],
        "end": "描述事件與感受，不指責——比責罵更容易被聽進去",
        "color_seq": ["#1F6E54", "#E8641B", "#8E4413", "#4A8F3C"],
    },
    "p18": {
        "title": "改進習慣三步驟",
        "vo": "改進習慣三步驟：訂小目標、每天記錄上網時間、每週檢討一次。沒成功沒關係，調整方法再試一次，你就是網路的主人！",
        "steps": [("訂目標", "寫下最想改進的一個習慣"), ("做記錄", "每天記下實際使用的時間"), ("檢討修正", "每週回顧，調整方法再試")],
        "end": "你就是網路的主人！",
        "color_seq": ["#1F6E54", "#E8641B", "#8E4413"],
    },
}

HTML = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>{pid} {title}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  @font-face {{ font-family:"Microsoft JhengHei"; src: local("Microsoft JhengHei"); }}
  @font-face {{ font-family:"PingFang TC"; src: local("PingFang TC"); }}
  body {{ margin:0; background:#F7F3E9; }}
  #root {{ position:relative; width:100%; height:100%; overflow:hidden;
          font-family:"Microsoft JhengHei","PingFang TC",sans-serif; }}
  .clip {{ position:absolute; inset:0; }}
  .bar {{ position:absolute; left:0; top:0; width:100%; height:150px;
        background:#1F6E54; display:flex; align-items:center; padding-left:70px; }}
  .bar h1 {{ color:#F7F3E9; font-size:64px; margin:0; }}
  .stage {{ position:absolute; inset:0; }}
  .card {{ position:absolute; box-sizing:border-box; border-radius:28px; padding:24px 28px;
          color:#fff; text-align:center; }}
  .card .big {{ font-size:44px; font-weight:700; }}
  .card .sub {{ font-size:28px; margin-top:12px; }}
  .card.row {{ display:flex; align-items:center; gap:30px; text-align:left; }}
  .card.row .num {{ background:rgba(255,255,255,.25); border-radius:50%; width:88px; height:88px;
                   display:flex; align-items:center; justify-content:center; font-size:44px; font-weight:700; flex:none; }}
  .card.row .txt {{ font-size:38px; font-weight:600; }}
  .sub1 {{ position:absolute; color:#F7F3E9; background:#1F6E54; width:1840px;
          left:40px; top:930px; height:100px; border-radius:20px;
          display:flex; align-items:center; justify-content:center;
          font-size:36px; font-weight:600; }}
</style>
</head>
<body>
<div id="root" data-composition-id="{pid}" data-start="0" data-width="1920" data-height="1080" data-duration="{dur}">
  <section class="clip" id="scene" data-start="0" data-duration="{dur}">
    <div class="bar"><h1 id="t">{title}</h1></div>
    <div class="stage" id="stage">{cards}</div>
    <div class="sub1" id="endline">{end}</div>
    <audio id="vo" src="vo.mp3" data-start="0"></audio>
  </section>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.from("#t", {{ y:-60, opacity:0, duration:0.7, ease:"power3.out" }}, 0.2);
{tweens}
tl.fromTo("#endline", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.6, ease:"power2.out" }}, {endt});
window.__timelines["{pid}"] = tl;
</script>
</body>
</html>"""

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    return float(json.loads(out)["format"]["duration"])

def gen(pid, cfg):
    d = os.path.join(VID, pid)
    os.makedirs(d, exist_ok=True)
    vo = os.path.join(d, "vo.mp3")
    if not os.path.exists(vo):
        subprocess.run(["edge-tts", "--voice", VOICE, "--rate=+10%", "--text", cfg["vo"], "--write-media", vo], check=True)
    dur = probe(vo)
    n = len(cfg["steps"])
    cardw = 560 if n == 4 else 620
    # 卡片布局
    cards, tweens = [], []
    if n == 5:  # 直列（數字＋文字一行）
        pos = [(140, 175 + i * 148) for i in range(5)]
        sizes = [(1500, 125)] * 5
    elif n == 4:  # 菱形
        pos = [(680, 180), (1230, 420), (680, 660), (130, 420)]
        sizes = [(560, 190)] * 4
    else:  # 3 橫排
        pos = [(150, 400), (703, 400), (1256, 400)]
        sizes = [(500, 260)] * 3
    times = [round(1.4 + i * ((dur - 3.2) / max(n, 1)), 2) for i in range(n)]
    for i, ((t1, t2), c) in enumerate(zip(cfg["steps"], cfg["color_seq"])):
        x, y = pos[i]
        w, h = sizes[i]
        if n == 5:
            inner = f'<div class="num">{t1}</div><div class="txt">{t2}</div>'
            cards.append(f'<div class="card row" id="c{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};">{inner}</div>')
        else:
            inner = f'<div class="big">{t1}</div><div class="sub">{t2}</div>'
            cards.append(f'<div class="card" id="c{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};">{inner}</div>')
        tweens.append(f'tl.fromTo("#c{i}", {{ opacity:0, y:50, scale:0.92 }}, {{ opacity:1, y:0, scale:1, duration:0.6, ease:"back.out(1.6)" }}, {times[i]});')
    endt = round(dur - 1.2, 2)
    html = HTML.format(pid=pid, title=cfg["title"], dur=round(dur + 0.8, 2), cardw=cardw,
                       cards="".join(cards), tweens="\n".join(tweens), end=cfg["end"], endt=endt)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return round(dur + 0.8, 2)

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    for pid, cfg in PAGES.items():
        d = gen(pid, cfg)
        print(pid, "duration", d, "s")
