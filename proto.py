# -*- coding: utf-8 -*-
"""HOMEGROWN — кликабельный прототип. Один файл, роутер на data-go."""
import pathlib
ICO = pathlib.Path(__file__).parent / 'icons'

SOLID = pathlib.Path(__file__).parent / 'icons-solid'

# старое имя (Lucide) → файл Phosphor fill. Позволяет не править десятки вызовов.
IMAP = {
 'calendar-days':'calendar-dots', 'sprout':'plant', 'settings-2':'sliders-horizontal',
 'chevron-right':'caret-right', 'search':'magnifying-glass', 'droplets':'drop',
 'repeat':'arrows-clockwise', 'shield':'shield-check', 'circle-check':'check',
 'salad':'leaf', 'leafy-green':'leaf', 'clover':'leaf',
 'apple':'cherries', 'bean':'grains', 'wheat':'grains',
 'sun-dim':'sun', 'camera':'camera', 'leaf':'leaf', 'carrot':'carrot',
 'plus':'plus', 'x':'x', 'check':'check', 'sun':'sun', 'eye':'eye',
 'package':'package', 'scissors':'scissors', 'hand-heart':'hand-heart',
 'lightbulb':'lightbulb', 'trash':'trash',
}

def inner(n):
    f = SOLID / ((IMAP.get(n, n)) + '.svg')
    s = f.read_text()
    body = s[s.index('>', s.index('<svg')) + 1 : s.rindex('</svg>')]
    return ' '.join(body.split())

def ring(pct, dark=False, sz=38, sw=3.2):
    """Кольцо прогресса на SVG — круглые концы, conic-gradient их не умеет."""
    import math
    r = (sz - sw) / 2; circ = 2 * math.pi * r
    off = circ * (1 - max(0, min(100, pct)) / 100)
    track = 'rgba(255,255,255,.20)' if dark else '#DDE3DC'
    col = 'var(--lime)' if dark else 'var(--bright)'
    return (f'<svg aria-hidden="true" width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}">'
            f'<circle cx="{sz/2}" cy="{sz/2}" r="{r}" fill="none" stroke="{track}" stroke-width="{sw}"/>'
            f'<circle cx="{sz/2}" cy="{sz/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{off:.1f}" '
            f'transform="rotate(-90 {sz/2} {sz/2})"/></svg>')

# простые глифы рисуем штрихом: у Phosphor они залитые и читаются как плашки
STROKE_GLYPHS = {
    'check':         'M5 12.8 9.6 17.4 19 8',
    'plus':          'M12 5.5v13M5.5 12h13',
    'x':             'M6.5 6.5 17.5 17.5M17.5 6.5 6.5 17.5',
    'caret-right':   'm9.5 5 7 7-7 7',
    'chevron-right': 'm9.5 5 7 7-7 7',
}

def stroke_ic(n, c='#fff', sz=16, sw=2.4):
    return (f'<svg aria-hidden="true" viewBox="0 0 24 24" width="{sz}" height="{sz}" fill="none" stroke="{c}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{STROKE_GLYPHS[n]}"/></svg>')

def ic(n, c='currentColor', sz=22, sw=None):
    if n in STROKE_GLYPHS:
        return stroke_ic(n, c, sz, float(sw) if sw else 2.4)
    """Solid-иконка Phosphor. sw сохранён в сигнатуре — вызовы его передают, заливке он не нужен."""
    return (f'<svg aria-hidden="true" viewBox="0 0 256 256" width="{sz}" height="{sz}" fill="{c}">{inner(n)}</svg>')

# ───────────────────────────── TOKENS (все проверены на WCAG AA)
T = """
:root{
  --ground:#F2F4F0; --surface:#FFFFFF;
  --ink:#0B1F14;            /* 17.2:1 на белом */
  --ink-2:#3F4A43;          /* 9.2:1  */
  --muted:#5C6660;          /* 6.0:1  */
  --hair:#E4E8E2;
  --primary:#0E7A3C;        /* белый текст 5.43:1 */
  --bright:#22A559;         /* графика: кольца, чек */
  --lime:#B4F461;           /* на тёмном 13.2:1 */
  --deep:#0F3A24;           /* белый текст 12.7:1 */
  --deepest:#0B1F14;
  --flame:#FF7043;          /* на тёмном 6.3:1 */
  /* радиусы: одна лестница по 4px + пилюля */
  --r-xs:8px; --r-sm:10px; --r-md:12px; --r-lg:16px; --r-xl:18px; --r-2xl:20px;
  /* типографическая шкала. Было 31 произвольное значение на 26 экранов. */
  --t-11:11px;   /* микро-лейблы, подписи навигации, легенда */
  --t-12:12px;   /* капшены, календарь, мелкая мета */
  --t-13:13px;   /* вторичная мета, минуты задачи, срок */
  --t-14:14px;   /* мелкий текст, подписи опций, тело заметки */
  --t-15:15px;   /* заголовок строки списка, значение виджета */
  --t-16:16px;   /* тело, опция, кнопка, заголовок секции — минимум для iOS */
  --t-20:20px;   /* вордмарк */
  --t-24:24px;   /* заголовок карточки, цена */
  --t-31:31px;   /* h1 экрана (Caprasimo) */
  --t-40:40px;   /* display на тёмных и full-bleed экранах */
  --n-sm:18px;   /* суффикс числа, значение в ячейке */
  --n-md:36px;   /* число виджета */
  --n-lg:64px;   /* health score */
}
"""

FACES = """@font-face{font-family:'Caprasimo';font-style:normal;font-weight:400;font-display:swap;src:url('fonts/Caprasimo-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;}
@font-face{font-family:'Caprasimo';font-style:normal;font-weight:400;font-display:swap;src:url('fonts/Caprasimo-400-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
@font-face{font-family:'Inter Tight';font-style:normal;font-weight:400;font-display:swap;src:url('fonts/InterTight-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;}
@font-face{font-family:'Inter Tight';font-style:normal;font-weight:400;font-display:swap;src:url('fonts/InterTight-400-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
@font-face{font-family:'Inter Tight';font-style:normal;font-weight:500;font-display:swap;src:url('fonts/InterTight-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;}
@font-face{font-family:'Inter Tight';font-style:normal;font-weight:500;font-display:swap;src:url('fonts/InterTight-400-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
@font-face{font-family:'Inter Tight';font-style:normal;font-weight:600;font-display:swap;src:url('fonts/InterTight-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;}
@font-face{font-family:'Inter Tight';font-style:normal;font-weight:600;font-display:swap;src:url('fonts/InterTight-400-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
@font-face{font-family:'Inter Tight';font-style:normal;font-weight:700;font-display:swap;src:url('fonts/InterTight-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;}
@font-face{font-family:'Inter Tight';font-style:normal;font-weight:700;font-display:swap;src:url('fonts/InterTight-400-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}
"""

CSS = T + FACES + """
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;touch-action:manipulation}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{background:#DDE2DA;font-family:'Inter Tight',system-ui,sans-serif;color:var(--ink);
     display:flex;gap:32px;padding:32px;min-height:100vh}
h1,h2,h3{font-weight:600;letter-spacing:-.015em}
.cap-f{font-family:Caprasimo,Georgia,serif;font-weight:400;letter-spacing:0}

/* ───── левая колонка: телефон */
.stage{position:sticky;top:32px;align-self:flex-start}
.phone{width:390px;height:844px;background:var(--ground);border-radius:44px;overflow:hidden;
       position:relative;box-shadow:0 30px 70px rgba(11,31,20,.28);border:9px solid #0B1F14}
.screen{position:absolute;inset:0;display:none;flex-direction:column;overflow:hidden}
.screen.on{display:flex}
.stage-bar{display:flex;align-items:center;gap:8px;margin-bottom:16px}
.stage-bar .t{font-size:var(--t-15);font-weight:600}
.stage-bar .s{font-size:var(--t-13);color:#5C6660}
.hint{font-size:var(--t-12);color:#5C6660;margin-top:12px;max-width:390px;line-height:1.45}
.hint b{color:var(--ink)}

/* ───── правая колонка: индекс + флоу */
.side{flex:1;min-width:0;padding-bottom:60px}
.side h1{font-size:var(--t-40);line-height:1.05}
.side .lede{font-size:var(--t-15);color:var(--ink-2);line-height:1.55;max-width:760px;margin-top:8px}
.grp{margin-top:24px}
.grp .gt{font-size:var(--t-11);font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:var(--surface);border:0;border-radius:999px;padding:8px 16px;font:500 var(--t-13)/1 'Inter Tight',sans-serif;
      color:var(--ink);cursor:pointer;box-shadow:0 1px 2px rgba(11,31,20,.06)}
.chip:hover{background:var(--lime)}
.chip.act{background:var(--primary);color:#fff}
.tok{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.tk{background:var(--surface);border-radius:var(--r-sm);padding:8px 12px;width:168px}
.tk i{display:block;height:32px;border-radius:var(--r-xs);margin-bottom:8px}
.tk b{font-size:var(--t-12);display:block}
.tk s{font-size:var(--t-11);color:var(--muted);text-decoration:none;display:block;margin-top:2px}
.flow{background:var(--surface);border-radius:var(--r-lg);padding:16px;margin-top:12px;font-size:var(--t-13);line-height:2;color:var(--ink-2)}
.flow b{color:var(--ink);font-weight:600}
.flow code{font:500 var(--t-12) ui-monospace,monospace;background:var(--ground);padding:2px 8px;border-radius:var(--r-xs);color:var(--primary)}

/* ───── app chrome */
.sb{height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 24px;flex:none;
    font-size:var(--t-13);font-weight:600}
.hd{padding:4px 12px 8px;display:grid;grid-template-columns:44px 1fr 44px;align-items:center;
    flex:none;min-height:52px;position:relative;z-index:5;
    background:linear-gradient(180deg,#E4EBE4 0%,#EDF1EB 58%,var(--ground) 100%)}
.hd-l,.hd-r{display:flex;align-items:center;height:44px}
.hd-l{justify-content:flex-start}
.hd-r{justify-content:flex-end}
.hd .wm{text-align:center}
.back{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;flex:none}
.back svg{transform:rotate(180deg)}
.back:active{background:#E6EBE4}
.wm{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:var(--t-20);letter-spacing:.01em;color:var(--primary);line-height:1}
.bd{flex:1;overflow-y:auto;overflow-x:hidden;padding:8px 20px 8px;scrollbar-width:none;min-height:0}
.screen:has(.foot) .bd{padding-bottom:var(--foot-h, 100px)}
.foot{position:absolute;left:0;right:0;bottom:0;padding:8px 20px 24px;background:transparent;
     z-index:22;pointer-events:none}
.foot>*{pointer-events:auto}
.foot .btn{margin-top:0}
.bd::-webkit-scrollbar{display:none}
.greet{font-size:var(--t-14);color:var(--muted);margin-top:16px}
.h1{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:var(--t-31);line-height:1.06;letter-spacing:0;margin-top:8px}
.h1 .m{color:#9EA8A2}
.sl{font-size:var(--t-12);font-weight:600;letter-spacing:-.02em;color:var(--muted);margin:20px 0 8px}

/* ───── ACCENT BLOCK (референс 1) */
.acc{border-radius:var(--r-2xl);padding:20px;margin-top:16px;color:#fff;position:relative;overflow:hidden;
     background:linear-gradient(150deg,#17683C 0%,#0F3A24 52%,#0B1F14 100%)}
.acc:after{content:"";pointer-events:none;position:absolute;width:232px;height:232px;right:-88px;top:-112px;border-radius:50%;
     background:radial-gradient(circle,rgba(180,244,97,.30),rgba(180,244,97,0) 70%)}
.acc .row1{display:flex;justify-content:space-between;align-items:center;position:relative}
.acc .tag{background:var(--lime);color:var(--deepest);font-size:var(--t-11);font-weight:700;letter-spacing:.06em;
     padding:4px 12px;border-radius:999px}
.acc .lbl{font-size:var(--t-13);color:#B7C7BD;margin-top:16px;letter-spacing:-.02em}
.acc .big{font-size:var(--t-31);font-weight:600;letter-spacing:-.02em;line-height:1.05;margin-top:4px}
.acc .sub{font-size:var(--t-13);color:#B7C7BD;margin-top:8px;line-height:1.45}
.acc .duo{display:flex;gap:8px;margin-top:16px}
.acc .cell{flex:1;background:#17492F;border-radius:var(--r-sm);padding:12px 12px}
.acc .cell s{display:block;font-size:var(--t-11);color:#A9BCB0;text-decoration:none;white-space:nowrap}
.acc .cell b{display:block;font-size:var(--n-sm);font-weight:600;margin-top:4px;white-space:nowrap}
.acc .plants{margin-top:16px;position:relative}
.accwhy{margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,.14);position:relative;
        font-size:var(--t-14);line-height:1.5;color:#C2D3C8}
.accwhy b{color:#fff;font-weight:600}
.accwhy .warn{display:block;margin-top:8px;color:var(--lime)}
.acc .prow{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.10)}
.acc .prow:last-child{border-bottom:0}
.acc .prow .nm{flex:1}
.acc .prow .nm b{display:block;font-size:var(--t-15);font-weight:600}
.acc .prow .nm s{display:block;font-size:var(--t-12);color:#A9BCB0;text-decoration:none;margin-top:1px}
.acc .prow .rt{font-size:var(--t-12);color:var(--lime);font-weight:600}
.rw{width:40px;height:40px;flex:none;position:relative;display:flex;align-items:center;justify-content:center}
.rw i{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.acc-photo{height:152px;border-radius:var(--r-2xl);background-size:cover;background-position:center;
           margin:-4px 0 16px;position:relative}

/* ───── карточки, задачи */
.card{background:var(--surface);border-radius:var(--r-lg);padding:16px}
.task{background:var(--surface);border-radius:var(--r-lg);padding:16px;margin-bottom:8px;display:flex;gap:12px;cursor:pointer;align-items:center}
.task:active{transform:scale(.985)}
.box{width:24px;height:24px;border-radius:var(--r-xs);box-shadow:inset 0 0 0 2px #C9D2CC;flex:none;margin-top:1px;
     display:flex;align-items:center;justify-content:center;transition:background .16s,box-shadow .16s}
.box svg{opacity:0;transform:scale(.6);transition:opacity .16s,transform .16s}
.task.done .box{background:var(--bright);box-shadow:none}
.task.done .box svg{opacity:1;transform:scale(1)}
.tt{flex:1}.tt .t{font-size:var(--t-16);font-weight:600;line-height:1.3}
.tt .b{font-size:var(--t-14);color:var(--ink-2);line-height:1.42;margin-top:4px}
.min{font-size:var(--t-13);color:var(--muted);flex:none;margin-top:2px;font-weight:500}
.task.done .t{color:#9EA8A2;text-decoration:line-through;text-decoration-color:#C9D2CC}
.wk{background:var(--surface);border-radius:var(--r-2xl);margin-top:16px;overflow:hidden;
     box-shadow:0 1px 3px rgba(11,31,20,.07)}
.wk-h{padding:16px;cursor:pointer}
.wk.open .wk-h{padding-bottom:4px}
.wk-title{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:var(--t-24);line-height:1.05;
     letter-spacing:0;margin-bottom:12px}
.wk-row{display:flex;align-items:center;gap:10px}
.pb-n{font-size:var(--t-15);font-weight:700;letter-spacing:-.02em;flex:none}
.pb-track{flex:1;height:8px;border-radius:999px;background:#E4E8E2;overflow:hidden;min-width:0}
.pb-track i{display:block;height:100%;background:var(--bright);border-radius:999px;transition:width .3s}
.pb-pct{font-size:var(--t-15);font-weight:700;color:var(--muted);flex:none;letter-spacing:-.02em}
.pb-chev{display:flex;flex:none;transition:transform .2s}
.wk.open .pb-chev{transform:rotate(90deg)}
.wk-list{padding:4px 16px 12px}
.br-row{display:flex;align-items:center;gap:12px;padding:12px 0;cursor:pointer}
.br-dot{width:24px;height:24px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 2px #C9D2CC;
     display:flex;align-items:center;justify-content:center;background:var(--surface)}
.br-dot.on{background:var(--primary);box-shadow:none}
.br-t{flex:1;font-size:var(--t-15);font-weight:600;letter-spacing:-.02em;line-height:1.25;min-width:0}
.br-t s{display:block;font-size:var(--t-13);font-weight:400;color:var(--ink-2);text-decoration:none;
     margin-top:3px;line-height:1.35}
.br-t.done{color:#9EA8A2;text-decoration:line-through;text-decoration-color:#C9D2CC}
.br-m{font-size:var(--t-13);color:var(--muted);flex:none;font-weight:500;align-self:flex-start;margin-top:4px}
.blur{height:12px;border-radius:999px;background:#E1E6E0}

/* ───── кнопки */
.btn{display:flex;align-items:center;justify-content:center;height:52px;border-radius:999px;
     font-size:var(--t-16);font-weight:600;margin-top:12px;cursor:pointer}
.b-pri{background:var(--primary);color:#fff}
.b-lime{background:var(--lime);color:var(--deepest)}
.b-white{background:#fff;color:var(--deepest)}
.b-ghost{background:#E6EBE4;color:var(--ink)}
.pill{display:inline-flex;align-items:center;height:32px;padding:0 16px;border-radius:999px;
      font-size:var(--t-12);font-weight:700;letter-spacing:.04em}

/* ───── навигация */
.nav{height:56px;background:var(--surface);display:flex;padding:6px 4px 0;flex:none;border-top:1px solid var(--hair)}
.ni{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;cursor:pointer;position:relative;color:#8E9A93;padding-top:2px}
.ni span{font-size:var(--t-11);font-weight:600;letter-spacing:.01em}
.ni.on{color:var(--primary)}
.ni.on span{font-weight:700}
.bdg{position:absolute;top:-4px;left:calc(50% + 8px);width:8px;height:8px;border-radius:50%;background:var(--flame)}
.ofr{position:absolute;left:0;right:0;padding:0 12px;cursor:pointer;z-index:20;
     bottom:calc(var(--ofr-bottom, 68px) + env(safe-area-inset-bottom))}
.screen:has(.ofr) .bd{padding-bottom:calc(var(--ofr-bottom, 68px) + 64px)}
.screen:has(.ofr):has(.foot) .bd{padding-bottom:calc(var(--ofr-bottom, 68px) + 64px)}
body.is-pro .ofr{display:none}
.ofr-in{display:flex;align-items:center;gap:12px;border-radius:999px;height:52px;padding:0 8px 0 8px;
        background:var(--lime);position:relative;overflow:hidden;
        box-shadow:0 6px 18px rgba(120,190,40,.34)}
.ofr-ic{width:36px;height:36px;border-radius:50%;background:var(--deepest);display:flex;align-items:center;
        justify-content:center;flex:none;position:relative}
.ofr-tx{flex:1;position:relative}
.ofr-tx b{font-size:var(--t-15);font-weight:700;color:var(--deepest);letter-spacing:-.01em}
.ofr-tx s{font-size:var(--t-15);color:#2C4A1E;text-decoration:none;font-weight:600;opacity:.72;margin-left:8px}
.ofr-go{width:36px;height:36px;border-radius:50%;background:var(--deepest);display:flex;align-items:center;
        justify-content:center;flex:none;position:relative}

/* ───── онбординг */
.pg{display:flex;gap:8px;margin-top:16px}
.pg i{height:4px;flex:1;border-radius:999px;background:#DDE3DC}
.pg i.on{background:var(--primary)}
.opt{background:var(--surface);border-radius:var(--r-lg);padding:16px 16px;margin-bottom:8px;font-size:var(--t-16);min-height:56px;
     font-weight:600;display:flex;justify-content:space-between;align-items:center;cursor:pointer;
     border:2px solid transparent}
.opt s{display:block;font-size:var(--t-13);color:var(--muted);font-weight:400;text-decoration:none;margin-top:4px}
.opt.sel{border-color:var(--primary);background:#EAF5EE}
.opt.sel s{color:var(--ink-2)}
.opt.dim{color:#A6B0AA;pointer-events:none}.opt.dim s{color:#B8C1BB}
.opt-tick{width:24px;height:24px;border-radius:50%;background:var(--primary);display:flex;
          align-items:center;justify-content:center;flex:none;margin-left:12px;
          opacity:0;transform:scale(.65);transition:opacity .14s,transform .14s}
.opt.sel .opt-tick{opacity:1;transform:scale(1)}
.btn.off{background:#DDE3DC;color:#9EA8A2;pointer-events:none;box-shadow:none}
.zip.ph{color:#B4BEB8;letter-spacing:.22em}
.tglrow{cursor:pointer}
.pickrow .picktick{display:none;flex:none}
.pickrow.on .picktick{display:flex}
.pickrow.on .nm b{color:var(--primary)}
.setnote{font-size:var(--t-13);color:var(--muted);line-height:1.45;margin:10px 4px 0;text-wrap:pretty}
.setval{font-size:var(--t-13);color:var(--muted);font-weight:500;flex:none;
     max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
/* удаление аккаунта — выход, а не пункт меню: без плашки, серым */
.danger{margin-top:20px;text-align:center;font-size:var(--t-14);font-weight:600;
     color:var(--muted);cursor:pointer;padding:14px 8px;border-radius:var(--r-xs);min-height:44px;
     display:flex;align-items:center;justify-content:center}
.danger:active{color:var(--ink-2)}
.dangernote{text-align:center;font-size:var(--t-12);color:#9AA49E;line-height:1.4;
     margin:0 16px 8px;text-wrap:pretty}
.tgl{width:48px;height:28px;border-radius:999px;background:#D3DAD4;flex:none;position:relative;
     cursor:pointer;transition:background .18s}
.tgl i{position:absolute;left:4px;top:4px;width:20px;height:20px;border-radius:50%;background:#fff;
       transition:left .18s;box-shadow:0 1px 3px rgba(11,31,20,.22)}
.tgl.on{background:var(--bright)}
.tgl.on i{left:24px}
.is-hidden{display:none}
.screen.onb .nav{display:none}
.screen.onb .ofr{display:none}
.searchrow{display:flex;gap:8px;align-items:center;margin-top:16px}
.search{display:flex;align-items:center;gap:8px;background:var(--surface);border-radius:var(--r-lg);
        padding:0 16px;height:52px;flex:1;min-width:0}
.scanbtn{width:52px;height:52px;flex:none;border-radius:var(--r-lg);background:var(--primary);
        display:flex;align-items:center;justify-content:center;cursor:pointer}
.scanbtn:active{transform:scale(.94)}
.scanhint{font-size:var(--t-13);color:var(--muted);margin-top:10px;line-height:1.4}
.scanhint b{color:var(--primary);font-weight:600;cursor:pointer;
        padding:6px 4px;margin:-6px -4px;border-radius:var(--r-xs)}
/* снимок со скана ждёт, пока человек выберет вид */
.scanwait{display:flex;gap:12px;align-items:center;background:var(--surface);
        border-radius:var(--r-lg);padding:10px;margin-top:12px}
.sw-ph{width:56px;height:56px;flex:none;border-radius:var(--r-md);background-size:cover;
        background-position:center;background-color:#DDE3DC}
.sw-tx b{display:block;font-size:var(--t-15);font-weight:600}
.sw-tx s{display:block;font-size:var(--t-13);color:var(--muted);text-decoration:none;
        margin-top:2px;line-height:1.35}
.search input{flex:1;border:0;outline:0;background:transparent;font:500 var(--t-16) 'Inter Tight',sans-serif;
        color:var(--ink);min-width:0}
.search input::placeholder{color:#9EA8A2;font-weight:400}
.search input::-webkit-search-cancel-button,
.search input::-webkit-search-decoration{-webkit-appearance:none;appearance:none;display:none}
.search .si{display:flex;flex:none}
.search .sx{display:none;cursor:pointer}
.search.has .sx{display:block}
.gsec{font-size:var(--t-12);font-weight:600;letter-spacing:-.02em;color:var(--muted);margin:20px 0 8px}
.empty{text-align:center;color:var(--muted);font-size:var(--t-14);padding:24px 8px;line-height:1.5}
.pl.have{opacity:.55}
.empty-hero{position:relative;border-radius:var(--r-2xl);overflow:hidden;height:560px;margin-top:8px}
.eh-shot{position:absolute;inset:0;background-size:cover;background-position:center}
.eh-ov{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:24px;
      background:linear-gradient(180deg,rgba(11,31,20,.10) 0%,rgba(11,31,20,.20) 40%,rgba(11,31,20,.88) 100%)}
.eh-k{font-size:var(--t-13);font-weight:600;color:var(--lime);letter-spacing:-.02em}
.eh-h{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:var(--t-31);line-height:1.04;color:#fff;margin-top:8px}
.eh-alt{text-align:center;font-size:var(--t-14);font-weight:600;color:#DCE7DE;margin-top:4px;
     cursor:pointer;padding:14px 8px;border-radius:var(--r-xs)}
.tlink2{font-size:var(--t-14);color:var(--muted);text-align:center;font-weight:600;
     cursor:pointer;padding:12px 8px;min-height:44px;display:flex;align-items:center;
     justify-content:center;border-radius:var(--r-xs)}
.tlink2:active{color:var(--ink-2)}
.tlink{font-size:var(--t-14);color:#fff;text-align:center;margin-top:8px;cursor:pointer;
     font-weight:600;padding:14px 8px;border-radius:var(--r-xs);min-height:44px;
     display:flex;align-items:center;justify-content:center}
.score{position:relative;border-radius:var(--r-2xl);overflow:hidden;margin-top:8px;min-height:240px;
      display:flex;align-items:flex-end;background:var(--deepest)}
.score-ph{position:absolute;inset:0;background-size:cover;background-position:center}
/* градиент снизу вверх: фото остаётся фотографией, текст читается */
.score-sc{position:absolute;inset:0;background:linear-gradient(180deg,
      rgba(11,31,20,0) 0%,rgba(11,31,20,.14) 34%,rgba(11,31,20,.62) 64%,
      rgba(11,31,20,.90) 84%,rgba(11,31,20,.96) 100%)}
.score-in{position:relative;padding:20px;width:100%}
.score-row{display:flex;align-items:center;gap:14px}
.score-top{display:flex;align-items:center;justify-content:center;width:56px;height:56px;
      position:relative;flex:none}
.score-top span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.score-n{display:flex;align-items:baseline;gap:2px;color:#fff}
.score-n b{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:var(--t-40);line-height:1}
.score-n s{font-size:var(--t-16);text-decoration:none;color:#A9BCB0}
.score-v{font-size:var(--t-16);font-weight:700;color:var(--lime);letter-spacing:-.02em;margin-top:2px}
.score-s{font-size:var(--t-14);color:#D2DFD6;line-height:1.35;margin-top:10px}
.sec-h{display:flex;align-items:baseline;justify-content:space-between;margin:20px 0 10px}
.sec-h span{font-size:var(--t-16);font-weight:600;letter-spacing:-.02em}
.sec-h i{font-style:normal;font-size:var(--t-14);font-weight:600;color:var(--primary);
     cursor:pointer;padding:14px 10px;margin:-14px -10px;border-radius:var(--r-xs)}
.prow-scroll{display:flex;gap:10px;overflow-x:auto;scrollbar-width:none;margin:0 -20px;padding:0 20px 4px}
.prow-scroll::-webkit-scrollbar{display:none}
.plcard{width:158px;flex:none;background:var(--surface);border-radius:var(--r-2xl);padding:8px;cursor:pointer}
.plcard-ph{aspect-ratio:1;border-radius:var(--r-sm);background-size:cover;background-position:center;position:relative}
.plcard-fav{position:absolute;right:6px;top:6px;width:26px;height:26px;border-radius:50%;
      background:rgba(11,31,20,.55);display:flex;align-items:center;justify-content:center}
.plcard b{display:block;font-size:var(--t-14);font-weight:600;margin:8px 4px 0;letter-spacing:-.02em;
      line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.plcard s{display:block;font-size:var(--t-12);text-decoration:none;margin:3px 4px 4px;font-weight:600;
      white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.st-ok{color:var(--primary)}.st-warn{color:#B8860B}.st-bad{color:#C2410C}
.wgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
.wg{border-radius:var(--r-2xl);padding:16px;min-width:0}
.wg.span2{grid-column:1 / -1}
.wg-lite{background:var(--surface)}
.wg-dark{background:var(--deepest);color:#fff}
.wg-top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px}
.wg .num{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:var(--n-md);line-height:1;letter-spacing:-.02em}
.wg .num span{font-size:var(--n-sm);margin-left:2px}
.wg .lbl{font-size:var(--t-13);color:var(--muted);margin-top:8px;letter-spacing:-.02em}
.wg-dark .lbl{color:#A9BCB0}
.wg-h{display:flex;align-items:baseline;justify-content:space-between;gap:8px}
.wg-h b{font-size:var(--t-15);font-weight:600;letter-spacing:-.02em}
.wg-h s{font-size:var(--t-12);color:var(--muted);text-decoration:none}
.wg-dark .wg-h s{color:#A9BCB0}
.mrow{display:flex;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid var(--hair)}
.wg-dark .mrow{border-top-color:rgba(255,255,255,.14)}
.mrow>div{flex:1;min-width:0}
.mrow s{display:block;font-size:var(--t-11);color:var(--muted);text-decoration:none;letter-spacing:-.02em}
.wg-dark .mrow s{color:#A9BCB0}
.mrow b{display:block;font-size:var(--t-15);font-weight:600;margin-top:2px;letter-spacing:-.02em}
.calyear{display:grid;grid-template-columns:repeat(12,1fr);gap:3px;margin-top:12px}
.calyear i{height:30px;border-radius:5px;background:#F0F3EF;font-style:normal;
     font-size:var(--t-11);font-weight:600;color:var(--muted);display:flex;
     align-items:flex-end;justify-content:center;padding-bottom:3px}
.calyear i.c-sow{background:#B9E3C6;color:#0E6234}
.calyear i.c-pick{background:var(--primary);color:#fff}
.calyear i.c-both{background:linear-gradient(180deg,#B9E3C6 0 55%,var(--primary) 55% 100%);color:#fff}
.calyear i.cnow{box-shadow:inset 0 0 0 1.5px var(--deep)}
.calcta{margin-top:12px;padding-top:12px;border-top:1px solid var(--hair);
     font-size:var(--t-13);font-weight:600;color:var(--primary)}
.calleg2{display:flex;gap:14px;flex-wrap:wrap;font-size:var(--t-12);color:var(--muted);
     margin-bottom:10px}
.calleg2 span{display:flex;align-items:center;gap:5px}
.calleg2 i{width:12px;height:12px;border-radius:3px;flex:none;font-style:normal}
.calbox{background:var(--surface);border-radius:var(--r-lg);padding:10px 12px}
.calrow{display:flex;align-items:center;gap:8px;padding:3px 0}
.calrow b{flex:0 0 92px;font-size:var(--t-13);font-weight:600;letter-spacing:-.02em;
     white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cal12{display:grid;grid-template-columns:repeat(12,1fr);gap:2px;flex:1;min-width:0}
.cal12 i{height:16px;border-radius:3px;background:#F0F3EF;font-style:normal}
.cal12 i.c-sow{background:#B9E3C6}
.cal12 i.c-pick{background:var(--primary)}
.cal12 i.c-both{background:linear-gradient(180deg,#B9E3C6 0 55%,var(--primary) 55% 100%)}
.calleg2 i.c-both{background:linear-gradient(180deg,#B9E3C6 0 55%,var(--primary) 55% 100%)}
.cal12 i.c-any{background:#DCE7DE}
.calhead b{flex:0 0 92px}
.calhead .cal12 i{background:transparent;font-size:var(--t-11);color:var(--muted);
     text-align:center;line-height:16px;font-weight:600}
.calhead .cal12 i.cnow{color:var(--primary);font-weight:700}
.cal12 i.cnow{box-shadow:inset 0 0 0 1.5px var(--deep)}
.calleg2 i.cnow{background:#F0F3EF;box-shadow:inset 0 0 0 1.5px var(--deep)}
.ccard{background:var(--surface);border-radius:var(--r-lg);padding:12px;margin-bottom:8px}
.chead{display:flex;align-items:center;gap:12px;cursor:pointer;padding:4px}
.chead .nm b{display:block;font-size:var(--t-16);font-weight:600;letter-spacing:-.02em}
.chead .nm s{display:block;font-size:var(--t-13);color:var(--muted);text-decoration:none;margin-top:2px}
.cstrip{display:flex;gap:4px;margin-top:8px;overflow-x:auto;scrollbar-width:none;
      overscroll-behavior-inline:contain;scroll-snap-type:x proximity}
.cstrip::-webkit-scrollbar{display:none}
.cstrip>div{flex:0 0 calc(25% - 3px);aspect-ratio:1;border-radius:var(--r-sm);background-size:cover;
      background-position:center;background-color:#DDE3DC;scroll-snap-align:start}
.st-pill{background:#EAF5EE}
.st-pill.st-warn{background:#FDF3E0}.st-pill.st-bad{background:#FDEBE2}
.cempty{display:flex;align-items:center;gap:8px;margin-top:8px;padding:12px;border-radius:var(--r-sm);
        background:var(--ground);color:var(--muted);font-size:var(--t-13);font-weight:600;cursor:pointer}
.cempty svg{flex:none}
.jgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.jc{background:var(--surface);border-radius:var(--r-lg);padding:8px;margin:0}
.jph{aspect-ratio:1;border-radius:var(--r-sm);background-size:cover;background-position:center;background-color:#DDE3DC}
.jc figcaption{padding:8px 4px 4px}
.jc figcaption b{display:block;font-size:var(--t-14);font-weight:600;line-height:1.2}
.jc figcaption s{display:block;font-size:var(--t-12);color:var(--muted);text-decoration:none;margin-top:2px}
.btn-dash{height:48px;border-radius:999px;border:2px dashed var(--primary);color:var(--primary);
       display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px;
       font-size:var(--t-15);font-weight:700;cursor:pointer}
.btn-dash svg{fill:var(--primary)}
.btn-dash:active{background:#EAF5EE}
#toast{position:absolute;left:12px;right:12px;top:calc(8px + env(safe-area-inset-top));background:var(--deepest);color:#fff;
       border-radius:var(--r-lg);padding:16px 16px;display:flex;justify-content:space-between;align-items:center;
       font-size:var(--t-14);opacity:0;transform:translateY(-12px);pointer-events:none;
       transition:opacity .22s ease-out,transform .22s cubic-bezier(.32,.72,0,1);z-index:70}
#toast.on{opacity:1;transform:none;pointer-events:auto}
#toast b{color:var(--lime);font-weight:700;cursor:pointer}
.zip{background:var(--surface);border-radius:var(--r-lg);padding:16px 16px;font-size:var(--t-31);font-weight:700;letter-spacing:.08em}

/* ───── full-bleed фото */
.shot{position:absolute;inset:0;background-size:cover;background-position:center}
.scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,31,20,.55) 0%,rgba(11,31,20,.05) 32%,rgba(11,31,20,.82) 72%,rgba(11,31,20,.96) 100%)}
.overlay{position:absolute;inset:0;display:flex;flex-direction:column;padding:24px 24px;color:#fff}

/* ───── тёмный экран (paywall / harvest) */
.scan-shot{position:absolute;inset:0;background:#0B1F14 center/cover no-repeat}
.scan-ov{position:absolute;inset:0;display:flex;flex-direction:column;padding:24px 20px;
     padding-top:calc(24px + env(safe-area-inset-top))}
.mile-ov{padding-top:calc(24px + env(safe-area-inset-top))}
.scan-frame{flex:1;border-radius:var(--r-2xl);box-shadow:inset 0 0 0 3px rgba(180,244,97,.7);margin-bottom:16px;
     position:relative;animation:scanpulse 1.2s ease-in-out infinite}
.scan-frame.ok{box-shadow:inset 0 0 0 3px var(--lime);animation:none}
@keyframes scanpulse{0%,100%{box-shadow:inset 0 0 0 3px rgba(180,244,97,.35)}
     50%{box-shadow:inset 0 0 0 3px rgba(180,244,97,.9)}}
.scan-foot{background:var(--deepest);border-radius:var(--r-2xl);padding:20px;color:#fff;flex:none}
.scan-foot b{display:block;font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:var(--t-24);line-height:1.05}
.scan-foot s{display:block;font-size:var(--t-14);color:#A9BCB0;text-decoration:none;margin-top:8px;line-height:1.4}
.scan-foot s em{color:#CFE0D4;font-style:italic}
.scan-dots{display:flex;gap:6px;margin-bottom:12px}
.scan-dots i{width:8px;height:8px;border-radius:50%;background:var(--lime);opacity:.35;
     animation:dot 1s infinite}
.scan-dots i:nth-child(2){animation-delay:.15s}.scan-dots i:nth-child(3){animation-delay:.3s}
@keyframes dot{0%,100%{opacity:.35}50%{opacity:1}}
.dark{position:absolute;inset:0;background:var(--deepest);padding:24px 24px;display:flex;flex-direction:column;color:#fff;overflow-y:auto;overflow-x:hidden;scrollbar-width:none}
.dark::-webkit-scrollbar{display:none}
/* Свечение раньше было блоком 420px со сдвигом за границу экрана — из-за него
   тёмные экраны распирало по горизонтали. Тот же самый визуал, но градиентом
   внутри границ: центр за кадром, переполнения нет. */
.glow{position:absolute;inset:0;pointer-events:none;
      background:radial-gradient(circle 210px at 150px 58px,
                 rgba(180,244,97,.34),rgba(180,244,97,0) 68%)}
.glow.b{background:radial-gradient(circle 170px at calc(100% + 30px) 450px,
                 rgba(34,165,89,.34),rgba(34,165,89,0) 68%)}
.xbtn{width:44px;height:44px;border-radius:50%;background:#1B3527;display:flex;align-items:center;
      justify-content:center;cursor:pointer;flex:none}
.seg{display:flex;background:#152B1F;border-radius:999px;padding:4px;margin:16px auto 0;width:fit-content;position:relative}
.seg div{height:44px;display:flex;align-items:center;padding:0 26px;border-radius:999px;font-size:var(--t-14);font-weight:600;cursor:pointer;color:#9DB0A4}
.seg div.on{background:var(--lime);color:var(--deepest)}
.pcard{border-radius:var(--r-xl);padding:20px;margin-top:16px;background:#122A1D;border:1.5px solid var(--lime);position:relative}
.pcard .pr{font-size:var(--t-24);font-weight:700}
.pcard .pn{font-size:var(--t-13);color:#A9BCB0;line-height:1.45;margin-top:8px}
.feat{margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,.12)}
.feat div{display:flex;align-items:flex-start;gap:8px;font-size:var(--t-14);margin-bottom:12px;color:#E4EEE6}
.feat i{width:8px;height:8px;border-radius:50%;background:var(--lime);flex:none;margin-top:8px}
.stat{background:#122A1D;border-radius:var(--r-lg);padding:16px}
.stat b{font-size:var(--n-md);font-weight:600;display:block;line-height:1}
.stat s{font-size:var(--t-12);color:#A9BCB0;text-decoration:none;display:block;margin-top:8px;line-height:1.35}
.sg2{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:16px}

/* ───── прочее */
.plist{background:var(--surface);border-radius:var(--r-lg);padding:4px 16px}
.pl{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--hair);cursor:pointer}
.pl:last-child{border-bottom:0}

.nm{flex:1}.nm b{display:block;font-size:var(--t-15);font-weight:600}
.nm s{display:block;font-size:var(--t-13);color:var(--muted);text-decoration:none;margin-top:1px}
.eta{font-size:var(--t-13);color:var(--muted);font-weight:500}
.addbtn{width:32px;height:32px;border-radius:50%;background:#E6EFE8;display:flex;align-items:center;
        justify-content:center;flex:none}
/* диск с иконкой вида. Раньше здесь стояло кольцо прогресса на 0% —
   пустой кружок, который ничего не означал в контексте библиотеки. */
.spic{width:40px;height:40px;flex:none;border-radius:50%;background:#EDF3EE;
      display:flex;align-items:center;justify-content:center}
.spic svg{width:20px;height:20px}
.spic.has{background-size:cover;background-position:center;background-color:#DDE3DC}
.acc .spic{background:rgba(255,255,255,.10)}
.acc .spic svg{fill:var(--lime)}
.addbtn svg:last-child{display:none}
.pl.added .addbtn{background:var(--bright)}
.pl.added .addbtn svg:first-child{display:none}
.pl.added .addbtn svg:last-child{display:block}
.pl.locked{opacity:.42;pointer-events:none}
.note{background:var(--surface);border-radius:var(--r-lg);padding:16px}
.note b{font-size:var(--t-16);font-weight:600;display:block;line-height:1.3}
.quote{background:var(--surface);border-radius:var(--r-lg);padding:16px;margin-top:16px;position:relative}
.quote .qmark{font-family:Caprasimo,Georgia,serif;font-size:var(--t-40);line-height:.7;color:var(--bright);
              opacity:.32;height:24px}
.quote p{font-size:var(--t-15);line-height:1.45;color:var(--ink);margin-top:4px}
.qwho{display:flex;align-items:center;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid var(--hair)}
.qav{width:36px;height:36px;border-radius:50%;background:var(--deepest);color:var(--lime);flex:none;
     display:flex;align-items:center;justify-content:center;font-size:var(--t-12);font-weight:700;letter-spacing:.04em}
.qwho b{display:block;font-size:var(--t-14);font-weight:600}
.qwho s{display:block;font-size:var(--t-12);color:var(--muted);text-decoration:none;margin-top:2px}
.note p{font-size:var(--t-14);color:var(--ink-2);line-height:1.45;margin-top:8px}

/* ───── фокус с клавиатуры: раньше его не было нигде */
:focus-visible{outline:3px solid var(--primary);outline-offset:2px;border-radius:var(--r-xs)}
.dark :focus-visible,.overlay :focus-visible,.scan-ov :focus-visible,.mile-ov :focus-visible,
.acc :focus-visible,.score :focus-visible,.wg-dark :focus-visible{outline-color:var(--lime)}
.nav :focus-visible{outline-offset:-3px}

/* ───── отклик на нажатие: было на трёх элементах из двадцати четырёх */
.btn:active,.btn-dash:active,.opt:active,.pl:active,.plcard:active,.chead:active,
.br-row:active,.chip:active,.ofr:active .ofr-in,.zip:active,.seg div:active,
.cempty:active,.ccard:active .chead{transform:scale(.985)}
.ni:active{opacity:.6}
.xbtn:active{transform:scale(.92)}
.btn,.btn-dash,.opt,.pl,.plcard,.chead,.br-row,.ofr-in,.xbtn,.zip,.seg div{
     transition:transform .16s cubic-bezier(.32,.72,0,1),background-color .16s ease-out,
                opacity .16s ease-out}

/* ───── цифры не должны прыгать по ширине при пересчёте */
.wg .num,.acc .huge,.acc .cell b,.score-n b,.stat b,.pcard .pr,.mrow b,
.pb-n,.pb-pct,.min,.br-m,.eta,.zip,.acc .prow .rt{font-variant-numeric:tabular-nums}

/* ───── висячие слова в заголовках и хвосты в абзацах */
.h1,.acc .big,.eh-h,.mile-h,.recap-h,.done-h,.wk-title,.scan-foot b,.a2-h{text-wrap:balance}
.note p,.acc .sub,.mile-s,.recap-s,.score-s,.opt s,.quote p,.accwhy,.tt .b,
.empty,.scan-foot s,.br-t s{text-wrap:pretty}

/* ───── скролл внутри экрана не должен тянуть страницу за собой */
.bd,.dark,.prow-scroll{overscroll-behavior:contain}

/* ───── уважение к системной настройке «меньше движения» */
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;
       transition-duration:.01ms!important}
}

/* ───── крупное число в акцентном блоке (Growth · health score) */
.acc .huge{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:var(--n-lg);line-height:.96;
     letter-spacing:-.01em}
.scorehead{display:flex;align-items:baseline;gap:8px;margin-top:2px;position:relative}
.huge-of{font-size:var(--t-15);color:#A9BCB0;font-weight:500}
/* полоса прогресса переехала сюда из отдельного виджета Plant health,
   который показывал то же самое число второй раз */
.accbar{margin-top:14px;height:10px;background:rgba(255,255,255,.16);position:relative}
.accbar i{background:var(--lime)}

/* ───── плитка вместо фотографии: у вида нет настоящего снимка, врать нечем */
.no-ph{position:relative;overflow:hidden}
.no-ph .ph-ic{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.no-ph .ph-ic svg{width:52%;height:52%}
.det-ph{height:220px;border-radius:var(--r-2xl);background-size:cover;background-position:center}

/* ───── экран-момент (milestone) */
.mile-scrim{height:58%;background:linear-gradient(180deg,rgba(11,31,20,.45),
     rgba(11,31,20,0) 40%,var(--deepest))}
.mile-ov{position:absolute;inset:0;display:flex;flex-direction:column;padding:24px}
.mile-h{font-size:var(--t-40);line-height:1.02;margin-top:12px;color:#fff}
.mile-s{font-size:var(--t-16);color:#C6D6CA;line-height:1.5;margin-top:12px}
.mile-tx{position:relative;margin-top:auto}

/* ───── итог года и «неделя закрыта» */
.recap-in{flex:1;display:flex;flex-direction:column;justify-content:center;position:relative}
.recap-ph{height:200px;border-radius:var(--r-xl);background-size:cover;background-position:center;
     background-color:#122A1D}
.recap-h{font-size:var(--t-40);line-height:1.02;margin-top:12px}
.recap-s{font-size:var(--t-16);color:#A9BCB0;line-height:1.5;margin-top:12px}
.done-h{font-size:var(--t-31);font-weight:600;line-height:1.15;margin-top:12px;letter-spacing:-.02em}
"""

# ───────────────────────────── helpers
SCR = []
def screen(sid, html, title, note, group):
    SCR.append(dict(id=sid, html=html, title=title, note=note, group=group))

def sb():
    return ('<div class="sb"><span>9:41</span><span style="letter-spacing:.06em">' +
            ic('sun', 'var(--ink)', 15, '2') + '</span></div>')

NAVI = [('Week', 'calendar-days', 'home'), ('Growth', 'camera', 'growth'),
        ('Settings', 'settings-2', 'settings')]
def nav(active='Week', badge=False):
    out = []
    for name, icon, target in NAVI:
        on = ' on' if name == active else ''
        cur = ' aria-current="page"' if name == active else ''
        b = '<div class="bdg" aria-hidden="true"></div>' if (badge and name == 'Week') else ''
        out.append(f'<div class="ni{on}" role="link" tabindex="0"{cur} data-go="{target}">'
                   f'{b}{ic(icon, "currentColor", 23)}<span>{name}</span></div>')
    return '<nav class="nav" aria-label="Main">' + ''.join(out) + '</nav>'

def hd(initial=None, back=None):
    """Шапка: лого всегда по центру, «назад» слева, аватар справа."""
    left = (f'<div class="back" role="button" tabindex="0" aria-label="Back" '
            f'data-go="{back}">{ic("caret-right", "var(--ink)", 20)}</div>'
            if back else '')
    right = ''
    return (f'<div class="hd"><div class="hd-l">{left}</div>'
            f'<div class="wm">HOMEGROWN</div>'
            f'<div class="hd-r">{right}</div></div>')

def ofr(txt='Unlock the full care plan', sub='$29/yr', go='paywall'):
    return (f'<div class="ofr" role="button" tabindex="0" data-go="{go}"><div class="ofr-in">'
            f'<div class="ofr-ic">{ic("sprout", "var(--lime)", 19, "2")}</div>'
            f'<div class="ofr-tx"><b>{txt}</b><s>{sub}</s></div>'
            f'<div class="ofr-go">{ic("chevron-right", "var(--lime)", 18, "2.4")}</div>'
            f'</div></div>')

def task(t, mins, body=None, done=False, lock=False):
    if lock:
        return ('<div class="task"><div class="box"></div><div class="tt">'
                '<div class="blur" style="width:76%;margin-bottom:8px"></div>'
                '<div class="blur" style="width:52%"></div></div>'
                f'<div class="min">{mins}</div></div>')
    b = f'<div class="b">{body}</div>' if body else ''
    return (f'<div class="task{" done" if done else ""}" role="checkbox" tabindex="0" '
            f'aria-checked="{"true" if done else "false"}" data-task>'
            + '<div class="box">' + ic('check', '#fff', 16, '3') + '</div>'
            + f'<div class="tt"><div class="t">{t}</div>{b}</div>'
            + f'<div class="min">{mins}</div></div>')

def ringrow(icon, name, sub, right, pct, dark=False, go=None, pick=False):
    g = ' data-add' if pick else (f' data-go="{go}"' if go else '')
    col = 'var(--lime)' if dark else 'var(--primary)'
    rr = f'<div class="rw">{ring(pct, dark)}<i>{ic(icon, col, 15, "1.9")}</i></div>' 
    role = ' role="button" tabindex="0"' if (go or pick) else ''
    if dark:
        return (f'<div class="prow"{role}{g}>{rr}'
                f'<div class="nm"><b>{name}</b><s>{sub}</s></div><div class="rt">{right}</div></div>')
    rt = (f'<div class="addbtn">{ic("plus","var(--primary)",17,"2.4")}'
          f'{ic("check","#fff",17,"3")}</div>') if pick else f'<div class="eta">{right}</div>'
    return (f'<div class="pl"{role}{g}>{rr}'
            f'<div class="nm"><b>{name}</b><s>{sub}</s></div>{rt}</div>')

def opt(label, sub=None, next=None, multi=False):
    """Опция онбординга. Ни одна не выбрана заранее — состояние появляется от тапа."""
    s = f'<s>{sub}</s>' if sub else ''
    attr = ' data-multi' if multi else f' data-single data-next="{next}"'
    role = 'checkbox' if multi else 'radio'
    return (f'<div class="opt" role="{role}" tabindex="0" aria-checked="false"{attr}>'
            f'<div>{label}{s}</div>'
            f'<div class="opt-tick">{ic("check", "#fff", 14, "3")}</div></div>')

def foot(html):
    """Подвал экрана: прибит к низу, не скроллится вместе с контентом."""
    return f'<div class="foot">{html}</div>'

IMG = 'img/'

# ═════════════════════════════ 1. ОНБОРДИНГ
screen('landing',
 f'{sb()}<div class="shot" style="background-image:url({IMG}hero-farm.jpg);top:48px"></div>'
 '<div class="scrim" style="top:48px"></div>'
 '<div class="overlay" style="top:48px">'
 '<div class="wm" style="color:#fff">HOMEGROWN</div>'
 '<div style="flex:1"></div>'
 '<div class="cap-f" style="font-size:var(--t-40);line-height:1.02">Keep every plant<br>'
 '<span style="color:var(--lime)">alive and growing</span></div>'
 '<div style="font-size:var(--t-16);line-height:1.5;margin-top:16px;color:#DCE7DE">'
 'Radishes in a pot, basil on the sill, a monstera in the corner. Tell us what you have and '
 'how much light it gets &mdash; we&rsquo;ll tell you exactly what it needs this week.</div>'
 '<div class="btn b-lime" style="margin-top:24px" data-go="q0">Get started free</div>'
 '<div style="font-size:var(--t-13);color:#C3D2C7;text-align:center;margin-top:12px">No card. Takes 90 seconds.</div></div>',
 'Landing', 'Фото на весь экран, лайм-кнопка. Никаких попапов и логина — §4.2. '
 'Обещание больше не про еду: продукт про растения в целом.', 'Онбординг')

screen('q0',
 f'{sb()}{hd(back="landing")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Where are you<br>starting from?</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);margin-top:4px">'
 'Two very different jobs, so we ask different things.</div>'
 '<div class="pg" data-pg></div>'
 '<div style="margin-top:16px">' +
 opt('I already have plants', 'Get them on a care schedule', next='add-plant') +
 opt('I want to start growing', 'Tell me what to plant and buy', next='qwhat') + '</div></div>',
 'Q0 · Старт', 'Развилка, которой раньше не было. Приложение — трекер ухода, а онбординг строил '
 '<b>план посадки</b>: человеку с готовой монстерой пять вопросов про то, что сажать, были '
 'бесполезны. Теперь «уже есть» ведёт сразу в библиотеку со сканом, а «хочу начать» — в план. '
 'Обе ветки сходятся на Home. Начало онбординга <b>обнуляет MY_PLANTS</b>: демо-набор больше '
 'не притворяется твоими растениями.', 'Онбординг')

screen('qwhat',
 f'{sb()}{hd(back="q0")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">What are you growing?</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);margin-top:4px">'
 'This decides the rest of the questions.</div>'
 '<div class="pg" data-pg></div>'
 '<div style="margin-top:16px">' +
 opt('Something to eat', 'Radishes, greens, tomatoes in pots', next='q1') +
 opt('Houseplants', 'Monstera, pothos, snake plant', next='q1') +
 opt('Both', 'Something edible, plants inside too', next='q1') + '</div></div>',
 'Q1 · Track', 'Тот же вопрос, что был первым, но теперь его видит только ветка «хочу начать». '
 'Кто уже держит растения, трек не выбирает — он выводится из того, что человек занёс.', 'Онбординг')

screen('q1',
 f'{sb()}{hd(back="q0")}<div class="bd">'
 '<div class="h1" id="q1head" style="margin-top:16px">Where will it live?</div>'
 '<div class="pg" data-pg></div>'
 '<div id="q1opts" style="margin-top:16px"></div></div>',
 'Q1 · Space', 'Варианты рендерятся из трека: комнаты для house, площадки для edible, смесь для both. '
 'Уличное место включает <b>outdoor</b> — только тогда спрашиваем ZIP и заморозки.', 'Онбординг')

screen('q2',
 f'{sb()}{hd(back="q1")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">What&rsquo;s your ZIP?</div>'
 '<div class="pg" data-pg></div>'
 '<div style="margin-top:16px">'
 '<div class="zip ph" role="button" tabindex="0" aria-label="Enter your ZIP code" data-zip>'
 '&mdash; &mdash; &mdash; &mdash; &mdash;</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);line-height:1.5;margin-top:16px">'
 'Frost dates decide what you can put outside right now. Tap to enter.</div>'
 '<div class="acc is-hidden" data-zipres style="margin-top:16px"><div class="row1"><span class="tag">Matched</span></div>'
 '<div class="lbl">Climate profile</div><div class="big" id="zipcity">&nbsp;</div>'
 '<div class="duo"><div class="cell"><s>Last frost</s><b id="zipfrost">&nbsp;</b></div>'
 '<div class="cell"><s>Season</s><b id="zipseason">&nbsp;</b></div></div></div>'
 '</div></div>' + foot('<div class="btn b-pri off" data-cta data-go="q3">Continue</div>'),
 'Q2 · ZIP', 'Спрашивается <b>только на уличном треке</b>. Комнатным растениям заморозки не нужны, '
 'поэтому indoor этот экран не видит вообще.', 'Онбординг')

screen('q3',
 f'{sb()}{hd(back="q2")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">How much direct sun<br>does that spot get?</div>'
 '<div class="pg" data-pg></div>'
 '<div style="margin-top:16px">' +
 opt('3&ndash;5 hours', 'Mostly shade or morning sun', next='q4') +
 opt('6&ndash;8 hours', 'Good sun most of the day', next='q4') +
 opt('8+ hours', 'Full blazing sun', next='q4') +
 opt('Not sure yet', 'We&rsquo;ll start you safe and check later', next='q4') + '</div></div>',
 'Q3 · Sun', 'Главный фильтр качества плана, только для уличного трека. not_sure → ранг 1 + задача Sun check.', 'Онбординг')

screen('q2i',
 f'{sb()}{hd(back="q1")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">How bright is<br>that spot?</div>'
 '<div class="pg" data-pg></div>'
 '<div style="margin-top:16px">' +
 opt('South window', 'Brightest &mdash; aloe and basil work here', next='q4') +
 opt('East or West', 'Good for most houseplants and herbs', next='q4') +
 opt('North window', 'Low light &mdash; pothos, ZZ, snake plant', next='q4') +
 opt('Not sure', 'We&rsquo;ll start you safe', next='q4') + '</div>'
 '<div class="card" style="margin-top:12px;display:flex;gap:12px;align-items:center">' +
 ic('lightbulb', 'var(--primary)', 24) +
 '<div style="font-size:var(--t-14);color:var(--ink-2);line-height:1.4">Got a grow light? '
 '<b style="color:var(--ink)">Tell us</b> &mdash; it upgrades your options.</div></div></div>',
 'Q2-indoor · Light', 'Внутри света меряется <b>стороной окна</b>, не часами. Ложится в тот же sunRank, '
 'движок один. Это экран всего indoor — и комнатных, и подоконниковых съедобных.', 'Онбординг')

screen('q4',
 f'{sb()}{hd(back="q3")}<div class="bd">'
 '<div class="h1" id="q4head" style="margin-top:16px">What are you after?</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);margin-top:4px">Up to 3 &middot; '
 '<span data-count>nothing selected yet</span></div>'
 '<div class="pg" data-pg></div>'
 '<div id="q4opts" style="margin-top:16px"></div>'
 '</div>' + foot('<div style="font-size:var(--t-13);color:var(--muted);margin-bottom:8px;text-align:center" data-hint>'
 'Pick at least one.</div><div class="btn b-pri off" data-cta data-go="q5">Continue</div>'),
 'Q4 · Goals', 'Варианты из трека: комнатные спрашивают «hard to kill / low light / statement», '
 'съедобные — «salads / herbs / tomatoes». Лимит 3, лишние <b>гаснут, а не исчезают</b> — §4.6.', 'Онбординг')

screen('q5',
 f'{sb()}{hd(back="q4")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">How much time can<br>you give it?</div>'
 '<div class="pg" data-pg></div>'
 '<div id="q5opts" style="margin-top:16px"></div></div>',
 'Q5 · Effort', 'Определяет размер плана: 3 / 4 / 5&ndash;6 растений. Слово в подписи меняется по треку.', 'Онбординг')

screen('preview',
 f'{sb()}{hd(back="q5")}<div class="bd">'
 '<div class="greet">Your plan is ready</div>'
 '<div class="cap-f" id="planhead" style="font-size:var(--t-31);line-height:1.06;margin-top:4px">4 plants.</div>'
 '<div style="font-size:var(--t-13);color:var(--muted);margin-top:8px" id="planmeta">&nbsp;</div>'
 '<div class="quote" id="planquote"></div>'
 '<div class="acc"><div class="row1"><span class="tag">Your plan</span></div>'
 '<div class="plants" id="planrows"></div>'
 '<div class="accwhy" id="planwhy"></div></div>'
 '</div>' + foot('<div class="btn b-pri" data-planadd>Add these plants</div>'
 '<div class="tlink2" data-planskip>I&rsquo;ll pick my own</div>')
 + ofr('See the whole calendar', '$29/yr'),
 'Plan Preview', '⚠ Цитата — <b>плейсхолдер</b>: настоящий отзыв надо получить у реального человека '
 'с его согласия, выдумывать его нельзя. Момент ценности. <b>План до регистрации</b> — §4.8. '
 'Строки плана: съедобным показываем дату первого сбора, комнатным — интервал полива.', 'Онбординг')

screen('save',
 f'<div class="shot" style="background-image:url({IMG}hero-farm.jpg)"></div><div class="scrim"></div>'
 '<div class="overlay">'
 f'{sb().replace("var(--ink)","#fff")}'
 '<div style="flex:1"></div>'
 '<span class="pill b-lime" id="savepill" style="align-self:flex-start">4 PLANTS</span>'
 '<div class="cap-f" style="font-size:var(--t-40);line-height:1.03;margin-top:16px">Save your plan<br>'
 '<span style="color:var(--lime)">so we can remind you.</span></div>'
 '<div style="font-size:var(--t-16);color:#DCE7DE;line-height:1.5;margin-top:12px">'
 'Your plan is already built. This just saves it. We email you a few tasks a week &mdash; nothing else.</div>'
 '<div class="btn b-lime" style="margin-top:20px" data-go="paywall">Continue with Google</div>'
 '<div class="btn b-white" data-go="paywall">Continue with email</div></div>',
 'Save Plan', 'Фото на весь экран. Регистрация — <b>после</b> показанной ценности, magic link без пароля (§4.9). '
 'Пилюля считается из плана: «4 PLANTS · YEAR-ROUND» внутри, «· 30 WEEKS» на улице.', 'Онбординг')

# ═════════════════════════════ 2. HOME
screen('home',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet" id="homegreet">Good morning</div>'
 '<div class="h1" id="homeh1">Let&rsquo;s get you growing.</div>'
 '<div id="homeacc"></div>'
 '<div id="wkwid"></div>'
 '<div id="homeprog"></div>'
 '<div id="hometasks"></div>'
 '</div>' + ofr() + nav('Week', badge=True),
 'Home', 'Один экран, два состояния. Пусто → акцентный блок зовёт добавить растение. '
 'Есть растения → health score, виджеты и список. Задачи недели <b>считаются из MY_PLANTS</b>, '
 'а не захардкожены: полив по просрочке, сбор для созревших, протирка листьев для крупных.', 'Home')

screen('add-plant',
 f'{sb()}{hd(back="home")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Add a plant</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);margin-top:4px">'
 '<span id="libsub"></span> &middot; <span data-addcount>nothing selected</span></div>'
 '<div class="searchrow">'
 '<div class="search"><span class="si" aria-hidden="true">' + ic('search', '#8E9A93', 19, '2') + '</span>'
 '<input id="spq" type="search" inputmode="search" autocomplete="off" spellcheck="false" '
 'aria-label="Search the plant library" placeholder="Search by name or latin…">'
 '<span class="sx" id="spx" role="button" tabindex="0" aria-label="Clear search">' + ic('x', '#8E9A93', 17, '2.4') + '</span></div>'
 '<div class="scanbtn" role="button" tabindex="0" aria-label="Identify a plant by photo" '
 'data-scan>' + ic('camera', '#fff', 22) + '</div></div>'
 '<div class="scanhint">Don&rsquo;t know what it is? '
 '<b role="button" tabindex="0" data-scan>Point the camera at it</b></div>'
 '<div id="scanwait"></div>'
 '<div id="splist"></div>'
 '<div class="note is-hidden" data-limit style="margin:12px 0 4px"><b>That&rsquo;s the free limit</b>'
 '<p>Free plans keep 3 plants. Pro keeps everything your light and space allow &mdash; '
 'and the whole care calendar for all of them.</p>'
 '<div class="btn b-pri" data-go="paywall">Unlock &mdash; $29/yr</div></div>'
 '</div>' + foot('<div class="btn b-pri off" data-cta>Add to my plants</div>') + nav('Week'),
 'Add a plant', 'Библиотека — <b>один справочник на 29 видов</b>: 8 комнатных и 21 съедобная культура. '
 'Показывается подмножество под трек и место; тем, чему не хватает света, ставим блок '
 '«Needs more light» — <b>погашено, а не спрятано</b>. Внизу soft-lock OFF-04.', 'Home')

screen('week-lock',
 f'{sb()}{hd(back="home")}<div class="bd">'
 '<div class="greet" id="lockwhen">&nbsp;</div>'
 '<div class="h1" id="lockhead">Tasks<br><span class="m">already planned.</span></div>'
 '<div id="lockbody"></div>'
 '</div>' + nav('Week'),
 'Soft-lock', '<b>Даты и объём видны</b>, скрыты только формулировки — §10.3. Это не стена. '
 'Обещание Pro теперь «весь календарь ухода», а не «30 недель сезона».', 'Home')

screen('week-empty',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet">Good morning &middot; nothing due</div>'
 '<div class="h1">Nothing needed<br><span class="m">this week.</span></div>'
 '<div class="note" id="wkemptynote" style="margin-top:16px"></div>'
 '<div class="sl">Your plants</div><div id="wkplants"></div>'
 '</div>' + ofr() + nav('Week'),
 'Week · пусто', '<b>§18</b> «Nothing needed this week. Water, watch, enjoy.» Пустая неделя — '
 'подтверждение, что всё идёт по плану. Список растений и срок следующей задачи '
 '<b>считаются из данных</b> — здесь раньше падало на модели съедобных.', 'Home')

screen('week-back',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet">You were away 2 weeks</div>'
 '<div class="h1">Welcome back.<br><span class="m">Here&rsquo;s what matters now.</span></div>'
 '<div class="note" style="margin-top:16px"><b>Most of it doesn&rsquo;t matter now</b>'
 '<p>Nine tasks stopped being useful and closed themselves. The ones below still pay off.</p></div>'
 '<div class="sl">Still worth doing</div><div id="backtasks"></div>'
 '<div class="btn b-pri" data-go="home">Continue with this week</div>'
 '</div>' + ofr() + nav('Week', badge=True),
 'Week · возврат', '<b>§6.4</b> Продукт <b>никогда</b> не показывает список из двадцати просроченных задач. '
 'Движок сворачивает пропуск в две задачи из настоящих растений, остальное закрывается '
 'статусом expired без обвинения.', 'Home')

screen('week-long',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet">Last visit: 6 weeks ago</div>'
 '<div class="h1">It&rsquo;s been a while.<br><span class="m">Let&rsquo;s restart from today.</span></div>'
 '<div class="note" style="margin-top:16px"><b>Your plan is out of date</b>'
 '<p>Six weeks changed what needs doing. We&rsquo;ll rebuild the schedule from today and keep '
 'everything you already did &mdash; every logged watering and photo stays.</p>'
 '<div class="btn b-pri" data-go="home">Rebuild my plan</div>'
 '<div class="btn b-ghost" data-go="home">Keep the old one</div></div>'
 '<div id="longnote" style="font-size:var(--t-14);color:var(--muted);line-height:1.45;margin-top:16px;padding:0 4px">'
 '</div></div>' + ofr() + nav('Week'),
 'Week · долгий пропуск', '<b>§19.1 №7</b> Пересчёт <b>предлагается</b>, но никогда не делается автоматически. '
 'Нижняя строка называет растения, которые реально пересохли, а не выдуманный редис.', 'Home')

screen('season-end',
 '<div class="dark" id="recapbody"></div>',
 'Recap · OFF-11', '<b>§7.5</b> Итог. На уличном треке триггер <b>today &ge; first_frost</b> и счёт в сборах; '
 'для комнатных сезон не кончается никогда, поэтому итог считается в поливах, растениях и снимках. '
 'Один экран, две формулировки — рендерится из данных.', 'Home')

# ═════════════════════════════ 3. РАСТЕНИЯ
screen('scan',
 '<div class="dark" style="padding:0">'
 '<div id="scanbody"></div></div>',
 'Scan a plant', 'Кнопка Add открывает камеру и распознаёт растение <b>по-настоящему</b> — PlantNet через '
 'воркер-прокси (ключ в клиент не попадает). Латинское имя маппится на наши 29 видов, '
 'включая комнатные; процент — настоящий score от API. Состояния: не подключено, нет совпадения, '
 'не наш вид, нет сети.', 'Plants')

screen('plant',
 f'{sb()}{hd(back="home")}<div class="bd" id="pdetail"></div>' + nav('Week'),
 'Plant detail', 'Карточка растения. Второй виджет зависит от вида: комнатному — свет и влажность, '
 'съедобному — прогресс до сбора и «типичный диапазон». Если у вида нет настоящей фотографии, '
 'стоит <b>плитка с иконкой</b>, а не битая картинка. Внизу — удаление с Undo.', 'Plants')

# ═════════════════════════════ 4. GROWTH
screen('growth',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="h1">Your plants</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);margin-top:4px" id="caresub">&nbsp;</div>'
 '<div id="dash"></div>'
 '<div id="plantcards"></div>'
 '</div>' + ofr('Keep every photo', '$29/yr') + nav('Growth'),
 'Growth', 'История ухода. Раньше здесь были <b>две сущности про одно и то же</b> — список и '
 'отдельная сетка фото, хотя каждое фото и так принадлежит растению. Теперь один дашборд '
 'и карточки растений, у каждой свои снимки. Тап ведёт в карточку.', 'Growth')

screen('harvest',
 '<div class="dark" id="milebody" style="padding:0"></div>',
 'Milestone', 'Пик удержания и лучшая точка конверсии — §9. Для съедобных это «First harvest. Day 31», '
 'для комнатных — «It is thriving» с числом дней и поливов. Экран <b>берёт настоящее фото '
 'растения из журнала</b>, если оно есть.', 'Growth')

screen('shopping',
 f'{sb()}{hd(back="home")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Shopping list</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);margin-top:4px" id="shopsum">&nbsp;</div>'
 '<div id="shopbody"></div>'
 '</div>' + nav('Week'),
 'Shopping list', 'Собирается <b>из плана</b>: горшки по размеру каждого вида, поддоны, грунт, лейка, '
 'удобрение — и строка семян только если в плане есть съедобное. Сумма считается, а не написана. '
 'Free — список на экране, Pro — печатный PDF.', 'Growth')

# ═════════════════════════════ 5. ДЕНЬГИ
FEATS = ['Every week planned, not just this one', 'Every plant in the library, no cap of three',
         'Printable shopping list as PDF', 'Unlimited journal photos + yearly recap',
         'Export your whole care history']
screen('paywall',
 '<div class="dark"><div class="glow"></div><div class="glow b"></div>'
 '<div style="display:flex;justify-content:space-between;align-items:center;position:relative">'
 '<div style="display:flex;align-items:center;gap:8px">' + ic('sprout', 'var(--lime)', 24, '2') +
 '<span style="font-size:var(--t-14);font-weight:700;letter-spacing:.1em">HOMEGROWN</span></div>'
 '<div class="xbtn" role="button" tabindex="0" aria-label="Close" data-pw-exit>' + ic('x', '#CFE0D4', 17, '2') + '</div></div>'
 '<div style="text-align:center;margin-top:24px;position:relative">'
 '<div style="font-size:var(--t-31);font-weight:600;line-height:1.14;letter-spacing:-.02em">'
 'Every plant,<br><span style="color:var(--lime)">planned all year.</span></div>'
 '<div style="font-size:var(--t-14);color:#A9BCB0;margin-top:8px">7 days free. Cancel anytime.</div></div>'
 '<div class="seg" role="radiogroup" aria-label="Billing period">'
 '<div class="on" role="radio" tabindex="0" aria-checked="true" data-seg>Year pass</div>'
 '<div role="radio" tabindex="0" aria-checked="false" data-seg>Monthly</div></div>'
 '<div class="pcard"><div style="display:flex;justify-content:space-between;align-items:flex-start">'
 '<div><div class="pr">$29<span style="font-size:var(--t-15);font-weight:500;color:#A9BCB0"> / year</span></div>'
 '<div class="pn">Cheaper than one dead fiddle leaf fig. Covers every plant, all year.</div></div>'
 '<span class="pill b-lime">Best</span></div>'
 '<div class="feat">' + ''.join(f'<div><i></i><span>{f}</span></div>' for f in FEATS) + '</div></div>'
 '<div style="flex:1;min-height:16px"></div>'
 '<div class="btn b-white" data-buy>Start 7-day free trial</div>'
 '<div class="tlink" data-pw-exit>'
 'Continue with the free plan</div>'
 '<div style="font-size:var(--t-12);color:#6E8175;text-align:center;margin-top:8px;line-height:1.45">'
 'No card for the trial. Your plants and photos stay yours either way.</div></div>',
 'Paywall', 'Собран по референсу Fit AI: тёмный фон, лаймовый glow, сегмент-переключатель, '
 'фичи с точками, белый CTA. <b>Починено:</b> карточка цены была помечена классом карточки растения '
 '(<code>plcard</code>) — из-за этого рисовалась белой полосой 132px, а переключатель тарифов падал '
 'на несуществующем <code>.pcard</code>. Показывается сразу после регистрации и закрывается '
 'в тот экран, откуда пришёл — конфликт со §10.4 сохранён осознанно.', 'Деньги')

screen('week-done',
 '<div class="dark" id="donebody"></div>',
 'Week complete · OFF-05', 'success_modal, <b>не чаще 1 раза в 7 дней</b>. Прозрачного скрима нет — '
 'полный экран. Цифры и строка «что дальше» берутся из настоящих растений.', 'Деньги')

# ═════════════════════════════ 6. SETTINGS
screen('settings',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Settings</div>'
 '<div id="planbox"></div>'
 '<div id="setupbox"></div>'
 '<div id="carebox"></div>'
 '<div id="remindbox"></div>'
 '<div id="databox"></div>'
 '</div>' + nav('Settings'),
 'Settings', 'Экран собирается из состояния целиком, и <b>каждая строка что-то меняет</b>. '
 '«Your setup» — ответы онбординга: тап циклит значение, ZIP появляется только на уличном треке, '
 'Units переводит объёмы и диаметры по всему приложению (настоящий пересчёт, не подпись). '
 '«What goes on the week card» — тумблеры, которые реально фильтруют движок задач; полив не '
 'отключается, это ядро. «Reminders» — время и письма. Export отдаёт настоящий JSON файлом. '
 'Delete account вынесен из блока и подан серым секондари: это выход, а не пункт меню.', 'Система')

screen('pick',
 f'{sb()}{hd(back="settings")}<div class="bd">'
 '<div class="h1" id="pickhead" style="margin-top:16px">Setting</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);margin-top:4px" id="picknote">&nbsp;</div>'
 '<div id="pickbody" style="margin-top:16px"></div>'
 '</div>' + nav('Settings'),
 'Настройка · выбор', 'Значения в настройках больше <b>не циклятся по тапу</b>: строка открывает '
 'раздел со списком, где видно все варианты и что выбрано сейчас. У каждого варианта есть '
 'следствие — для света это «сколько растений подойдёт», для ZIP — зона, заморозки и длина '
 'сезона. Выбрал — вернулся в настройки.', 'Система')

screen('calendar',
 f'{sb()}{hd(back="growth")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Harvest calendar</div>'
 '<div style="font-size:var(--t-14);color:var(--muted);margin-top:4px;line-height:1.4" id="calsub">&nbsp;</div>'
 '<div id="calbody" style="margin-top:16px"></div>'
 '</div>' + nav('Growth'),
 'Harvest calendar', 'Общий календарь года: когда что <b>сеять</b> и когда <b>снимать</b>. '
 'Окна не выдуманы — считаются из даты последних заморозков выбранного ZIP, длины сезона и '
 'числа дней до сбора каждой культуры. Холодостойкие уходят в грунт за месяц до заморозков, '
 'теплолюбивые только после; крайний срок посева такой, чтобы культура успела отдать урожай '
 'до осенних заморозков. У комнатных сезона нет — их строка открыта весь год. '
 'Проваливаешься из виджета на Growth.', 'Growth')

# ═════════════════════════════ 7. ПОДОКОННИК
screen('indoor',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet">Good morning &middot; week 12</div>'
 '<div class="h1">Basil is ready<br><span class="m">to cut again.</span></div>'
 f'<div class="acc"><div class="acc-photo" style="background-image:url({IMG}basil.jpg)"></div>'
 '<div class="row1"><span class="tag">WINDOWSILL &middot; YEAR-ROUND</span></div>'
 '<div class="plants">' +
 ringrow('leaf', 'Basil', 'Cut 7 times &middot; regrows in 10d', 'ready', 100, dark=True, go='plant') +
 ringrow('grains', 'Microgreens', 'Tray 3 &middot; day 8', '~2d', 80, dark=True) +
 ringrow('leaf', 'Cilantro', 'Cut 2 times &middot; next in 9d', '~9d', 60, dark=True) +
 ringrow('plant', 'Garlic chives', 'Day 34 &middot; first cut Jun 8', '~50d', 40, dark=True) +
 '</div>'
 '<div class="duo"><div class="cell"><s>Cuts this year</s><b style="color:var(--lime)">23</b></div>'
 '<div class="cell"><s>Season ends</s><b>never</b></div></div></div>'
 '<div class="sl">This week</div>' +
 task('Cut 6 basil leaves from the top', '2 min', 'Cut above a leaf pair &mdash; it branches and doubles.') +
 task('Sow a new microgreens tray', '5 min') +
 task('Water check: soil top dry?', '2 min') +
 '</div>' + ofr('Add a second windowsill', 'Pro') + nav('Week', badge=True),
 'Windowsill · edibles', 'Съедобный трек внутри дома. «Season ends: never» — вот почему подоконник '
 'закрывает сезонность: ритм тут <b>срез каждую неделю</b>, а не один сбор за 30 дней. '
 'Все четыре вида есть в справочнике с флагом <code>sill</code>. Экран показательный, '
 'содержимое статичное.', 'Windowsill')


# ── ЕДИНЫЙ справочник растений. kind: house — декоративные, edible — съедобные.
#    Интервалы полива и требования к свету — стандартные справочные диапазоны.
#    img=None означает «настоящей фотографии нет» → рисуем плитку с иконкой,
#    а не битую картинку. Выдумывать ассеты нельзя.
def sp(id, name, kind, icon, latin, water, light, hum, img=None,
       days=0, days_max=0, pot='', sun=1, tags=(), sill=False, cool=False):
    # cool=True — холодостойкая культура: сеется до последних заморозков и терпит их.
    # cool=False у съедобных — теплолюбивая, только после заморозков.
    return dict(id=id, name=name, kind=kind, icon=icon, latin=latin, water=water,
                light=light, hum=hum, img=img, days=days, daysMax=days_max or days,
                pot=pot, sun=sun, tags=list(tags), sill=sill, cool=cool)

PLANTS = [
 # ── комнатные: у всех восьми есть настоящее фото
 sp('monstera','Monstera','house','leaf','Monstera deliciosa',9,'Bright indirect','Medium',
    'monstera',sun=1,tags=('statement','trailing'),pot='10 inch'),
 sp('snakeplant','Snake plant','house','plant','Dracaena trifasciata',18,'Low to bright','Low',
    'snakeplant',sun=1,tags=('hardy','lowlight','air'),pot='8 inch'),
 sp('pothos','Pothos','house','leaf','Epipremnum aureum',8,'Low to bright','Medium',
    'pothos',sun=1,tags=('hardy','lowlight','trailing','air','kids'),pot='6 inch'),
 sp('zzplant','ZZ plant','house','plant','Zamioculcas zamiifolia',18,'Low light','Low',
    'zzplant',sun=1,tags=('hardy','lowlight'),pot='8 inch'),
 sp('fiddleleaf','Fiddle leaf fig','house','leaf','Ficus lyrata',9,'Bright indirect','Medium',
    'fiddleleaf',sun=2,tags=('statement',),pot='12 inch'),
 sp('peacelily','Peace lily','house','flower','Spathiphyllum wallisii',6,'Medium indirect','High',
    'peacelily',sun=1,tags=('flowers','air'),pot='8 inch'),
 sp('aloe','Aloe vera','house','plant','Aloe vera',18,'Bright direct','Low',
    'aloe',sun=3,tags=('hardy','useful'),pot='6 inch'),
 sp('calathea','Calathea','house','leaf','Goeppertia orbifolia',6,'Medium indirect','High',
    'calathea',sun=1,tags=('statement','petsafe'),pot='8 inch'),

 # ── съедобные: контейнеры сохнут быстро, отсюда короткие интервалы полива
 sp('radish','Radish','edible','carrot','Raphanus sativus',2,'6\u20138 h sun','\u2014','radish',
    days=25,days_max=35,pot='1 pint',sun=1,tags=('fast','roots','kids'),cool=True),
 sp('lettuce','Leaf lettuce','edible','leaf','Lactuca sativa',2,'3\u20135 h sun','\u2014','lettuce',
    days=30,days_max=35,pot='0.5 gal',sun=1,tags=('salads','fast'),sill=True,cool=True),
 sp('chard','Swiss chard','edible','leaf','Beta vulgaris',2,'3\u20135 h sun','\u2014','chard',
    days=30,days_max=40,pot='0.5 gal',sun=1,tags=('salads',),cool=True),
 sp('mustard','Mustard greens','edible','leaf','Brassica juncea',2,'3\u20135 h sun','\u2014','mustard',
    days=35,days_max=40,pot='0.5 gal',sun=1,tags=('salads',),sill=True,cool=True),
 sp('microgreens','Microgreens','edible','grains','',1,'3\u20135 h sun','\u2014','microgreens',
    days=10,days_max=14,pot='tray',sun=1,tags=('fast','herbs','kids'),sill=True,cool=True),
 sp('cilantro','Cilantro','edible','leaf','Coriandrum sativum',3,'3\u20135 h sun','\u2014','cilantro',
    days=28,days_max=42,pot='0.5 gal',sun=1,tags=('herbs','fast'),sill=True,cool=True),
 sp('basil','Basil','edible','leaf','Ocimum basilicum',3,'6\u20138 h sun','\u2014','basil',
    days=40,days_max=40,pot='1 gal',sun=2,tags=('herbs',),sill=True),
 sp('beans','Bush beans','edible','grains','Phaseolus vulgaris',2,'6\u20138 h sun','\u2014','beans',
    days=45,days_max=60,pot='2 gal',sun=2,tags=('beans','kids')),
 sp('beets','Beets','edible','carrot','Beta vulgaris',2,'3\u20135 h sun','\u2014','beets',
    days=50,days_max=60,pot='0.5 gal',sun=1,tags=('roots',),cool=True),
 sp('squash','Summer squash','edible','orange','Cucurbita pepo',2,'6\u20138 h sun','\u2014','squash',
    days=50,days_max=60,pot='5 gal',sun=2,tags=()),
 sp('cherrytomato','Cherry tomato','edible','cherries','Solanum lycopersicum',2,'6\u20138 h sun','\u2014','cherrytomato',
    days=55,days_max=100,pot='1 gal',sun=2,tags=('tomatoes','kids')),
 sp('tomato','Tomato','edible','cherries','Solanum lycopersicum',2,'6\u20138 h sun','\u2014','tomato',
    days=55,days_max=100,pot='5 gal',sun=2,tags=('tomatoes',)),
 sp('kale','Kale','edible','leaf','Brassica oleracea',2,'3\u20135 h sun','\u2014','kale',
    days=55,days_max=65,pot='5 gal',sun=1,tags=('salads',),cool=True),
 sp('turnips','Turnips','edible','carrot','Brassica rapa',2,'3\u20135 h sun','\u2014','turnips',
    days=30,days_max=60,pot='3 gal',sun=1,tags=('roots',),cool=True),
 sp('carrots','Carrots','edible','carrot','Daucus carota',2,'6\u20138 h sun','\u2014','carrots',
    days=65,days_max=80,pot='1 quart',sun=1,tags=('roots','kids'),cool=True),
 sp('cucumber','Cucumber','edible','orange','Cucumis sativus',2,'6\u20138 h sun','\u2014','cucumber',
    days=70,days_max=80,pot='5 gal',sun=2,tags=()),
 sp('onions','Green onions','edible','plant','Allium fistulosum',3,'3\u20135 h sun','\u2014','onions',
    days=70,days_max=100,pot='0.5 gal',sun=1,tags=('herbs',),sill=True,cool=True),
 sp('parsley','Parsley','edible','leaf','Petroselinum crispum',3,'3\u20135 h sun','\u2014','parsley',
    days=70,days_max=84,pot='0.5 gal',sun=1,tags=('herbs',),sill=True,cool=True),
 sp('eggplant','Eggplant','edible','pepper','Solanum melongena',2,'6\u20138 h sun','\u2014','eggplant',
    days=75,days_max=100,pot='5 gal',sun=2,tags=()),
 sp('chives','Garlic chives','edible','plant','Allium tuberosum',3,'3\u20135 h sun','\u2014','chives',
    days=84,days_max=84,pot='0.5 gal',sun=1,tags=('herbs',),sill=True,cool=True),
 sp('pepper','Bell pepper','edible','pepper','Capsicum annuum',2,'6\u20138 h sun','\u2014','pepper',
    days=110,days_max=120,pot='2 gal',sun=2,tags=('peppers',)),
]
N_HOUSE  = len([x for x in PLANTS if x['kind'] == 'house'])
N_EDIBLE = len([x for x in PLANTS if x['kind'] == 'edible'])
N_PLANTS = len(PLANTS)

ICONSET = sorted({x['icon'] for x in PLANTS} | {'plant','leaf','flower','potted-plant','basket','drop'})

JS_SRC = r'''
const ICONS = __ICONS__;
const SPECIES = __SPECIES__;
const RING_TRACK = '#DDE3DC', RING_ON = '#22A559';
/* track: house | edible | both. outdoor решает, спрашиваем ли ZIP и есть ли конец сезона. */
/* Какой веткой онбординга идёт человек: 'own' — уже есть растения,
   'plan' — начинает с нуля. null — онбординг не идёт. */
let ONB_MODE = null;
/* съедобное — основной трек продукта. Комнатные остаются полноценной ветвью. */
const CHOICES = {track:'edible', space:'patio', outdoor:true,
                 sun:'6–8 hours of sun', sunRank:2, goals:[], effort:4, zip:'78704'};
const anA  = w => (/^[aeiou]/i.test(w) ? 'an ' : 'a ') + w;
const inOn = () => CHOICES.outdoor ? 'on your ' : 'in your ';

const SP      = id => SPECIES.find(function(x){ return x.id === id; });
const spName  = n  => SPECIES.find(function(x){ return x.name === n; });
const ofKind  = k  => SPECIES.filter(function(x){ return x.kind === k; });
const lc      = s  => s.charAt(0).toLowerCase() + s.slice(1);

/* какие виды вообще уместны при выбранном треке и месте */
function speciesPool(){
  /* В ветке «уже есть» трек ещё не известен — показываем всё, что знаем. */
  if(ONB_MODE === 'own') return SPECIES.slice();
  return SPECIES.filter(function(s){
    if(CHOICES.track === 'house'  && s.kind !== 'house')  return false;
    if(CHOICES.track === 'edible' && s.kind !== 'edible') return false;
    if(s.kind === 'edible' && !CHOICES.outdoor && !s.sill) return false;
    return true;
  });
}
const fitsLight = s => s.sun <= CHOICES.sunRank;

function ringSVG(pct, sz, dark, sw){
  sz = sz || 38; sw = sw || 3.2;
  const r = (sz-sw)/2, c = 2*Math.PI*r, off = c*(1-Math.max(0,Math.min(100,pct))/100);
  const tr = dark ? 'rgba(255,255,255,.20)' : RING_TRACK, on = dark ? '#B4F461' : RING_ON;
  return '<svg aria-hidden="true" width="'+sz+'" height="'+sz+'" viewBox="0 0 '+sz+' '+sz+'">'
   +'<circle cx="'+sz/2+'" cy="'+sz/2+'" r="'+r+'" fill="none" stroke="'+tr+'" stroke-width="'+sw+'"/>'
   +'<circle cx="'+sz/2+'" cy="'+sz/2+'" r="'+r+'" fill="none" stroke="'+on+'" stroke-width="'+sw+'"'
   +' stroke-linecap="round" stroke-dasharray="'+c.toFixed(1)+'" stroke-dashoffset="'+off.toFixed(1)+'"'
   +' transform="rotate(-90 '+sz/2+' '+sz/2+')"/></svg>';
}

/* ─────────── фото вида: настоящий снимок либо плитка с иконкой ─────────── */
const hasPhoto = s => !!s.img;
function photoStyle(s){
  return s.img ? 'background-image:url(img/' + s.img + '.jpg)'
               : 'background:linear-gradient(150deg,#17683C 0%,#0F3A24 60%,#0B1F14 100%)';
}
function photoTile(s, cls, style){
  return '<div class="' + cls + (s.img ? '' : ' no-ph') + '" style="'
   + photoStyle(s) + (style ? ';' + style : '') + '">'
   + (s.img ? '' : '<span class="ph-ic">' + (ICONS['_big_' + s.icon] || ICONS._big_leaf) + '</span>');
}

/* круглая миниатюра вида: настоящее фото, если оно есть в img/,
   иначе диск с иконкой. Из 29 видов без фото остался один. */
function spThumb(s){
  return s.img
    ? '<div class="spic has" style="background-image:url(img/' + s.img + '.jpg)"></div>'
    : '<div class="spic">' + ICONS[s.icon] + '</div>';
}
/* ─────────── библиотека: строка вида ─────────── */
function spSub(s){
  if(s.kind === 'edible')
    return s.days + (s.daysMax !== s.days ? '–' + s.daysMax : '') + ' days · ' + fmtPot(s.pot);
  return 'Water every ' + s.water + 'd · ' + s.light;
}
function spRow(s){
  const have = MY_PLANTS.some(function(p){ return p.s.id === s.id; });
  const pick = PENDING.indexOf(s.id) > -1;
  const label = have ? s.name + ' — already in your plants'
                     : (pick ? 'Remove ' + s.name + ' from the selection'
                             : 'Add ' + s.name + ' to your plants');
  return '<div class="pl' + (pick ? ' added' : '') + (have ? ' have' : '') + '" '
   + (have ? 'aria-disabled="true" ' : 'role="button" tabindex="0" data-add ')
   + 'aria-label="' + label + '" data-sp="' + s.id + '">'
   + spThumb(s)
   + '<div class="nm"><b>' + s.name + '</b><s>' + spSub(s)
   + (fitsLight(s) ? '' : ' · needs more light') + '</s></div>'
   + '<div class="addbtn" aria-hidden="true">'
   + (have ? ICONS._checkg : ICONS._plus + ICONS._check) + '</div></div>';
}
function renderLibrary(q){
  q = (q||'').trim().toLowerCase();
  const box = document.getElementById('splist'); if(!box) return;
  const cnt = document.querySelector('[data-addcount]');
  if(cnt) cnt.textContent = PENDING.length ? PENDING.length + ' selected' : 'nothing selected';
  const cta = document.querySelector('#s-add-plant [data-cta]');
  if(cta){
    if(ONB_MODE === 'own'){
      /* в онбординге пустой выбор не тупик: можно пройти дальше и добавить позже */
      cta.classList.remove('off');
      cta.textContent = PENDING.length ? 'Add ' + PENDING.length + ' and continue' : 'Skip for now';
    } else {
      cta.classList.toggle('off', !PENDING.length);
      cta.textContent = PENDING.length ? 'Add ' + PENDING.length + ' to my plants' : 'Add to my plants';
    }
  }
  const lim = document.querySelector('#s-add-plant [data-limit]');
  if(lim) lim.style.display = !IS_PRO && (MY_PLANTS.length + PENDING.length) >= FREE_LIMIT ? 'block' : 'none';
  const sub = document.getElementById('libsub');
  if(sub) sub.textContent = ONB_MODE === 'own'
    ? 'Everything we know how to look after'
    : (LIBNOTE[CHOICES.track] || LIBNOTE.both);
  const sh = document.getElementById('scanwait');
  if(sh) sh.innerHTML = SCAN_KEEP
    ? '<div class="scanwait"><div class="sw-ph" style="background-image:url(' + SCAN_KEEP + ')"></div>'
      + '<div class="sw-tx"><b>Your photo is waiting</b>'
      + '<s>Pick what it is and the shot goes into its journal.</s></div></div>'
    : '';

  const pool = speciesPool();
  const m = s => !q || s.name.toLowerCase().indexOf(q) > -1
              || (s.latin || '').toLowerCase().indexOf(q) > -1
              || s.tags.some(function(t){ return t.indexOf(q) > -1; });
  const hit = pool.filter(m);
  if(!hit.length){
    box.innerHTML = '<div class="empty">Nothing matches “' + q + '”.<br>'
      + 'We know ' + SPECIES.length + ' plants — ' + ofKind('house').length + ' houseplants and '
      + ofKind('edible').length + ' edible.</div>';
    return;
  }
  const lit = hit.filter(fitsLight), dim = hit.filter(function(s){ return !fitsLight(s); });
  const sect = (label, list) => list.length
    ? '<div class="gsec">' + label + '</div><div class="plist">' + list.map(spRow).join('') + '</div>' : '';
  let h = '';
  const house = lit.filter(function(s){ return s.kind === 'house'; });
  const edible = lit.filter(function(s){ return s.kind === 'edible'; });
  if(ONB_MODE === 'own' || CHOICES.track === 'both'){
    /* трек ещё не выбран или выбраны оба — показываем обе группы,
       иначе половина справочника не попадала ни в одну секцию */
    h += sect('Houseplants', house);
    h += sect(ONB_MODE === 'own' ? 'Edible'
              : (CHOICES.outdoor ? 'Edible — container crops' : 'Edible — windowsill crops'), edible);
  } else if(CHOICES.track === 'house'){
    h += sect('Hard to kill', house.filter(function(s){ return s.water >= 12; }));
    h += sect('A bit more attention', house.filter(function(s){ return s.water < 12; }));
  } else {
    h += sect('Fast wins', edible.filter(function(s){ return s.days <= 35; }));
    h += sect('Worth the wait', edible.filter(function(s){ return s.days > 35; }));
  }
  if(dim.length) h += '<div class="gsec">Needs more light than you have</div>'
     + '<div class="plist" style="opacity:.5">' + dim.map(spRow).join('') + '</div>';
  box.innerHTML = h;
}
const LIBNOTE = {
  house: 'Survives an ordinary room',
  edible: 'Finishes in one season',
  both: 'Houseplants, then edible'
};

/* ─────────── мини-движок плана ─────────── */
function buildPlan(){
  const g = CHOICES.goals, n = CHOICES.effort;
  let pool = speciesPool().filter(fitsLight);
  if(!pool.length) pool = speciesPool();
  const score = s => (s.tags.filter(function(t){ return g.indexOf(t) > -1; }).length * 40)
                   + (s.kind === 'edible' && s.days <= 35 ? 20 : 0)
                   + (s.kind === 'house' ? (s.water >= 12 ? 14 : 6) : 0)
                   + (s.kind === 'edible' ? (120 - s.daysMax) / 12 : 0);
  pool = pool.slice().sort(function(a,b){ return score(b) - score(a); });
  const out = [];
  for(let i = 0; i < pool.length && out.length < n; i++){
    const s = pool[i];
    if(s.kind === 'edible' && s.days > 70
       && out.filter(function(x){ return x.days > 70; }).length >= 2) continue;
    out.push(s);
  }
  /* трек both обязан дать и то, и другое */
  if(CHOICES.track === 'both'){
    const need = ['house','edible'].filter(function(k){
      return !out.some(function(s){ return s.kind === k; }); });
    need.forEach(function(k){
      const add = pool.find(function(s){ return s.kind === k; });
      if(add){ out.pop(); out.unshift(add); }
    });
  }
  /* съедобный трек обязан дать хотя бы одну быструю культуру */
  if(CHOICES.track === 'edible' && !out.some(function(s){ return s.days <= 35; })){
    const f = pool.find(function(s){ return s.days <= 35; });
    if(f){ out.pop(); out.unshift(f); }
  }
  /* каждая заявленная цель обязана быть представлена, если по свету это возможно.
     Иначе человек просит томаты, получает пять салатов и не понимает почему. */
  g.forEach(function(tag){
    if(out.some(function(s){ return s.tags.indexOf(tag) > -1; })) return;
    const cand = pool.find(function(s){ return s.tags.indexOf(tag) > -1; });
    if(!cand) return;
    let victim = -1;
    for(let i = out.length - 1; i >= 0; i--){
      const covers = out[i].tags.filter(function(t){ return g.indexOf(t) > -1; });
      const spare = covers.every(function(t){
        return out.some(function(x, k){ return k !== i && x.tags.indexOf(t) > -1; }); });
      if(spare){ victim = i; break; }
    }
    if(victim < 0 && out.length >= n) victim = out.length - 1;
    if(victim >= 0) out.splice(victim, 1);
    out.push(cand);
  });
  return out;
}
const MONTH = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function dateAfter(days){ const d = new Date(2026,2,14); d.setDate(d.getDate()+days);
                          return MONTH[d.getMonth()]+' '+d.getDate(); }
const QUOTE = {
  house: ['Start with one plant that forgives you. A pothos will tell you it is thirsty and '
        + 'come back from it — that is the whole lesson, and it costs eight dollars.',
          'Placeholder name', 'Plant shop owner · sample quote'],
  edible: ['Radish and leaf lettuce are what we hand every first-timer — they finish before '
        + 'anyone has time to lose interest. The container sizes here are the ones we recommend.',
          'Placeholder name', 'Extension master gardener · sample quote']
};
function renderPreview(){
  const plan = buildPlan();
  const el = document.getElementById('planrows'); if(!el) return;
  const edible = plan.filter(function(s){ return s.kind === 'edible'; });
  el.innerHTML = plan.map(function(s){
    const right = s.kind === 'edible' ? dateAfter(s.days) : 'every ' + s.water + 'd';
    return '<div class="prow">' + spThumb(s)
     + '<div class="nm"><b>' + s.name + '</b><s>' + spSub(s) + '</s></div>'
     + '<div class="rt">' + right + '</div></div>';
  }).join('');
  let second = 'Care starts today.';
  if(edible.length){
    const first = Math.min.apply(null, edible.map(function(s){ return s.days; }));
    second = (CHOICES.outdoor ? 'First pick ' : 'First cut ') + dateAfter(first) + '.';
  }
  document.getElementById('planhead').innerHTML =
    plan.length + (plan.length === 1 ? ' plant.' : ' plants.') + '<br>' + second;
  const add = document.querySelector('#s-preview [data-planadd]');
  if(add){
    const room = Math.min(plan.length, limit());
    add.textContent = 'Add ' + (room === plan.length ? 'these ' + room : 'the first ' + room)
      + (room === 1 ? ' plant' : ' plants');
  }
  const mins = CHOICES.effort === 3 ? 10 : CHOICES.effort === 4 ? 20 : 30;
  document.getElementById('planmeta').textContent =
    (CHOICES.outdoor ? zipInfo().city + ' · ' : '') + CHOICES.sun + ' · ' + anA(CHOICES.space)
    + ' · about ' + mins + ' min a week';
  const q = QUOTE[CHOICES.track === 'edible' ? 'edible' : 'house'];
  const qb = document.getElementById('planquote');
  if(qb) qb.innerHTML = '<div class="qmark">“</div><p>' + q[0] + '</p>'
    + '<div class="qwho"><div class="qav">' + (CHOICES.track === 'edible' ? 'MG' : 'PS')
    + '</div><div><b>' + q[1] + '</b><s>' + q[2] + '</s></div></div>';

  const got = {};
  plan.forEach(function(s){ s.tags.forEach(function(t){ got[t] = 1; }); });
  const asked = CHOICES.goals.length ? CHOICES.goals : (CHOICES.track === 'edible' ? ['fast'] : ['hardy']);
  const kept = asked.filter(function(t){ return got[t]; });
  const missed = asked.filter(function(t){ return !got[t]; });
  const list = a => a.map(function(x){ return GOALWORD[x] || x; })
      .reduce(function(s,x,i,arr){ return s + (i===0?'':(i===arr.length-1?' and ':', ')) + x; }, '');
  let t = '<b>Why these:</b> you asked for ' + list(asked) + ', and ' + CHOICES.sun
        + ' is what decides the rest. ';
  const fast = edible.length ? edible.reduce(function(a,b){ return b.days < a.days ? b : a; }) : null;
  const tough = plan.filter(function(s){ return s.kind === 'house'; })
                    .sort(function(a,b){ return b.water - a.water; })[0];
  t += fast ? fast.name + ' is your fast win — ready in ' + fast.days + ' days.'
            : (tough ? tough.name + ' is the forgiving one — it only needs water every '
                       + tough.water + ' days.' : '');
  if(missed.length){
    const all = speciesPool();
    const exists = tag => all.some(function(s){ return s.tags.indexOf(tag) > -1; });
    const lit    = tag => all.some(function(s){ return s.tags.indexOf(tag) > -1 && fitsLight(s); });
    const dark   = missed.filter(function(tag){ return exists(tag) && !lit(tag); });
    const absent = missed.filter(function(tag){ return !exists(tag); });
    const tight  = missed.filter(function(tag){
      return dark.indexOf(tag) < 0 && absent.indexOf(tag) < 0; });
    let w = '';
    if(dark.length){
      const need = dark.map(function(m){ return SUNNEED[m]; }).filter(Boolean)[0];
      w += list(dark).replace(/^./, function(c){ return c.toUpperCase(); })
         + (need ? ' need ' + need + ' of direct sun. At your light they rarely finish, so we left '
                 : ' need more light than you have, so we left ')
         + (dark.length > 1 ? 'them' : 'it') + ' out. ';
    }
    if(absent.length){
      w += list(absent).replace(/^./, function(c){ return c.toUpperCase(); })
         + (absent.length > 1 ? ' are' : ' is') + ' not something we grow '
         + (CHOICES.outdoor ? 'in containers' : 'indoors') + ' yet. ';
    }
    if(tight.length){
      w += list(tight).replace(/^./, function(c){ return c.toUpperCase(); })
         + ' didn\u2019t fit in ' + plan.length + ' plants — ask for more time a week and '
         + (tight.length > 1 ? 'they' : 'it') + ' come' + (tight.length > 1 ? '' : 's') + ' in. ';
    }
    w += 'You can add ' + (missed.length > 1 ? 'them' : 'it') + ' by hand any time.';
    t += '<span class="warn">' + w + '</span>';
  }
  document.getElementById('planwhy').innerHTML = t;
}

/* ═══════════ состояние: ОДНА форма растения {s, since, day, photos} ═══════════ */
let MY_PLANTS = [], SELECTED = 0, PENDING = [], UNDO = null, UNDOT = null, IS_PRO = false;
const FREE_LIMIT = 3;
const limit = () => IS_PRO ? 99 : FREE_LIMIT;
const TODAY = 27;                                  // условный «сегодня» в днях от старта

function mkPlant(id, since, day, photos){
  const s = SP(id) || SPECIES[0];
  return { s: s, since: since === undefined ? 0 : since,
           day: day === undefined ? 0 : day, photos: photos || [] };
}
function seedPlants(){
  MY_PLANTS = [ mkPlant('radish', 0, 27, [{f:'radish', day:24}, {f:'leaves1', day:11}]),
                mkPlant('lettuce', 1, 24, [{f:'leaves3', day:18}]),
                mkPlant('basil', 3, 34, [{f:'basil', day:21}]),
                mkPlant('cherrytomato', 1, 12, []) ];
}
function seedHouseDemo(){
  MY_PLANTS = [ mkPlant('monstera', 4, 210, [{f:'leaves3', day:18}]),
                mkPlant('snakeplant', 20, 430, []),
                mkPlant('pothos', 9, 96, [{f:'leaves1', day:11}]),
                mkPlant('peacelily', 2, 64, [{f:'flowers', day:21}]) ];
}
function seedMixed(){
  MY_PLANTS = [ mkPlant('monstera', 4, 210, [{f:'leaves3', day:18}]),
                mkPlant('pothos', 9, 96, []),
                mkPlant('basil', 1, 34, [{f:'basil', day:21}]),
                mkPlant('radish', 0, 27, [{f:'radish', day:24}]) ];
}
const isEdible = p => p.s.kind === 'edible';
/* компактная подпись света для узкой колонки виджета: раньше строка
   резалась по первому слову и «Low to bright» превращалось в «Low» */
const LIGHTSHORT = {'Low to bright':'Any', 'Bright indirect':'Indirect',
  'Medium indirect':'Indirect', 'Bright direct':'Direct', 'Low light':'Low'};
const lightShort = s => LIGHTSHORT[s.light] || s.light.replace(/ (h )?sun$/, 'h');
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
const inDays = n => n <= 0 ? 'today' : n === 1 ? 'tomorrow' : 'in ' + n + ' days';
const wDue = p => p.s.water - p.since;                              // дней до полива
const wPct = p => Math.max(0, Math.min(100, Math.round(p.since / p.s.water * 100)));
const hPct = p => !isEdible(p) ? 0 : Math.min(100, Math.round(p.day / p.s.days * 100));
const hEta = p => { const d = p.s.days - p.day; return d <= 0 ? 'ready' : '~' + d + 'd'; };
const hStage = p => { const r = p.day / p.s.days;
  return r < 0.1 ? 'seed' : r < 0.35 ? 'seedling' : r < 0.7 ? 'growing'
       : r < 1 ? 'nearly ready' : 'ready'; };
const pPct = p => isEdible(p) ? hPct(p) : wPct(p);
const pSub = p => isEdible(p) ? 'Day ' + p.day + ' · ' + hStage(p)
                              : p.s.light + ' · every ' + p.s.water + 'd';
function pState(p){
  const d = wDue(p);
  if(d <= 0) return ['Needs water', 'bad'];
  if(d <= 2) return ['Water soon',  'warn'];
  if(isEdible(p) && hPct(p) >= 100) return ['Ready to pick', 'ok'];
  return ['Healthy', 'ok'];
}
const allPhotos = () => MY_PLANTS.flatMap(function(p){
  return p.photos.map(function(x){
    return {f:x.f, u:x.u, n:p.s.name, day:x.day, st:pState(p)[0]}; });
}).sort(function(a,b){ return b.day - a.day; });

function healthScore(){
  if(!MY_PLANTS.length) return 0;
  const sum = MY_PLANTS.reduce(function(a, p){
    const d = wDue(p);
    const pen = d > 0 ? 0                                    // ещё не пора — полный вклад
              : d === 0 ? 0.12                               // ровно сегодня — небольшой штраф
              : Math.min(1, (-d) / p.s.water * 1.6);         // просрочено — по мере просрочки
    return a + Math.max(0, 1 - pen);
  }, 0);
  return Math.round(sum / MY_PLANTS.length * 100);
}
function verdict(sc, due){
  due = due || 0;
  if(due >= 3)  return ['Struggling', due + ' plants are waiting for water'];
  if(due === 2) return ['Needs care', 'Two are waiting for water'];
  if(due === 1) return ['Good', 'One needs a drink today'];
  if(sc >= 92)  return ['Great', 'Your plants are doing amazing'];
  if(sc >= 75)  return ['Good', 'Everything is on schedule'];
  return ['Needs care', 'Some plants are drifting off schedule'];
}
function ringBig(pct, sz){
  const sw = 6, r = (sz - sw) / 2, c = 2 * Math.PI * r, off = c * (1 - pct / 100);
  return '<svg aria-hidden="true" width="' + sz + '" height="' + sz + '" viewBox="0 0 ' + sz + ' ' + sz + '">'
   + '<circle cx="' + sz/2 + '" cy="' + sz/2 + '" r="' + r + '" fill="none" stroke="rgba(255,255,255,.16)" stroke-width="' + sw + '"/>'
   + '<circle cx="' + sz/2 + '" cy="' + sz/2 + '" r="' + r + '" fill="none" stroke="var(--lime)" stroke-width="' + sw + '"'
   + ' stroke-linecap="round" stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '"'
   + ' transform="rotate(-90 ' + sz/2 + ' ' + sz/2 + ')"/></svg>';
}
function plantCard(p, i){
  const st = pState(p);
  return '<div class="plcard" data-open="' + i + '">'
   + photoTile(p.s, 'plcard-ph')
   + '<span class="plcard-fav">' + ICONS._drop + '</span></div>'
   + '<b>' + p.s.name + '</b>'
   + '<s class="st-' + st[1] + '">' + st[0] + '</s></div>';
}
function renderDashHome(){
  const acc = document.getElementById('homeacc'); if(!acc) return;
  const g = document.getElementById('homegreet'), h = document.getElementById('homeh1');
  if(!MY_PLANTS.length){
    g.textContent = '';
    h.innerHTML = '';
    const HEAD = {
      edible: ['One pot is enough to start', 'Grow something<br>you can<br>actually eat.'],
      house:  ['One plant is enough to start', 'Every room<br>feels better<br>with something<br>alive in it.'],
      both:   ['One pot is enough to start', 'One pot,<br>one plant,<br>and you have<br>started.']
    };
    const hd2 = HEAD[CHOICES.track] || HEAD.both;
    acc.innerHTML = '<div class="empty-hero">'
      + '<div class="eh-shot" style="background-image:url(img/hero-garden.jpg)"></div>'
      + '<div class="eh-ov"><div>'
      + '<div class="eh-k">' + hd2[0] + '</div>'
      + '<div class="eh-h">' + hd2[1] + '</div></div>'
      + '<div class="btn b-lime" data-scan>Add your first plant</div>'
      + '<div class="eh-alt" data-go="add-plant">or pick from the library</div></div></div>';
    return;
  }
  const sc = healthScore();
  const due = MY_PLANTS.filter(function(p){ return wDue(p) <= 0; });
  const v = verdict(sc, due.length);
  const soon = MY_PLANTS.filter(function(p){ const d = wDue(p); return d > 0 && d <= 2; });
  const nextP = MY_PLANTS.slice().sort(function(a,b){ return wDue(a) - wDue(b); })[0];
  g.textContent = 'Good morning';
  h.innerHTML = 'Plant parent';
  acc.innerHTML =
     '<div class="score">'
   + '<div class="score-ph" style="' + photoStyle(MY_PLANTS[0].s) + '"></div>'
   + '<div class="score-sc"></div>'
   + '<div class="score-in"><div class="score-row">'
   + '<div class="score-top">' + ringBig(sc, 56) + '<span>' + ICONS._leaf + '</span></div>'
   + '<div><div class="score-n"><b>' + sc + '</b><s>/100</s></div>'
   + '<div class="score-v">' + v[0] + '</div></div></div>'
   + '<div class="score-s">' + v[1] + '</div></div></div>'
   + '<div class="wgrid" style="margin-top:8px">'
   + '<div class="wg wg-dark"><div class="wg-top"><div class="num">' + due.length + '</div>'
   + ICONS._dropbig + '</div><div class="lbl">Water today</div>'
   + metricRow([['Soon', soon.length], ['Plants', MY_PLANTS.length]]) + '</div>'
   + '<div class="wg wg-lite"><div class="wg-top"><div class="num">'
   + Math.max(0, wDue(nextP)) + '<span>d</span></div>' + ICONS._dropp + '</div>'
   + '<div class="lbl">' + (wDue(nextP) <= 0 ? nextP.s.name + ' is thirsty'
                                             : 'Until ' + lc(nextP.s.name)) + '</div>'
   + metricRow([['Light', lightShort(nextP.s)],
                [isEdible(nextP) ? 'Harvest' : 'Humidity',
                 isEdible(nextP) ? hEta(nextP) : nextP.s.hum]]) + '</div></div>'
   + '<div class="sec-h"><span>My plants</span><i data-go="add-plant">Add</i></div>'
   + '<div class="prow-scroll">' + MY_PLANTS.map(plantCard).join('') + '</div>';
}

/* ─────────── недельные задачи считаются из растений, а не захардкожены ─────────── */
let DONE = {}, WEEK_OPEN = true;
/* задача = [заголовок, время, пояснение, КЛЮЧ]. Ключ привязан к растению:
   по тексту два одинаковых заголовка делили одну галочку. */
function weekTasks(){
  if(!MY_PLANTS.length) return [];
  const out = [];
  MY_PLANTS.forEach(function(p, i){
    if(wDue(p) <= 0) out.push(['Water the ' + lc(p.s.name), '1 min',
      p.since + ' days since the last drink — it wants one every ' + p.s.water + '.',
      'water:' + i]);
  });
  if(CARE.pick) MY_PLANTS.forEach(function(p, i){
    if(isEdible(p) && hPct(p) >= 100)
      out.push(['Pick from the ' + lc(p.s.name), '4 min',
        'It is ready. Picking keeps it producing.', 'pick:' + i]);
  });
  const si = MY_PLANTS.findIndex(function(p){ return p.s.tags.indexOf('statement') > -1; });
  if(CARE.leaf && si > -1) out.push(['Wipe the ' + lc(MY_PLANTS[si].s.name) + ' leaves', '3 min',
    'Dust cuts the light it gets.', 'wipe:' + si]);
  MY_PLANTS.forEach(function(p, i){
    const d = wDue(p);
    if(d > 0 && d <= 2) out.push(['Check the ' + lc(p.s.name) + ' — top soil dry?', '1 min', '',
      'check:' + i]);
  });
  const ti = MY_PLANTS.findIndex(function(p){ return p.s.sun >= 2; });
  if(CARE.rotate && ti > -1) out.push(['Rotate the ' + lc(MY_PLANTS[ti].s.name) + ' a quarter turn',
    '1 min', 'Keeps it growing even on all sides.', 'rotate:' + ti]);
  if(CARE.feed) out.push([MY_PLANTS.some(isEdible) ? 'Feed the edible pots once this month'
                                                   : 'Feed everything once this month', '4 min',
    'Container soil runs out faster than a bed.', 'feed']);
  return out.slice(0, 6);
}
const tkey = t => t[3] || t[0];
let WEEK = [];
function taskHTML(t){
  return '<div class="task" role="checkbox" tabindex="0" aria-checked="false" data-task>'
    +'<div class="box" aria-hidden="true">'+ICONS._check2+'</div><div class="tt">'
    +'<div class="t">'+t[0]+'</div>'+(t[2]?'<div class="b">'+t[2]+'</div>':'')
    +'</div><div class="min">'+t[1]+'</div></div>';
}
function progHTML(){
  const n = WEEK.filter(function(t){ return DONE[tkey(t)]; }).length, m = WEEK.length;
  const pct = m ? Math.round(n / m * 100) : 0;
  return '<div class="wk' + (WEEK_OPEN ? ' open' : '') + '">'
    + '<div class="wk-h" data-progtoggle>'
    + '<div class="wk-title">' + m + (m === 1 ? ' thing to do' : ' things to do') + '</div>'
    + '<div class="wk-row"><span class="pb-n">' + n + ' of ' + m + '</span>'
    + '<span class="pb-track"><i style="width:' + pct + '%"></i></span>'
    + '<span class="pb-pct">' + pct + '%</span>'
    + '<span class="pb-chev">' + ICONS._chevd + '</span></div></div>'
    + (WEEK_OPEN ? '<div class="wk-list">' + WEEK.map(function(t, i){
        const on = !!DONE[tkey(t)];
        return '<div class="br-row" role="checkbox" tabindex="0" aria-checked="'
          + (on ? 'true' : 'false') + '" data-brtoggle="' + i + '">'
          + '<span class="br-dot' + (on ? ' on' : '') + '">'
          + (on ? ICONS._check2 : '') + '</span>'
          + '<span class="br-t' + (on ? ' done' : '') + '">' + t[0]
          + (t[2] && !on ? '<s>' + t[2] + '</s>' : '') + '</span>'
          + '<span class="br-m">' + t[1] + '</span></div>';
      }).join('') + '</div>' : '')
    + '</div>';
}
function renderWeek(){
  const pr = document.getElementById('homeprog'), tk = document.getElementById('hometasks');
  if(!pr) return;
  WEEK = weekTasks();
  pr.innerHTML = progHTML();
  if(tk) tk.innerHTML = '';
}
function checkWeekDone(){
  if(WEEK.length && WEEK.every(function(t){ return DONE[tkey(t)]; }))
    setTimeout(function(){ go('week-done'); }, 600);
}
function renderHome(){
  renderDashHome();
  const pr = document.getElementById('homeprog'), tk = document.getElementById('hometasks'),
        w = document.getElementById('wkwid');
  if(w) w.innerHTML = '';
  if(!MY_PLANTS.length){ if(pr) pr.innerHTML = ''; if(tk) tk.innerHTML = ''; return; }
  renderWeek();
}

/* ─────────── удаление с Undo ─────────── */
function removePlant(i){
  if(!MY_PLANTS[i]) return;
  UNDO={p:MY_PLANTS[i], i:i}; MY_PLANTS.splice(i,1);
  if(SELECTED >= MY_PLANTS.length) SELECTED = Math.max(0, MY_PLANTS.length - 1);
  renderAll();
  const t=document.getElementById('toast');
  t.innerHTML='<span>'+UNDO.p.s.name+' removed</span><b data-undo>Undo</b>';
  t.classList.add('on'); clearTimeout(UNDOT);
  UNDOT=setTimeout(function(){t.classList.remove('on'); UNDO=null;}, 4500);
}
function undoRemove(){
  if(!UNDO) return;
  MY_PLANTS.splice(UNDO.i,0,UNDO.p); UNDO=null;
  document.getElementById('toast').classList.remove('on');
  renderAll();
}

/* ─────────── карточка растения ─────────── */
/* Роли на разметку, которую собирает JS. Один проход по активному экрану
   вместо шестидесяти правок в местах сборки строк. */
const TAPPABLE = '.btn,.btn-dash,.plcard,.chead,.cempty,.sec-h i,.eh-alt,.xbtn,.addtop,'
               + '.pl[data-add],.pl[data-open],.pl[data-go],[data-shoot],[data-water],'
               + '[data-remove],[data-addphoto],[data-scan],[data-scanadd],[data-cta],'
               + '[data-undo],[data-unpro],[data-buy],[data-pw-exit],[data-gogrowth]';
function stampRoles(scope){
  (scope || document).querySelectorAll(TAPPABLE).forEach(function(e){
    if(!e.hasAttribute('role')) e.setAttribute('role', 'button');
    if(!e.hasAttribute('tabindex')) e.setAttribute('tabindex', '0');
  });
}
function toast(html, ms){
  const t = document.getElementById('toast'); if(!t) return;
  t.innerHTML = html; t.classList.add('on'); clearTimeout(UNDOT);
  UNDOT = setTimeout(function(){ t.classList.remove('on'); }, ms || 3500);
}
function addPhotoBtn(label){
  return '<div class="btn-dash" data-addphoto>'+ICONS._plus
    +'<span>'+(label||'Add a photo')+'</span></div>';
}
const phUrl = x => x.u || ('img/' + x.f + '.jpg');
function photoCard(x){
  return '<figure class="jc"><div class="jph" style="background-image:url('+phUrl(x)+')"></div>'
   +'<figcaption><b>'+x.n+'</b><s>Day '+x.day+' &middot; '+x.st+'</s></figcaption></figure>';
}
function renderDetail(){
  const box = document.getElementById('pdetail'); if(!box) return;
  const p = MY_PLANTS[SELECTED];
  if(!p){ box.innerHTML = '<div class="note" style="margin-top:16px"><b>This plant is gone</b>'
      + '<p>You removed it. Nothing is lost — add it again whenever you like.</p>'
      + '<div class="btn b-pri" data-go="add-plant">Add a plant</div></div>'; return; }
  const st = pState(p), d = wDue(p);
  box.innerHTML =
     photoTile(p.s, 'det-ph', 'margin-top:8px') + '</div>'
   + '<div style="display:flex;align-items:center;gap:12px;margin-top:16px">'
   + '<div><div style="font-size:var(--t-24);font-weight:600;letter-spacing:-.02em">' + p.s.name + '</div>'
   + (p.s.latin ? '<div style="font-size:var(--t-13);color:var(--muted);font-style:italic">'
                  + p.s.latin + '</div>' : '')
   + '</div>'
   + '<div style="flex:1"></div><span class="pill st-pill st-' + st[1] + '">' + st[0] + '</span></div>'
   + '<div class="wgrid" style="margin-top:12px">'
   + '<div class="wg wg-dark"><div class="wg-top"><div class="num">' + Math.max(0, d)
   + '<span>d</span></div>' + arc(100 - wPct(p), 44, true) + '</div>'
   + '<div class="lbl">' + (d <= 0 ? 'Water it today' : 'Until next water') + '</div>'
   + metricRow([['Every', p.s.water + 'd'], ['Last', p.since + 'd ago']]) + '</div>'
   + (isEdible(p)
      ? '<div class="wg wg-lite"><div class="wg-top"><div class="num">' + hPct(p)
        + '<span>%</span></div>' + arc(hPct(p), 44, false) + '</div>'
        + '<div class="lbl">' + (hPct(p) >= 100 ? 'Ready to pick' : 'To first pick') + '</div>'
        + metricRow([['Pot', fmtPot(p.s.pot)], ['Typical', p.s.days
          + (p.s.daysMax !== p.s.days ? '–' + p.s.daysMax : '') + 'd']]) + '</div>'
      : '<div class="wg wg-lite"><div class="wg-h"><b>Conditions</b></div>'
        + metricRow([['Light', p.s.light]]) + metricRow([['Humidity', p.s.hum]]) + '</div>')
   + '</div>'
   + '<div class="btn b-pri" data-water="' + SELECTED + '">Water it now</div>'
   + (isEdible(p) && hPct(p) >= 100
      ? '<div class="btn b-ghost" data-go="harvest">Pick it — first harvest</div>' : '')
   + '<div class="sl">Journal' + (p.photos.length ? ' · ' + p.photos.length
        + (p.photos.length === 1 ? ' photo' : ' photos') : '') + '</div>'
   + (p.photos.length
      ? '<div class="jgrid">' + p.photos.map(function(x){
          return photoCard({ f:x.f, u:x.u, n:p.s.name, day:x.day, st:st[0] }); }).join('') + '</div>' + addPhotoBtn()
      : addPhotoBtn('Take the first photo'))
   + '<div class="btn b-ghost" data-remove>Remove from my plants</div>';
}

/* ─────────── Pro ─────────── */
function buyPro(){
  IS_PRO = true;
  document.body.classList.add('is-pro');
  renderAll();
  const t=document.getElementById('toast');
  t.innerHTML='<span>Pro unlocked — the whole calendar is open</span><b data-unpro>Undo</b>';
  t.classList.add('on'); clearTimeout(UNDOT);
  UNDOT=setTimeout(function(){t.classList.remove('on')}, 5000);
  /* Кнопки обещают «весь календарь», а возврат шёл туда, откуда пришли, —
     обещание не выполнялось ни разу. Ведём в календарь. Исключения: лимит
     растений обещал библиотеку, а без растений календарь показывать нечем. */
  go((PW_FROM === 'add-plant' || !MY_PLANTS.length) ? PW_FROM : 'week-lock');
}
function dropPro(){
  IS_PRO = false; document.body.classList.remove('is-pro');
  renderAll();
  document.getElementById('toast').classList.remove('on');
}
const WORDNUM = ['No','One','Two','Three','Four','Five','Six'];
function renderLock(){
  const box=document.getElementById('lockbody'); if(!box) return;
  /* окно «через две недели» считалось из захардкоженных дат Apr 11–17,
     не связанных с TODAY. Теперь от сегодня. */
  const a = dayOffset(TODAY + 14), b = dayOffset(TODAY + 20);
  const when = document.getElementById('lockwhen');
  if(when) when.textContent = 'Two weeks from now · ' + MON[a.getMonth()] + ' ' + a.getDate()
    + '–' + (a.getMonth() === b.getMonth() ? b.getDate()
            : MON[b.getMonth()] + ' ' + b.getDate());
  const head = document.getElementById('lockhead');
  const cnt = Math.min(3, weekTasks().length);
  if(head) head.innerHTML = (WORDNUM[cnt] || cnt) + (cnt === 1 ? ' task' : ' tasks')
    + '<br><span class="m">already planned.</span>';
  if(!MY_PLANTS.length){
    box.innerHTML='<div class="note" style="margin-top:16px"><b>Nothing is scheduled yet</b>'
      +'<p>Add a plant and the weeks ahead fill themselves in — that is what Pro keeps open.</p>'
      +'<div class="btn b-pri" data-go="add-plant">Add a plant</div></div>';
    return;
  }
  if(IS_PRO){
    const t = weekTasks();
    box.innerHTML='<div class="sl">What they are</div>'
      + t.slice(0,3).map(taskHTML).join('')
      +'<div class="note" style="margin-top:12px"><b>You have the whole calendar</b>'
      +'<p>Every week ahead is planned. Nothing is hidden any more.</p></div>';
    return;
  }
  box.innerHTML='<div class="sl">What they are</div>'
    +'<div class="task"><div class="box"></div><div class="tt"><div class="blur" style="width:76%;margin-bottom:8px">'
    +'</div><div class="blur" style="width:52%"></div></div><div class="min">4 min</div></div>'
    +'<div class="task"><div class="box"></div><div class="tt"><div class="blur" style="width:60%"></div></div>'
    +'<div class="min">3 min</div></div>'
    +'<div class="task"><div class="box"></div><div class="tt"><div class="blur" style="width:68%"></div></div>'
    +'<div class="min">10 min</div></div>'
    +'<div class="acc" style="margin-top:16px"><div class="row1"><span class="tag">Locked</span></div>'
    +'<div class="big" style="font-size:var(--t-24);margin-top:16px">Pro unlocks<br>the whole calendar</div>'
    +'<div class="sub">The dates and the workload are real — only the wording is hidden.</div>'
    +'<div class="btn b-lime" data-go="paywall">Unlock the full plan</div></div>';
}
/* ═════════ НАСТРОЙКИ: каждая строка реально меняет поведение ═════════ */
let UNITS = 'imperial';
let REMIND = 3;                                   // индекс в REMIND_AT
const REMIND_AT = ['07:00', '09:00', '12:00', '18:00', '21:00'];
/* какие типы задач попадают в недельную карточку. Полив не отключается —
   это ядро продукта. Остальное — выбор пользователя. */
const CARE = { pick: true, leaf: true, rotate: true, feed: true };
const MAIL = { weekly: true, water: true, news: false };

/* перевод объёмов и диаметров. Настоящие пересчёты, не подписи «на глаз». */
const POT_METRIC = {'6 inch':'15 cm', '8 inch':'20 cm', '10 inch':'25 cm', '12 inch':'30 cm',
  '1 pint':'0.5 L', '1 quart':'1 L', '0.5 gal':'2 L', '1 gal':'4 L',
  '2 gal':'7.5 L', '3 gal':'11 L', '5 gal':'19 L', 'tray':'tray'};
const fmtPot = v => UNITS === 'metric' ? (POT_METRIC[v] || v) : v;

/* Типичные справочные значения последних заморозков и длины сезона.
   Ими же питается карточка климата на Q2 — раньше она всегда говорила Austin. */
const ZIPS = [
  {zip:'78704', city:'Austin, TX',   zone:'8b', frost:'Mar 3',  season:270},
  {zip:'97214', city:'Portland, OR', zone:'8b', frost:'Apr 5',  season:230},
  {zip:'10025', city:'New York, NY', zone:'7b', frost:'Apr 15', season:200},
  {zip:'60613', city:'Chicago, IL',  zone:'6a', frost:'May 5',  season:170}
];
const zipInfo = () => ZIPS.find(function(z){ return z.zip === CHOICES.zip; }) || ZIPS[0];

const SPACE_OPTS = {
  house: ['living room','bedroom','kitchen','bathroom','home office','windowsill'],
  edible: ['patio','deck','porch','backyard','raised bed','balcony','windowsill'],
  both: ['living room','kitchen','windowsill','patio','balcony','backyard']
};
const LIGHT_IN  = ['a south-facing window','an east or west window','a north window'];
const LIGHT_OUT = ['3–5 hours of sun','6–8 hours of sun','8+ hours of sun'];
const LIGHT_RANK_IN  = {'a south-facing window':2,'an east or west window':1,'a north window':1};
const LIGHT_RANK_OUT = {'3–5 hours of sun':1,'6–8 hours of sun':2,'8+ hours of sun':3};

function cycle(list, cur){ const i = list.indexOf(cur); return list[(i + 1) % list.length]; }

function setRow(key, label, value){
  return '<div class="pl" role="button" tabindex="0" data-set="' + key + '" '
   + 'aria-label="' + label + ': ' + value + '. Opens a list of options">'
   + '<div class="nm"><b>' + label + '</b><s>' + value + '</s></div>'
   + ICONS._chev + '</div>';
}
function swRow(key, label, on, sub){
  return '<div class="pl tglrow" role="switch" tabindex="0" aria-label="' + label + '" '
   + 'aria-checked="' + (on ? 'true' : 'false') + '" data-sw="' + key + '">'
   + '<div class="nm"><b>' + label + '</b>' + (sub ? '<s>' + sub + '</s>' : '') + '</div>'
   + '<div class="tgl' + (on ? ' on' : '') + '" aria-hidden="true"><i></i></div></div>';
}
function renderSettingsPlan(){
  const el = document.getElementById('planbox'); if(!el) return;
  const pic = MY_PLANTS.length && MY_PLANTS[0].s.img
    ? 'img/' + MY_PLANTS[0].s.img + '.jpg' : 'img/hero-plants.jpg';
  const shot = '<div class="acc-photo" style="background-image:url(' + pic + ')"></div>';
  el.innerHTML = IS_PRO
   ? '<div class="acc" style="margin-top:16px">' + shot
     + '<div class="row1"><span class="tag">Pro · full plan</span></div>'
     + '<div class="big" style="font-size:var(--t-24);margin-top:12px">Everything is open</div>'
     + '<div class="sub">Every week planned, unlimited plants and photos, full export. '
     + 'Renews Mar 14, 2027.</div>'
     + '<div class="btn" style="background:#17492F;color:#fff" data-unpro>Back to Free (demo)</div></div>'
   : '<div class="acc" style="margin-top:16px">' + shot
     + '<div class="row1"><span class="tag">Free plan</span></div>'
     + '<div class="big" style="font-size:var(--t-24);margin-top:12px">1 space · 3 plants<br>'
     + 'this week only</div>'
     + '<div class="sub">Pro opens every week ahead, the whole library and unlimited photos.</div>'
     + '<div class="btn b-lime" data-go="paywall">Compare with Pro</div></div>';
}
function renderSettingsSetup(){
  const el = document.getElementById('setupbox'); if(!el) return;
  const mins = CHOICES.effort === 3 ? 10 : CHOICES.effort === 4 ? 20 : 30;
  /* Growing здесь нет: чем ты занимаешься, выбирается один раз в онбординге. */
  let h = setRow('space', 'Space', CHOICES.space);
  if(CHOICES.outdoor) h += setRow('zip', 'ZIP', zipInfo().zip + ' · ' + zipInfo().city);
  h += setRow('light', 'Light', CHOICES.sun);
  h += setRow('effort', 'Time per week', mins + ' minutes');
  h += setRow('units', 'Units', UNITS === 'metric' ? 'Metric · cm, litres' : 'Imperial · inches, gallons');
  el.innerHTML = '<div class="sl">Your setup</div><div class="plist">' + h + '</div>'
   + '<div class="setnote">You picked ' + TRACKWORD[CHOICES.track].toLowerCase()
   + ' when you set up your plan. That one stays put.</div>';
}
function renderSettingsCare(){
  const el = document.getElementById('carebox'); if(!el) return;
  const hasEdible = MY_PLANTS.some(isEdible);
  let h = '<div class="pl"><div class="nm"><b>Watering</b>'
        + '<s>Always on — it is what keeps them alive</s></div>'
        + '<span class="setval">Always</span></div>';
  if(hasEdible) h += swRow('pick', 'Harvest reminders', CARE.pick, 'When something is ready to pick');
  h += swRow('leaf', 'Leaf care', CARE.leaf, 'Wiping dust off the big leaves');
  h += swRow('rotate', 'Rotating', CARE.rotate, 'A quarter turn so growth stays even');
  h += swRow('feed', 'Feeding', CARE.feed, 'Once a month while they are growing');
  el.innerHTML = '<div class="sl">What goes on the week card</div><div class="plist">' + h + '</div>';
}
function renderSettingsRemind(){
  const el = document.getElementById('remindbox'); if(!el) return;
  el.innerHTML = '<div class="sl">Reminders</div><div class="plist">'
   + setRow('remind', 'Remind me at', REMIND_AT[REMIND])
   + swRow('weekly', 'Weekly task email', MAIL.weekly)
   + swRow('water', 'Watering reminders', MAIL.water)
   + swRow('news', 'Product updates', MAIL.news)
   + '</div>';
}
function renderSettingsData(){
  const el = document.getElementById('databox'); if(!el) return;
  el.innerHTML = '<div class="sl">Data</div><div class="plist">'
   + '<div class="pl" role="button" tabindex="0" data-export>'
   + '<div class="nm"><b>Export my plants</b><s>' + MY_PLANTS.length
   + (MY_PLANTS.length === 1 ? ' plant' : ' plants') + ' and '
   + allPhotos().length + ' photos as JSON</s></div>'
   + '<span class="setval">Download</span>' + ICONS._chev + '</div></div>'
   + '<div class="danger" role="button" tabindex="0" data-del-acct>Delete account</div>'
   + '<div class="dangernote">Asks you to type DELETE first. Your plants go with it.</div>';
}
function renderSettings(){
  renderSettingsPlan(); renderSettingsSetup(); renderSettingsRemind();
  renderSettingsCare(); renderSettingsData();
}
function exportPlants(){
  const payload = { app: 'HOMEGROWN', exported: 'prototype demo',
    units: UNITS, track: CHOICES.track,
    plants: MY_PLANTS.map(function(p){
      return { id: p.s.id, name: p.s.name, kind: p.s.kind, latin: p.s.latin,
               ageDays: p.day, daysSinceWater: p.since,
               waterEvery: p.s.water, photos: p.photos.length }; }) };
  try{
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = 'homegrown-plants.json';
    document.body.appendChild(a); a.click();
    setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 0);
    toast('<span>Exported ' + MY_PLANTS.length
      + (MY_PLANTS.length === 1 ? ' plant' : ' plants') + '</span>');
  }catch(e){
    toast('<span>Export is not available in this browser</span>');
  }
}
/* ─────────── раздел выбора значения ─────────── */
let PICK_KEY = 'space';
const PICKS = {
  space:  {title:'Where it lives',  note:'Changes what the library offers you.'},
  zip:    {title:'Your ZIP',        note:'Frost dates decide what can go outside and when.'},
  light:  {title:'How much light',  note:'The single biggest filter on what will actually finish.'},
  effort: {title:'Time per week',   note:'Sets how many plants the plan holds.'},
  units:  {title:'Units',           note:'Applies to pot sizes across the whole app.'},
  remind: {title:'Remind me at',    note:'One notification a day, at this time.'}
};
function pickOptions(key){
  if(key === 'space')  return (SPACE_OPTS[CHOICES.track] || SPACE_OPTS.both).map(function(v){
    return {v:v, label:cap(v), sub:isOutdoorSpace(cap(v)) ? 'Outside' : 'Indoors'}; });
  if(key === 'zip')    return ZIPS.map(function(z){
    return {v:z.zip, label:z.zip + ' · ' + z.city,
            sub:'Zone ' + z.zone + ' · last frost ' + z.frost + ' · ' + z.season + '-day season'}; });
  if(key === 'light'){ const L = CHOICES.outdoor ? LIGHT_OUT : LIGHT_IN;
    const R = CHOICES.outdoor ? LIGHT_RANK_OUT : LIGHT_RANK_IN;
    return L.map(function(v){ return {v:v, label:cap(v),
      sub:'Fits ' + speciesPool().filter(function(s){ return s.sun <= R[v]; }).length
          + ' of ' + speciesPool().length + ' plants'}; }); }
  if(key === 'effort') return [{v:3,label:'About 10 minutes',sub:'3 plants'},
                               {v:4,label:'About 20 minutes',sub:'4 plants'},
                               {v:6,label:'30+ minutes',sub:'up to 6 plants'}];
  if(key === 'units')  return [{v:'imperial',label:'Imperial',sub:'inches, gallons, pints'},
                               {v:'metric',label:'Metric',sub:'centimetres, litres'}];
  if(key === 'remind') return REMIND_AT.map(function(t, i){
    return {v:i, label:t, sub:i <= 1 ? 'Before the day starts'
                            : i === 2 ? 'Midday' : 'After work'}; });
  return [];
}
function currentPick(key){
  if(key === 'space')  return CHOICES.space;
  if(key === 'zip')    return CHOICES.zip;
  if(key === 'light')  return CHOICES.sun;
  if(key === 'effort') return CHOICES.effort;
  if(key === 'units')  return UNITS;
  if(key === 'remind') return REMIND;
  return null;
}
function renderPick(){
  const box = document.getElementById('pickbody'); if(!box) return;
  const meta = PICKS[PICK_KEY] || PICKS.space;
  const h1 = document.getElementById('pickhead');
  if(h1) h1.textContent = meta.title;
  const nt = document.getElementById('picknote');
  if(nt) nt.textContent = meta.note;
  const cur = currentPick(PICK_KEY);
  box.innerHTML = '<div class="plist">' + pickOptions(PICK_KEY).map(function(o){
    const on = String(o.v) === String(cur);
    return '<div class="pl pickrow' + (on ? ' on' : '') + '" role="radio" tabindex="0" '
      + 'aria-checked="' + (on ? 'true' : 'false') + '" data-pickval="' + o.v + '">'
      + '<div class="nm"><b>' + o.label + '</b><s>' + o.sub + '</s></div>'
      + '<span class="picktick">' + ICONS._checkg + '</span></div>';
  }).join('') + '</div>';
}
function applyPick(raw){
  const key = PICK_KEY;
  if(key === 'space'){
    CHOICES.space = raw;
    CHOICES.outdoor = isOutdoorSpace(cap(raw));
    /* свет живёт в двух разных доменах: часы солнца снаружи, сторона окна внутри */
    if(!CHOICES.outdoor && LIGHT_IN.indexOf(CHOICES.sun) < 0){
      CHOICES.sun = LIGHT_IN[1]; CHOICES.sunRank = LIGHT_RANK_IN[CHOICES.sun];
    }
    if(CHOICES.outdoor && LIGHT_OUT.indexOf(CHOICES.sun) < 0){
      CHOICES.sun = LIGHT_OUT[1]; CHOICES.sunRank = LIGHT_RANK_OUT[CHOICES.sun];
    }
  }
  else if(key === 'zip'){ CHOICES.zip = raw;
    toast('<span>Frost dates set for ' + zipInfo().city + '</span>'); }
  else if(key === 'light'){ CHOICES.sun = raw;
    CHOICES.sunRank = (CHOICES.outdoor ? LIGHT_RANK_OUT : LIGHT_RANK_IN)[raw] || 1;
    toast('<span>The library now shows what fits ' + raw + '</span>'); }
  else if(key === 'effort') CHOICES.effort = +raw;
  else if(key === 'units')  UNITS = raw;
  else if(key === 'remind'){ REMIND = +raw;
    toast('<span>Reminders at ' + REMIND_AT[REMIND] + '</span>'); }
  renderSettings(); renderAll(); go('settings');
}
function toggleSetting(key){
  if(CARE.hasOwnProperty(key)) CARE[key] = !CARE[key];
  else if(MAIL.hasOwnProperty(key)) MAIL[key] = !MAIL[key];
  DONE = {};
  renderSettings(); renderAll();
}
const TRACKWORD = {house:'Houseplants', edible:'Edible crops', both:'Houseplants and edibles'};

/* ─────────── скан: настоящее распознавание через PlantNet ─────────── */
// латинское имя → id вида. Ключи — род или вид, как их отдаёт PlantNet.
const LATIN = {
  'Monstera deliciosa':'monstera', 'Monstera':'monstera',
  'Dracaena trifasciata':'snakeplant', 'Sansevieria trifasciata':'snakeplant',
  'Epipremnum aureum':'pothos', 'Epipremnum':'pothos',
  'Zamioculcas zamiifolia':'zzplant', 'Zamioculcas':'zzplant',
  'Ficus lyrata':'fiddleleaf', 'Ficus':'fiddleleaf',
  'Spathiphyllum wallisii':'peacelily', 'Spathiphyllum':'peacelily',
  'Aloe vera':'aloe', 'Aloe':'aloe',
  'Goeppertia orbifolia':'calathea', 'Goeppertia':'calathea', 'Calathea':'calathea',
  'Ocimum basilicum':'basil', 'Ocimum':'basil',
  'Raphanus sativus':'radish', 'Raphanus':'radish',
  'Lactuca sativa':'lettuce', 'Lactuca':'lettuce',
  'Coriandrum sativum':'cilantro', 'Coriandrum':'cilantro',
  'Petroselinum crispum':'parsley', 'Petroselinum':'parsley',
  'Allium tuberosum':'chives', 'Allium schoenoprasum':'chives',
  'Allium fistulosum':'onions', 'Allium cepa':'onions', 'Allium':'onions',
  'Solanum lycopersicum':'cherrytomato', 'Lycopersicon esculentum':'cherrytomato',
  'Solanum melongena':'eggplant',
  'Capsicum annuum':'pepper', 'Capsicum':'pepper',
  'Cucumis sativus':'cucumber', 'Cucumis':'cucumber',
  'Cucurbita pepo':'squash', 'Cucurbita':'squash',
  'Beta vulgaris':'chard', 'Beta':'beets',
  'Daucus carota':'carrots', 'Daucus':'carrots',
  'Brassica oleracea':'kale', 'Brassica juncea':'mustard',
  'Brassica rapa':'turnips', 'Brassica':'kale',
  'Phaseolus vulgaris':'beans', 'Phaseolus':'beans',
};
function matchSpecies(r){
  const byLatin = LATIN[r.latin] || LATIN[r.genus];
  if(byLatin) return SP(byLatin);
  // Подстраховка по обиходному имени. Только безопасное направление: обиходное имя
  // целиком содержит наше. Обратное давало 'Pea' → Peace lily и '' → первый вид в списке.
  const names = (r.common || [])
    .map(function(n){ return (n || '').toLowerCase().trim(); })
    .filter(function(n){ return n.length >= 4; });
  for(let i = 0; i < SPECIES.length; i++){
    const n = SPECIES[i].name.toLowerCase();
    if(names.some(function(c){
      return c === n || (c.indexOf(n) > -1 && c.length - n.length <= 12);
    })) return SPECIES[i];
  }
  return null;
}
let SCAN_URL = null, SCAN_FILE = null;
/* снимок, ждущий, пока человек выберет вид в библиотеке */
let SCAN_KEEP = null;
function scanShot(){
  return SCAN_URL ? '<div class="scan-shot" style="background-image:url(' + SCAN_URL + ')"></div>'
                  : '<div class="scan-shot"></div>';
}
function scanBusy(){
  document.getElementById('scanbody').innerHTML = scanShot()
    + '<div class="scan-ov"><div class="scan-frame"></div>'
    + '<div class="scan-foot"><div class="scan-dots"><i></i><i></i><i></i></div>'
    + '<b>Looking at your plant…</b>'
    + '<s>Sending the photo to PlantNet</s></div></div>';
}
function scanFoot(inner){
  document.getElementById('scanbody').innerHTML = scanShot()
    + '<div class="scan-ov"><div class="scan-frame ok"></div>'
    + '<div class="scan-foot">' + inner + '</div></div>';
}
function scanManual(label){
  /* data-scanpick, а не data-go: снимок надо донести до библиотеки,
     чтобы он стал первой фотографией растения */
  return '<div class="btn" style="background:#1B3527;color:#fff" data-scanpick>'
    + (label || 'Choose manually') + '</div>';
}
function scanRetry(){
  return '<div class="btn b-lime" data-scan>Try another photo</div>';
}
async function identify(file){
  const url = window.HG_SCAN_ENDPOINT;
  if(!url){
    /* Распознавание не подключено. Не выдумываем ответ и не делаем вид, что
       это ошибка: снимок сделан, дальше человек выбирает вид сам, а фото
       уезжает в журнал вместе с растением. */
    scanFoot('<span class="pill b-lime" style="align-self:flex-start">Photo saved</span>'
      + '<b style="margin-top:12px">Which one is it?</b>'
      + '<s>Automatic recognition is not switched on, so we won’t guess at your plant. '
      + 'Pick it from the library and this photo becomes its first journal shot.</s>'
      + scanManual('Pick from ' + SPECIES.length + ' plants'));
    return;
  }
  try{
    const fd = new FormData();
    fd.append('images', file, 'plant.jpg');
    fd.append('organs', 'auto');
    const res = await fetch(url, { method:'POST', body: fd });
    const data = await res.json();
    if(data.error || !data.results || !data.results.length){
      scanFoot('<b>No match</b><s>PlantNet didn’t recognise this one. '
        + 'Try a closer shot of a single leaf, or pick it yourself — the photo stays.</s>'
        + scanRetry() + scanManual());
      return;
    }
    const top = data.results[0];
    const pct = Math.round((top.score || 0) * 100);
    const s = matchSpecies(top);
    const latin = '<em>' + (top.latin || '—') + '</em>';
    const common = (top.common && top.common[0]) ? top.common[0] : '';
    if(!s){
      scanFoot('<span class="pill" style="background:#3A3020;color:#F0C674;align-self:flex-start">'
        + pct + '% ' + (common || 'identified') + '</span>'
        + '<b style="margin-top:12px">Not in our library</b>'
        + '<s>' + latin + ' isn’t one of the ' + SPECIES.length
        + ' plants HOMEGROWN knows how to care for. You can still add one yourself.</s>'
        + scanRetry() + scanManual());
      return;
    }
    scanFoot('<span class="pill b-lime" style="align-self:flex-start">' + pct + '% match</span>'
      + '<b style="margin-top:12px">' + s.name + '</b>'
      + '<s>' + latin + (common ? ' · ' + common : '') + '<br>' + spSub(s)
      + (fitsLight(s) ? '' : ' · needs more light than you have') + '</s>'
      + '<div class="btn b-lime" data-scanadd="' + s.id + '">Add ' + lc(s.name)
      + ' to my plants</div>' + scanManual('Not it — choose manually'));
  }catch(err){
    scanFoot('<b>Couldn’t reach the service</b>'
      + '<s>Check the connection and try again — the photo is still here.</s>'
      + scanRetry() + scanManual());
  }
}
function startScan(file){
  SCAN_FILE = file || null;
  SCAN_URL = file ? URL.createObjectURL(file) : null;
  go('scan'); scanBusy();
  identify(file);
}
/* ─────────── камера ─────────── */
let CAM_TARGET = null, CAM_MODE = 'photo';
function openCamera(target, mode){
  CAM_MODE = mode || 'photo';
  CAM_TARGET = (target===undefined || target===null) ? SELECTED : target;
  const el = document.getElementById('cam');
  if(el){ el.value=''; el.click(); }
}
function attachShot(file){
  if(CAM_MODE === 'scan'){ startScan(file); return; }
  if(!file || !MY_PLANTS.length) return;
  const i = (CAM_TARGET!==null && MY_PLANTS[CAM_TARGET]) ? CAM_TARGET : 0;
  const p = MY_PLANTS[i];
  p.photos.unshift({u: URL.createObjectURL(file), day: TODAY});
  renderAll();
  const t=document.getElementById('toast');
  t.innerHTML='<span>Photo added to '+p.s.name+'</span><b data-gogrowth>See journal</b>';
  t.classList.add('on'); clearTimeout(UNDOT);
  UNDOT=setTimeout(function(){t.classList.remove('on')}, 4000);
}

/* ─────────── виджет-сетка дашборда ─────────── */
const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const START = new Date(2026, 2, 14);
function dayOffset(d){ const x = new Date(START); x.setDate(x.getDate() + d); return x; }
function arc(pct, sz, dark){
  const sw = 5, r = (sz - sw) / 2, c = 2 * Math.PI * r, off = c * (1 - Math.min(100, pct) / 100);
  return '<svg aria-hidden="true" width="' + sz + '" height="' + sz + '" viewBox="0 0 ' + sz + ' ' + sz + '">'
   + '<circle cx="' + sz/2 + '" cy="' + sz/2 + '" r="' + r + '" fill="none" stroke="'
   + (dark ? 'rgba(255,255,255,.18)' : '#E4E8E2') + '" stroke-width="' + sw + '"/>'
   + '<circle cx="' + sz/2 + '" cy="' + sz/2 + '" r="' + r + '" fill="none" stroke="'
   + (dark ? '#B4F461' : '#22A559') + '" stroke-width="' + sw + '" stroke-linecap="round"'
   + ' stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '"'
   + ' transform="rotate(-90 ' + sz/2 + ' ' + sz/2 + ')"/></svg>';
}
function metricRow(items){
  return '<div class="mrow">' + items.map(function(m){
    return '<div><s>' + m[0] + '</s><b>' + m[1] + '</b></div>';
  }).join('') + '</div>';
}
function careStats(){
  const due = MY_PLANTS.filter(function(p){ return wDue(p) <= 0; });
  let waterings = 0;
  MY_PLANTS.forEach(function(p){ waterings += Math.floor((p.day - p.since) / p.s.water) + 1; });
  return { plants: MY_PLANTS.length, due: due.length, photos: allPhotos().length,
           score: healthScore(), waterings: Math.max(0, waterings),
           soon: MY_PLANTS.filter(function(p){ const d = wDue(p); return d > 0 && d <= 2; }).length,
           edible: MY_PLANTS.filter(isEdible).length,
           ready: MY_PLANTS.filter(function(p){ return isEdible(p) && hPct(p) >= 100; }).length,
           oldest: MY_PLANTS.reduce(function(a,p){ return Math.max(a, p.day); }, 0),
           healthy: MY_PLANTS.filter(function(p){ return wDue(p) > 2; }).length };
}
/* ─────────── календарь урожая ─────────── */
const MON1 = ['J','F','M','A','M','J','J','A','S','O','N','D'];
function frostDates(){
  const parts = zipInfo().frost.split(' ');
  const last = new Date(2026, MON.indexOf(parts[0]), +parts[1]);
  const first = new Date(last); first.setDate(first.getDate() + zipInfo().season);
  return {last: last, first: first};
}
/* Окно посева: холодостойкие уходят в грунт за месяц до последних заморозков,
   теплолюбивые — только после. Крайний срок считается так, чтобы культура
   успела отдать урожай до первых осенних заморозков. */
function windows(sp){
  if(sp.kind === 'house') return null;
  const f = frostDates();
  const from = new Date(f.last);
  if(sp.cool) from.setDate(from.getDate() - 28);
  const to = new Date(f.first);
  to.setDate(to.getDate() - sp.daysMax - 14);
  if(to < from) return {sow:[from, from], pick:[from, from], tight:true};
  const pickFrom = new Date(from); pickFrom.setDate(pickFrom.getDate() + sp.days);
  const pickTo = new Date(to); pickTo.setDate(pickTo.getDate() + sp.daysMax);
  return {sow:[from, to], pick:[pickFrom, pickTo], tight:false};
}
const monthsOf = (a, b) => {
  const out = {};
  const d = new Date(a.getFullYear(), a.getMonth(), 1);
  while(d <= b){ out[d.getMonth()] = 1; d.setMonth(d.getMonth() + 1); }
  return out;
};
function monthMap(sp){
  const w = windows(sp);
  if(!w) return null;                                  // комнатное: круглый год
  const sow = monthsOf(w.sow[0], w.sow[1]), pick = monthsOf(w.pick[0], w.pick[1]);
  return MON1.map(function(_, m){
    if(sow[m] && pick[m]) return 'both';    // и сеять можно, и что-то снимаешь
    if(sow[m]) return 'sow';
    if(pick[m]) return 'pick';
    return '';
  });
}
const nowMonth = () => dayOffset(TODAY).getMonth();
function sowableNow(){
  return speciesPool().filter(function(sp){
    const mm = monthMap(sp);
    const k = mm && mm[nowMonth()];
    return k === 'sow' || k === 'both';
  });
}
function calStrip(sp){
  const mm = monthMap(sp);
  const now = nowMonth();
  const cells = MON1.map(function(_, m){
    const k = mm ? mm[m] : 'any';
    return '<i class="' + (k ? 'c-' + k : '') + (m === now ? ' cnow' : '') + '"></i>';
  }).join('');
  return '<div class="calrow"><b>' + sp.name + '</b><div class="cal12">' + cells + '</div></div>';
}
function renderCalendar(){
  const box = document.getElementById('calbody'); if(!box) return;
  const f = frostDates();
  const sub = document.getElementById('calsub');
  if(sub) sub.textContent = CHOICES.outdoor
    ? zipInfo().city + ' · last frost ' + zipInfo().frost + ' · first frost around '
      + MON[f.first.getMonth()] + ' ' + f.first.getDate()
    : 'Indoors, so there is no frost to work around — any month works.';
  const mine = MY_PLANTS.map(function(p){ return p.s; });
  const seen = {}; const mineU = mine.filter(function(x){
    if(seen[x.id]) return false; seen[x.id] = 1; return true; });
  const rest = speciesPool().filter(function(x){ return !seen[x.id]; });
  const head = '<div class="calrow calhead"><b></b><div class="cal12">'
    + MON1.map(function(m, i){
        return '<i class="' + (i === nowMonth() ? 'cnow' : '') + '">' + m + '</i>'; }).join('')
    + '</div></div>';
  box.innerHTML =
      '<div class="calleg2"><span><i class="c-sow"></i>sow</span>'
    + '<span><i class="c-both"></i>sow &amp; pick</span>'
    + '<span><i class="c-pick"></i>pick only</span>'
    + '<span><i class="cnow"></i>this month</span></div>'
    + (mineU.length ? '<div class="sl">Yours</div><div class="calbox">' + head
        + mineU.map(calStrip).join('') + '</div>' : '')
    + '<div class="sl">' + (mineU.length ? 'Could also go in' : 'What can go in') + '</div>'
    + '<div class="calbox">' + head + rest.map(calStrip).join('') + '</div>'
    + '<div class="setnote">Windows come from your last frost date and how long each crop needs. '
      + 'Houseplants have no season, so their row stays open all year.<br><br>'
      + 'One honest gap: this works off frost, not summer heat. In a hot region the '
      + 'cool-season crops — lettuce, radish, cilantro — will bolt in midsummer even though '
      + 'the row here stays open. Sow those in spring and again in late summer.</div>';
}
/* Виджет — предпросмотр календаря урожая, а не журнал поливов: заголовок
   обещал урожай, а внутри была сетка поливов за 35 дней. Показываем год
   по месяцам, сложенный по всем растениям человека. */
function calWidget(){
  const mine = MY_PLANTS.map(function(p){ return p.s; });
  const now = nowMonth();
  const cells = MON1.map(function(lbl, m){
    let sow = 0, pick = 0;
    mine.forEach(function(sp){
      const mm = monthMap(sp); if(!mm) return;
      if(mm[m] === 'sow' || mm[m] === 'both') sow++;
      if(mm[m] === 'pick' || mm[m] === 'both') pick++;
    });
    const k = pick && sow ? 'c-both' : pick ? 'c-pick' : sow ? 'c-sow' : '';
    return '<i class="' + k + (m === now ? ' cnow' : '') + '">' + lbl + '</i>';
  }).join('');
  const can = sowableNow();
  return '<div class="wg wg-lite span2" role="button" tabindex="0" data-go="calendar">'
    + '<div class="wg-h"><b>Harvest calendar</b><s>' + MON[now] + '</s></div>'
    + '<div class="calyear">' + cells + '</div>'
    + '<div class="calcta">' + (can.length
        ? can.length + (can.length === 1 ? ' crop can go in this month' : ' crops can go in this month')
        : 'Nothing new should go in this month') + ' · see the whole year</div></div>';
}
function careWidgets(){
  return '<div class="wgrid">' + calWidget() + '</div>';
}
function renderDash(){
  const el = document.getElementById('dash'); if(!el) return;
  const st = careStats();
  const sub = document.getElementById('caresub');
  if(sub) sub.textContent = MY_PLANTS.length
    ? st.plants + (st.plants === 1 ? ' plant in your care' : ' plants in your care')
    : 'No plants yet';
  if(!MY_PLANTS.length){
    el.innerHTML = '<div class="note" style="margin-top:16px"><b>Nothing to show yet</b>'
      + '<p>Add a plant and this page starts keeping its history — waterings, photos, how it changed.</p>'
      + '<div class="btn b-pri" data-go="add-plant">Add a plant</div></div>';
    return;
  }
  const v = verdict(st.score, st.due);
  el.innerHTML = '<div class="acc"><div class="row1"><span class="tag">Plant parent</span></div>'
    + '<div class="lbl">Health score</div>'
    + '<div class="scorehead"><div class="huge">' + st.score + '</div>'
    + '<div class="huge-of">of 100</div></div>'
    + '<div class="pb-track accbar"><i style="width:' + st.score + '%"></i></div>'
    + '<div class="sub">' + v[0] + ' — ' + v[1].toLowerCase() + '. '
    + st.photos + (st.photos === 1 ? ' photo' : ' photos') + ' in the journal.</div>'
    + '<div class="duo"><div class="cell"><s>Thirsty</s><b>' + st.due + '</b></div>'
    + '<div class="cell"><s>Soon</s><b>' + st.soon + '</b></div>'
    + '<div class="cell"><s>Fine</s><b>' + st.healthy + '</b></div></div></div>'
    + careWidgets();
}
function plantRow(p, i){
  const st = pState(p);
  const strip = p.photos.length
    ? '<div class="cstrip">' + p.photos.map(function(x){
        return '<div style="background-image:url(' + phUrl(x) + ')"></div>'; }).join('') + '</div>'
    : '<div class="cempty" data-shoot="' + i + '">' + ICONS._cam + '<span>No photos yet — take one</span></div>';
  return '<div class="ccard"><div class="chead" data-open="' + i + '">'
    + '<div class="nm"><b>' + p.s.name + '</b><s class="st-' + st[1] + '">' + st[0]
    + '</s></div>' + ICONS._chev + '</div>' + strip + '</div>';
}
function renderPlantCards(){
  const el = document.getElementById('plantcards'); if(!el) return;
  if(!MY_PLANTS.length){ el.innerHTML = ''; return; }
  const thirsty = [], fine = [];
  MY_PLANTS.forEach(function(p, i){ (wDue(p) <= 2 ? thirsty : fine).push([p, i]); });
  let h = '';
  if(thirsty.length) h += '<div class="sl">Needs attention</div>'
                          + thirsty.map(function(x){ return plantRow(x[0], x[1]); }).join('');
  if(fine.length)    h += '<div class="sl">Doing fine</div>'
                          + fine.map(function(x){ return plantRow(x[0], x[1]); }).join('');
  h += addPhotoBtn();
  el.innerHTML = h;
}

/* ─────────── экраны-моменты: milestone, recap, покупки ─────────── */
function renderMilestone(){
  const box = document.getElementById('milebody'); if(!box) return;
  const ready = MY_PLANTS.filter(function(p){ return isEdible(p) && hPct(p) >= 100; })[0];
  const p = ready || MY_PLANTS.slice().sort(function(a,b){ return b.day - a.day; })[0];
  if(!p){
    box.innerHTML = '<div class="mile-tx"><span class="pill b-lime">Nothing yet</span>'
      + '<div class="cap-f mile-h">Add a plant<br>and this fills up.</div>'
      + '<div class="mile-s">Every first — a new leaf, a first pick — lands here.</div>'
      + '<div class="btn b-lime" data-go="add-plant">Add a plant</div></div>';
    return;
  }
  const pic = p.photos[0] ? phUrl(p.photos[0]) : (p.s.img ? 'img/' + p.s.img + '.jpg' : null);
  const shot = pic
    ? '<div class="shot" style="background-image:url(' + pic + ');height:58%"></div>'
      + '<div class="scrim mile-scrim"></div>'
    : '<div class="shot" style="height:58%;' + photoStyle(p.s) + '"></div>'
      + '<div class="scrim mile-scrim"></div>';
  const edible = isEdible(p) && hPct(p) >= 100;
  const head = edible ? 'First harvest.' : 'It is thriving.';
  const pill = edible ? 'Day ' + p.day : p.s.name;
  const sub = edible
    ? 'You grew this ' + inOn() + CHOICES.space + '. ' + p.s.name
      + ' is ready — pick it and it keeps producing.'
    : p.s.name + ' has been with you ' + p.day + ' days and '
      + careStats().waterings + ' waterings. That is the whole trick: showing up.';
  box.innerHTML = shot
    + '<div class="mile-ov">'
    + '<div class="xbtn" role="button" tabindex="0" aria-label="Close" style="align-self:flex-end" data-go="growth">' + ICONS._x2 + '</div>'
    + '<div style="flex:1"></div>'
    + '<span class="pill b-lime" style="align-self:flex-start">' + pill + '</span>'
    + '<div class="cap-f mile-h">' + head + '</div>'
    + '<div class="mile-s">' + sub + '</div>'
    + '<div class="btn b-lime" data-addphoto>Add a photo</div>'
    + '<div class="btn" style="background:#1B3527;color:#fff" data-go="growth">Back to my plants</div>'
    + '</div>';
}
function renderRecap(){
  const box = document.getElementById('recapbody'); if(!box) return;
  const st = careStats();
  const outdoor = CHOICES.outdoor && st.edible;
  const pic = allPhotos()[0];
  const head = outdoor ? st.ready + (st.ready === 1 ? ' harvest.' : ' harvests.') + '<br>'
                         + st.oldest + ' days.'
                       : st.waterings + ' waterings.<br>' + st.plants
                         + (st.plants === 1 ? ' plant.' : ' plants.');
  const tag = outdoor ? 'SEASON 2026 · ' + zipInfo().city.toUpperCase()
                      : 'YOUR YEAR · YEAR-ROUND';
  const names = MY_PLANTS.map(function(p){ return p.s.name; });
  const list = names.length > 1
    ? names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1]
    : (names[0] || 'Nothing yet');
  const sub = outdoor
    ? list + ' all made it to the table. Next season starts in the fall window.'
    : list + ' are all still alive — that is the whole scoreboard. '
      + st.photos + (st.photos === 1 ? ' photo shows' : ' photos show') + ' how they changed.';
  box.innerHTML = '<div class="glow"></div>'
    + '<div class="xbtn" role="button" tabindex="0" aria-label="Close" style="align-self:flex-end" data-go="growth">' + ICONS._x2 + '</div>'
    + '<div class="recap-in">'
    + (pic ? '<div class="recap-ph" style="background-image:url(' + phUrl(pic) + ')"></div>'
           : '<div class="recap-ph" style="' + photoStyle(MY_PLANTS[0] ? MY_PLANTS[0].s : SPECIES[0]) + '"></div>')
    + '<span class="pill b-lime" style="align-self:flex-start;margin-top:20px">' + tag + '</span>'
    + '<div class="cap-f recap-h">' + head + '</div>'
    + '<div class="recap-s">' + sub + '</div></div>'
    + '<div class="btn b-lime" data-go="paywall">'
    + (outdoor ? 'Plan next season now' : 'Keep the whole calendar') + '</div>'
    + '<div class="btn" style="background:#1B3527;color:#fff" data-go="growth">Download recap</div>';
}
const POTPRICE = {'6 inch':6, '8 inch':8, '10 inch':12, '12 inch':16, 'tray':4,
  '1 pint':3, '1 quart':4, '0.5 gal':5, '1 gal':7, '2 gal':10, '3 gal':13, '5 gal':18};
function renderShopping(){
  const box = document.getElementById('shopbody'); if(!box) return;
  const plan = MY_PLANTS.length ? MY_PLANTS.map(function(p){ return p.s; }) : buildPlan();
  const edible = plan.filter(function(s){ return s.kind === 'edible'; });
  const pots = {};
  plan.forEach(function(s){ const k = s.pot || 'pot'; pots[k] = (pots[k] || 0) + 1; });
  const items = [];
  Object.keys(pots).forEach(function(k){
    const who = plan.filter(function(s){ return (s.pot || 'pot') === k; })
                    .map(function(s){ return lc(s.name); });
    items.push([(k === 'tray' ? 'Seed tray' : 'Pot — ' + fmtPot(k)) + (pots[k] > 1 ? ' ×' + pots[k] : ''),
      (POTPRICE[k] || 8) * pots[k],
      'For ' + (who.length > 1 ? who.slice(0,-1).join(', ') + ' and ' + who[who.length-1]
                               : who[0]) + '.']);
  });
  items.push(['Saucers ×' + plan.length, 2 * plan.length, 'Keeps water off the floor.']);
  items.push(['Potting mix, 1 cu ft', 12, 'Not garden soil — too much clay for a pot.']);
  items.push(['Watering can, 1 gal', 11, '']);
  items.push(['Liquid fertilizer', 9, 'Container soil runs out in about six weeks.']);
  if(edible.length) items.push(['Seed — ' + edible.map(function(s){ return lc(s.name); }).join(', '),
    3 * edible.length, '']);
  const total = items.reduce(function(a, x){ return a + x[1]; }, 0);
  const sub = document.getElementById('shopsum');
  if(sub) sub.textContent = 'Everything for ' + plan.length
    + (plan.length === 1 ? ' plant' : ' plants') + ' · about $' + total;
  box.innerHTML = '<div class="sl">Pots and soil</div>'
    + items.slice(0, items.length - (edible.length ? 1 : 0)).map(function(x){
        return taskHTML([x[0], '~$' + x[1], x[2]]); }).join('')
    + (edible.length ? '<div class="sl">Seed</div>'
        + taskHTML([items[items.length-1][0], '~$' + items[items.length-1][1], '']) : '')
    + '<div class="btn b-ghost" data-go="paywall">Printable PDF — Pro</div>';
}
function renderWeekEmpty(){
  const w = document.getElementById('wkplants'); if(!w) return;
  const note = document.getElementById('wkemptynote');
  const future = MY_PLANTS.filter(function(p){ return wDue(p) > 0; })
    .sort(function(a,b){ return wDue(a) - wDue(b); });
  const nextP = future[0];
  if(note) note.innerHTML = !MY_PLANTS.length
    ? '<b>Nothing to do yet</b><p>Add a plant and the week fills itself in.</p>'
    : nextP
    ? '<b>Just water and watch</b><p>Everything is on schedule. The next real job is '
      + (isEdible(nextP) && hPct(nextP) >= 100 ? 'picking the ' : 'watering the ')
      + lc(nextP.s.name) + ' ' + inDays(wDue(nextP)) + ' — '
      + 'we’ll put it on that week’s card.</p>'
    : '<b>Everything is thirsty at once</b><p>Water them today and the week clears itself. '
      + 'After that the schedule spreads them out again.</p>';
  w.innerHTML = MY_PLANTS.length
    ? '<div class="plist">' + MY_PLANTS.map(function(p, i){
        return '<div class="pl" data-open="' + i + '"><div class="rw">' + ringSVG(pPct(p))
         + '<i>' + ICONS[p.s.icon] + '</i></div>'
         + '<div class="nm"><b>' + p.s.name + '</b><s>' + pSub(p) + '</s></div>'
         + '<div class="eta">' + (isEdible(p) ? hEta(p)
              : (wDue(p) <= 0 ? 'water' : '~' + wDue(p) + 'd')) + '</div></div>';
      }).join('') + '</div>'
    : '';
}
function renderBack(){
  const box = document.getElementById('backtasks'); if(!box) return;
  const t = weekTasks().slice(0, 2);
  box.innerHTML = t.length ? t.map(taskHTML).join('')
    : '<div class="note"><b>Nothing is waiting</b><p>Your plants held out fine.</p></div>';
  const ln = document.getElementById('longnote');
  if(ln){
    const dry = MY_PLANTS.filter(function(p){ return wDue(p) <= 0; }).map(function(p){ return lc(p.s.name); });
    ln.textContent = dry.length
      ? 'The ' + dry.join(' and ') + ' may have dropped a leaf while you were away. '
        + 'If it did, that’s normal — water deeply once and it comes back.'
      : 'Nothing dried out completely. Water once, and the schedule picks up from today.';
  }
}
function renderWeekDone(){
  const box = document.getElementById('donebody'); if(!box) return;
  const st = careStats();
  const tasks = weekTasks().length;
  const nextP = MY_PLANTS.slice().sort(function(a,b){ return wDue(a) - wDue(b); })[0];
  const line = nextP
    ? (isEdible(nextP) && hPct(nextP) < 100
        ? 'Your ' + lc(nextP.s.name) + ' is ' + (nextP.s.days - nextP.day) + ' days out.'
        : cap(lc(nextP.s.name)) + ' needs water ' + inDays(wDue(nextP)) + '.')
    : 'Add a plant and next week fills itself in.';
  box.innerHTML = '<div class="glow"></div>'
    + '<div class="xbtn" role="button" tabindex="0" aria-label="Close" style="align-self:flex-end" data-go="home">' + ICONS._x2 + '</div>'
    + '<div class="recap-in">'
    + '<div class="recap-ph" style="background-image:url(img/hero-plants.jpg)"></div>'
    + '<span class="pill b-lime" style="align-self:flex-start;margin-top:20px">Week complete</span>'
    + '<div class="done-h">Everything<br><span style="color:var(--lime)">on time.</span></div>'
    + '<div class="recap-s">' + line + ' Pro maps every week ahead so you never wonder what’s next.</div>'
    + '<div class="sg2"><div class="stat"><b style="color:var(--lime)">' + st.waterings
    + '</b><s>waterings logged</s></div>'
    + '<div class="stat"><b>' + tasks + '/' + tasks + '</b><s>tasks this week</s></div></div></div>'
    + '<div class="btn b-lime" data-go="paywall">See the whole calendar</div>'
    + '<div class="btn" style="background:#1B3527;color:#fff" data-go="home">Not now</div>';
}
const seasonWeeks = () => Math.round(zipInfo().season / 7);
/* План — предложение. Раньше он строился, показывался и молча выбрасывался:
   после save→paywall на Home лежал демо-набор, а не то, что человек видел. */
function applyPlan(){
  const plan = buildPlan();
  const room = limit();
  const take = plan.slice(0, room), held = plan.slice(room);
  MY_PLANTS = take.map(function(sp){ return mkPlant(sp.id, 0, 0, []); });
  ONB_MODE = null;
  renderAll();
  const names = held.map(function(x){ return lc(x.name); });
  const list2 = names.length > 1
    ? names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1] : names[0];
  toast(held.length
    ? '<span>Added ' + take.length + '. Pro also keeps ' + list2 + '</span>'
    : '<span>Added ' + take.length + (take.length === 1 ? ' plant' : ' plants') + '</span>', 4500);
  go('save');
}
function renderSave(){
  const el = document.getElementById('savepill'); if(!el) return;
  const plan = MY_PLANTS.length ? MY_PLANTS : buildPlan();
  el.textContent = plan.length + (plan.length === 1 ? ' PLANT' : ' PLANTS') + ' · '
    + (CHOICES.outdoor ? seasonWeeks() + ' WEEKS' : 'YEAR-ROUND');
}

/* ─────────── онбординг: варианты рендерятся из трека ─────────── */
const SPACES = {
  house: [['Living room','The usual spot — bright but not direct','q2i'],
          ['Bedroom','Low light, steady temperature','q2i'],
          ['Kitchen','Warm, humid, good for most things','q2i'],
          ['Bathroom','High humidity, often low light','q2i'],
          ['Home office','Desk-side, artificial light too','q2i'],
          ['Windowsill','The brightest shelf you have','q2i']],
  edible: [['Patio',null,'q2'], ['Deck',null,'q2'], ['Porch',null,'q2'],
           ['Backyard',null,'q2'], ['Raised bed',null,'q2'],
           ['Apartment balcony',null,'q2'],
           ['Windowsill / indoors','Herbs and greens, year-round','q2i']],
  both: [['Living room','Plants inside, herbs on the sill','q2i'],
         ['Kitchen','Warm and humid — herbs do well','q2i'],
         ['Windowsill','The brightest shelf you have','q2i'],
         ['Patio','Pots outside, plants inside','q2'],
         ['Balcony','Containers out, greenery in','q2'],
         ['Backyard','Beds outside, plants inside','q2']]
};
const GOALS = {
  house: [['Hard to kill','hardy'], ['Low light room','lowlight'], ['A big statement plant','statement'],
          ['Flowers','flowers'], ['Trailing and hanging','trailing'], ['Cleaner air','air'],
          ['Kid-friendly project','kids']],
  edible: [['Salads and greens','salads'], ['Fresh herbs','herbs'], ['Fast first harvest','fast'],
           ['Tomatoes','tomatoes'], ['Peppers','peppers'], ['Beans and peas','beans'],
           ['Roots: radish, carrot','roots'], ['Kid-friendly project','kids']],
  both: [['Hard to kill','hardy'], ['Fresh herbs','herbs'], ['Salads and greens','salads'],
         ['A big statement plant','statement'], ['Fast first harvest','fast'],
         ['Flowers','flowers'], ['Cleaner air','air'], ['Kid-friendly project','kids']]
};
const Q4TITLE = {house:'What are you after?', edible:'What do you want to eat?',
                 both:'What are you after?'};
function optHTML(label, sub, next, multi){
  const s = sub ? '<s>' + sub + '</s>' : '';
  const attr = multi ? ' data-multi' : ' data-single data-next="' + next + '"';
  return '<div class="opt"' + attr + '><div>' + label + s + '</div>'
    + '<div class="opt-tick">' + ICONS._checkw + '</div></div>';
}
function renderQ1(){
  const box = document.getElementById('q1opts'); if(!box) return;
  box.innerHTML = (SPACES[CHOICES.track] || SPACES.both).map(function(o){
    return optHTML(o[0], o[1], o[2], false); }).join('');
  const h = document.getElementById('q1head');
  if(h) h.textContent = CHOICES.track === 'edible' ? 'Where will you grow?' : 'Where will it live?';
}
function renderQ4(){
  const box = document.getElementById('q4opts'); if(!box) return;
  box.innerHTML = (GOALS[CHOICES.track] || GOALS.both).map(function(o){
    return optHTML(o[0], null, null, true); }).join('');
  const h = document.getElementById('q4head');
  if(h) h.textContent = Q4TITLE[CHOICES.track] || Q4TITLE.both;
}
function renderQ5(){
  const box = document.getElementById('q5opts'); if(!box) return;
  const many = CHOICES.track === 'edible' ? 'a real garden' : 'a real collection';
  box.innerHTML =
      optHTML('About 10 minutes', 'Keep it very simple · 3 plants', 'preview', false)
    + optHTML('About 20 minutes', 'I can do a bit more · 4 plants', 'preview', false)
    + optHTML('30+ minutes', 'I want ' + many + ' · up to 6 plants', 'preview', false);
}

function renderAll(){
  renderHome(); renderDetail();
  try{ renderDash(); renderPlantCards(); }catch(e){}
  try{ renderLock(); renderSettings(); }catch(e){}
}

const SUNLABEL = {
 '3–5 hours':'3–5 hours of sun', '6–8 hours':'6–8 hours of sun',
 '8+ hours':'8+ hours of sun', 'Not sure yet':'a safe 3–5 hours until you check',
 'South':'a south-facing window', 'East or West':'an east or west window',
 'North':'a north window', 'Not sure':'a cautious low-light start'};
const GOALWORD = {salads:'salads', herbs:'herbs', fast:'a fast first harvest',
 tomatoes:'tomatoes', peppers:'peppers', beans:'beans', roots:'root crops', kids:'a kid project',
 hardy:'something hard to kill', lowlight:'plants for a dim room', statement:'a statement plant',
 flowers:'flowers', trailing:'trailing greenery', air:'cleaner air', petsafe:'pet-safe plants',
 useful:'a plant that earns its keep'};
const SUNNEED = {tomatoes:'6–8 hours', peppers:'6–8 hours', beans:'6–8 hours'};
const SUNRANK = {'3–5 hours':1,'6–8 hours':2,'8+ hours':3,'Not sure yet':1,
                 'South':2,'East or West':1,'North':1,'Not sure':1};
const TRACKOF = {'Houseplants':'house', 'Something to eat':'edible', 'Both':'both'};
function goalTag(label){
  const all = GOALS.house.concat(GOALS.edible, GOALS.both);
  const hit = all.find(function(o){ return o[0] === label; });
  return hit ? hit[1] : null;
}
function isOutdoorSpace(label){
  return ['Patio','Deck','Porch','Backyard','Raised bed','Apartment balcony','Balcony']
    .indexOf(label) > -1;
}
/* Трек ветки «уже есть» не спрашивается — он виден по тому, что занесли. */
function trackFromPlants(){
  const h = MY_PLANTS.some(function(p){ return p.s.kind === 'house'; });
  const e = MY_PLANTS.some(isEdible);
  return h && e ? 'both' : e ? 'edible' : h ? 'house' : CHOICES.track;
}
/* Куда ведёт ответ. Ветка «уже есть» заканчивается на Home, а не на плане. */
function onbNext(scr, staticNext){
  if(ONB_MODE === 'own' && (scr === 's-q3' || scr === 's-q2i')){
    CHOICES.track = trackFromPlants();
    ONB_MODE = null;
    return 'home';
  }
  return staticNext;
}
function recordChoice(scr, label){
  if(scr === 's-q0'){
    ONB_MODE = label.indexOf('already have') > -1 ? 'own' : 'plan';
    /* онбординг начинается с чистого листа: демо-набор не должен
       притворяться растениями, которые человек занёс сам */
    MY_PLANTS = []; PENDING = []; SELECTED = 0; DONE = {}; SCAN_KEEP = null;
    renderAll();
  }
  if(scr === 's-qwhat'){
    CHOICES.track = TRACKOF[label] || 'edible';
    CHOICES.goals = [];
    renderQ1(); renderQ4(); renderQ5();
  }
  if(scr === 's-q1'){
    CHOICES.outdoor = isOutdoorSpace(label);
    CHOICES.space = label.indexOf('Windowsill') > -1 ? 'windowsill' : label.toLowerCase();
  }
  if(scr === 's-q3' || scr === 's-q2i'){
    CHOICES.sun = SUNLABEL[label] || 'your light';
    CHOICES.sunRank = SUNRANK[label] || 1;
  }
  if(scr === 's-q5'){ CHOICES.effort = label.indexOf('10') > -1 ? 3
                                     : label.indexOf('20') > -1 ? 4 : 6; }
}
'''

ICON_JS = {n: ic(n, 'var(--primary)', 15, '1.9') for n in ICONSET}
ICON_JS['_plus'] = ic('plus', 'var(--primary)', 17, '2.4')
ICON_JS['_check'] = ic('check', '#fff', 17, '3')
ICON_JS['_check2'] = ic('check', '#fff', 16, '3')
ICON_JS['_drop'] = ic('drop', '#fff', 15)
ICON_JS['_dropbig'] = ic('drop', 'var(--lime)', 30)
ICON_JS['_dropp'] = ic('drop', 'var(--bright)', 28)
ICON_JS['_leaf'] = ic('leaf', 'var(--lime)', 20)
ICON_JS['_chevd'] = ic('chevron-right', 'var(--muted)', 18, '2.4')
ICON_JS['_circ'] = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#B4BEB8" '
                    'stroke-width="2"><circle cx="12" cy="12" r="9"/></svg>')
ICON_JS['_checkp'] = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="var(--primary)" '
                      'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                      '<circle cx="12" cy="12" r="9"/><path d="M8 12.4 10.8 15.2 16 9.6"/></svg>')
ICON_JS['_chev'] = ic('chevron-right', '#B4BEB8', 20, '2.2')
ICON_JS['_plusd'] = ic('plus', 'var(--deepest)', 16, '2.4')
ICON_JS['_checkg'] = ic('check', 'var(--bright)', 17, '3')
ICON_JS['_x'] = ic('x', '#6E7A73', 17, '2.4')
ICON_JS['_cam'] = ic('camera', 'var(--primary)', 22, '2')
ICON_JS['_cam2'] = ic('camera', 'var(--primary)', 26, '1.9')
ICON_JS['_checkw'] = ic('check', '#fff', 14, '3')
ICON_JS['_x2'] = ic('x', '#CFE0D4', 20, '2')
# крупные глифы для плитки-заглушки, когда настоящей фотографии вида нет
for _n in sorted({x['icon'] for x in PLANTS}):
    ICON_JS['_big_' + _n] = ic(_n, 'rgba(180,244,97,.42)', 64)


# ═════════════════════════════ ДОКУМЕНТ ФЛОУ
FLOWS = [
 ("1 · Первый заход", "Развилка на входе: приложение — трекер ухода, а не только планировщик посадки.", [
  ("Landing", "Фото фермера на весь экран, один заголовок, одна кнопка.",
   "Ничего не считает. Ждёт тапа.",
   "Q0", "Обещание про растения в целом, но ведёт съедобным: это основной трек."),
  ("Q0 · Старт", "«Уже есть растения» или «Хочу начать выращивать».",
   "Пишет ONB_MODE и ОБНУЛЯЕТ MY_PLANTS: онбординг начинается с чистого листа, "
   "демо-набор больше не притворяется твоими растениями.",
   "Add a plant или Q1 · Track",
   "Развилки не было. Онбординг строил план посадки, а весь интерфейс после него "
   "построен под уход. Человеку с готовой монстерой пять вопросов про то, что сажать, "
   "были бесполезны."),
  ("Ветка «уже есть» · библиотека", "Тот же экран Add a plant, но без таб-бара, "
   "с заголовком «What do you have?» и кнопкой «Skip for now».",
   "Показывает ВСЕ 29 видов: трек ещё не известен. Кнопка активна и на пустом выборе — "
   "пустой выбор не тупик.",
   "Q1 · Space", "Трек не спрашивается: он выводится из того, что человек занёс. "
   "Только комнатные → house, только съедобные → edible, и то и то → both."),
  ("Q1 · Track", "Три варианта: съедобное, комнатные, оба. Только для ветки «хочу начать».",
   "Пишет track. От него зависят варианты в Q1, Q4 и состав библиотеки.",
   "Q1 · Space", "Раньше это был первый вопрос для всех."),
  ("Q1 · Space", "Варианты из трека: комнаты для комнатных, площадки для съедобных.",
   "Пишет space и флаг outdoor. Уличное место — единственная причина спрашивать ZIP.",
   "Q2 если outdoor, иначе Q2-indoor", "Windowsill остаётся внутри."),
  ("Q2 · ZIP", "Пустое поле, Continue выключен. Только на уличном треке.",
   "Резолвит ZIP в climate_profile: зона, дата последних заморозков, длина сезона. "
   "Четыре города с типичными справочными значениями.",
   "Q3", "Раньше карточка климата всегда говорила Austin независимо от ZIP."),
  ("Q3 · Sun / Q2-indoor · Light", "Часы солнца снаружи, сторона окна внутри.",
   "Пишет sunRank — главный фильтр качества плана.",
   "Q4, а в ветке «уже есть» сразу Home",
   "Ветка «уже есть» здесь заканчивается: свет и место — всё, что нужно для ухода."),
  ("Q4 · Goals", "Мультивыбор, максимум три. Варианты из трека.",
   "Пишет plan.goals.", "Q5", "При лимите остальные гаснут, а не исчезают."),
  ("Q5 · Effort", "Три уровня: 3 / 4 / 5-6 растений.",
   "Пишет effort — размер плана.", "Plan Preview", "Вопросов об опыте нет."),
  ("Plan Preview", "План с фотографиями видов, дата первого сбора, блок «почему». "
   "Две кнопки: «Add the first N plants» и «I&rsquo;ll pick my own».",
   "Мини-движок: фильтр по треку и месту → фильтр по свету → скоринг по целям → "
   "гарантии состава. Кнопка ПРИМЕНЯЕТ план, соблюдая бесплатный лимит, и говорит, "
   "что именно осталось за платой.",
   "Save Plan", "Раньше план строился, показывался и молча выбрасывался: после "
   "save→paywall на Home лежал демо-набор, а не то, что человек только что видел."),
  ("Save Plan", "Фото на весь экран, Google или email. Пилюля считается из того, "
   "что реально добавлено.",
   "Создаёт User, привязывает план. Пароля нет — magic link.",
   "Paywall", "Регистрация после показанной ценности."),
  ("Paywall", "Тёмный экран, Year pass предвыбран, триал без карты.",
   "Ничего не блокирует. После покупки ведёт в календарь — туда, что обещала кнопка.",
   "Week-lock", "⚠ Показ сразу после регистрации — решение заказчика, против §10.4."),
 ]),
 ("2 · Недельный цикл", "То, ради чего продукт существует. 80% времени пользователя.", [
  ("Home · пусто", "Фото-герой на весь блок: «Every room feels better with something alive in it». "
   "Две дороги — скан камерой и библиотека.",
   "MY_PLANTS пуст. Экран знает это и меняется целиком.",
   "Scan или Add a plant", "Пустой экран не должен быть пустым: он продаёт ближайшее будущее."),
  ("Add a plant", "Поиск по 29 видам: 8 комнатных и 21 съедобная культура. Один справочник.",
   "Показывает подмножество под трек и место. Комнатные группируются по требовательности, "
   "съедобные — по скорости отдачи. Тем, чему не хватает света, отдельный блок внизу.",
   "Home", "Добавил одно — появится одно. Неподходящее показано и погашено, а не спрятано. "
           "Раньше этот экран не открывался вообще: он читал поле съедобной модели у "
           "комнатного растения и падал."),
  ("Home · есть растения", "Health score с фото, два виджета, горизонтальный список растений, "
   "ниже — раскрывающийся чеклист недели.",
   "Score считается по просрочке полива. Задачи собираются из MY_PLANTS: полив по просрочке, "
   "сбор для созревших, протирка листьев для крупных, поворот для светолюбивых, подкормка раз в месяц.",
   "Plant detail · Week complete", "Задачи текущей недели всегда бесплатны — это ядро обещания. "
   "Список задач раньше был захардкожен под четыре конкретных растения и врал, "
   "как только состав менялся."),
  ("Отметка задачи", "Один тап, без подтверждения. Прогресс-бар двигается.",
   "Отметка живёт по названию задачи, а не по индексу: список пересобирается при каждом "
   "изменении состава, и индексы бы разъехались.",
   "Week complete, если отмечены все", "Просроченная задача не красная и без жёсткого дедлайна."),
  ("Week complete", "Тёмный экран с фото, счётчик поливов, предложение Pro.",
   "success_modal. Частота — не чаще раза в 7 дней. Строка «что дальше» берётся из растений.",
   "Paywall или Home", "Оффер привязан к моменту успеха, а не к блокировке."),
  ("Week · пусто", "«Nothing needed this week» плюс список растений с их сроками.",
   "Считает ближайшую задачу и называет её словами: «watering the pothos tomorrow».",
   "Plant detail", "§18. Пустая неделя — подтверждение, что всё идёт по плану, а не сломанный экран."),
  ("Week · возврат", "«Most of it doesn\u2019t matter now» и две задачи, которые ещё имеют смысл.",
   "Задачи берутся из настоящих растений, а не из текста.",
   "Home", "§6.4 Продукт никогда не показывает список из двадцати просроченных задач."),
  ("Week · долгий пропуск", "Предложение пересобрать план. Нижняя строка называет растения, "
   "которые реально пересохли.",
   "Пересчёт предлагается, но не делается автоматически. Выполненное и журнал сохраняются.",
   "Home", "§19.1 №7."),
 ]),
 ("3 · Растения", "Управление составом и карточка вида.", [
  ("Plant detail", "Фото, латинское имя, статус, два виджета, журнал, удаление.",
   "Второй виджет зависит от вида: комнатному — свет и влажность, съедобному — процент "
   "до сбора и типичный диапазон дней.",
   "Milestone, если созрело", "Если у вида нет настоящей фотографии, стоит плитка с иконкой. "
   "Выдумывать ассет нельзя, а битая картинка — артефакт."),
  ("Удаление", "Кнопка внизу карточки, снизу всплывает Undo на 4.5 секунды.",
   "Растение удаляется из состояния, но хранится в буфере отмены вместе с позицией. "
   "SELECTED подтягивается, чтобы не указывать в пустоту.",
   "Home", "Провал не должен быть страшным. §23.1 запрещает обвинять пользователя."),
  ("Scan a plant", "Камера, рамка, ответ с процентом совпадения.",
   "Реальный PlantNet через воркер-прокси, ключ в клиент не попадает. Латинское имя "
   "маппится на 29 видов справочника, включая комнатные.",
   "Home", "Воркер не развёрнут → экран честно пишет «Recognition is off» и не угадывает. "
           "Добавление после скана раньше создавало объект чужой формы и ломало весь рендер."),
 ]),
 ("4 · История ухода", "Пик удержания и главный источник органики.", [
  ("Growth · дашборд", "Health score крупной цифрой, календарь ухода, полоса здоровья, "
   "карточки растений со своими снимками.",
   "Календарь отмечает дни поливов и дни со снимками. Карточки делятся на «нужно внимание» и "
   "«всё хорошо» по сроку полива.",
   "Plant detail", "Раньше здесь были две сущности про одно и то же — список и отдельная "
                   "сетка фото, хотя каждое фото и так принадлежит растению."),
  ("Milestone", "Тёмный экран с настоящим фото из журнала.",
   "Для съедобных это «First harvest. Day 31», для комнатных — «It is thriving» с числом "
   "дней и поливов. Один экран, две формулировки.",
   "Growth", "Единственный момент, когда человек получает физическое доказательство."),
  ("Recap", "Итог: сборы и дни на улице, поливы и растения внутри.",
   "На уличном треке триггер today ≥ first_frost. Для комнатных сезон не кончается никогда, "
   "поэтому итог считается в поливах и снимках.",
   "Paywall", "Экран пришёл из съедобной эпохи и считал «14 harvests, 187 days» "
              "независимо от того, что у человека росло."),
  ("Shopping list", "Горшки по размеру каждого вида, поддоны, грунт, лейка, удобрение.",
   "Собирается из плана, сумма считается. Строка семян появляется только если в плане "
   "есть съедобное.",
   "Paywall", "Free — список на экране, Pro — печатный PDF. Ценность видна до покупки."),
 ]),
 ("5 · Подоконник", "Съедобный трек внутри дома. Ветка, которая закрывает сезонность.", [
  ("Windowsill · Home", "«Season ends: never». Ритм — срез каждую неделю.",
   "Нет first_frost и horizon_weeks. Вместо дней до урожая — счётчик срезов и время до следующего.",
   "тот же цикл", "Все четыре вида есть в справочнике с флагом sill. Экран показательный, "
                  "содержимое статичное."),
 ]),
 ("6 · Точки оффера", "Видно часто, давления нет.", [
  ("Баннер над навигацией", "Лаймовая полоса «Unlock the full care plan», не перекрывает "
   "контент, не требует закрытия.",
   "persistent_line. Видна всегда, кроме Pro.",
   "Paywall", "Около 90% всех показов оффера приходится на неперекрывающие форматы."),
  ("Soft-lock двух недель", "Задачи размыты, но количество и время видны.",
   "Показывает, что за платой стоит реальный контент, а не пустота.",
   "Paywall", "Это не стена. §10.3. Обещание — «весь календарь ухода», а не «30 недель сезона»."),
  ("Лимит растений", "Четвёртое растение упирается в блок «That\u2019s the free limit».",
   "Не отказ: выбор остаётся в корзине, блок объясняет, что даёт Pro.",
   "Paywall", "Мы не блокируем то, что человек уже начал."),
  ("Anti-annoyance", "Если модалку показывать нельзя, оффер деградирует в inline, а не исчезает.",
   "max 1 модалка в 7 дней, 2 закрытия подряд → только inline, 5 → только баннер и Settings.",
   "—", "Если session-drop после показа > 10%, частота падает до 1 раза в 14 дней автоматически."),
 ]),
]

# ═════════════════════════════ СБОРКА
GROUPS = ['Онбординг', 'Home', 'Plants', 'Growth', 'Деньги', 'Система', 'Windowsill']
FLOW = """
<b>Основной путь.</b> <code>landing</code> → <code>q0</code> (что растим) → четыре-пять вопросов →
<code>preview</code> (план виден без регистрации) → <code>save</code> → <code>paywall</code> →
<code>home</code> → добавил растение → чекает задачи → <code>week-done</code><br>
<b>Развилка трека.</b> <code>q0</code> делит продукт: комнатные, съедобные или и то и другое. От трека
зависят варианты в <code>q1</code> и <code>q4</code>, состав библиотеки и то, спрашиваем ли ZIP.<br>
<b>Развилка места.</b> Уличное место в <code>q1</code> → <code>q2</code> (ZIP) → <code>q3</code> (часы солнца).
Комната или подоконник → <code>q2i</code> (сторона окна), ZIP не спрашиваем вообще.<br>
<b>Ветка момента.</b> <code>plant</code> → созрело → <code>harvest</code> (milestone) → <code>growth</code>;
конец года → <code>season-end</code> (recap).<br>
<b>Ветки оффера.</b> <code>week-lock</code> (soft-lock двух недель), <code>add-plant</code> (лимит трёх растений),
<code>week-done</code> — все ведут в <code>paywall</code>, и все закрываются туда, откуда пришли.
"""
TOKENS = [('--ground', '#F2F4F0', 'Ground'), ('--surface', '#FFFFFF', 'Surface'),
          ('--ink', '#0B1F14', 'Ink · 17.2:1'), ('--muted', '#5C6660', 'Muted · 6.0:1'),
          ('--primary', '#0E7A3C', 'Primary · белый 5.43:1'), ('--bright', '#22A559', 'Bright · графика'),
          ('--lime', '#B4F461', 'Lime · на тёмном 13.2:1'), ('--deep', '#0F3A24', 'Deep · белый 12.7:1'),
          ('--deepest', '#0B1F14', 'Deepest · экраны'), ('--flame', '#FF7043', 'Flame · на тёмном 6.3:1')]

screens_html = ''.join(f'<div class="screen" id="s-{s["id"]}">{s["html"]}</div>' for s in SCR)
notes = {s['id']: (s['title'], s['note']) for s in SCR}

idx = ('<div class="grp"><div class="gt">Состояние данных</div><div class="chips">'
       '<button class="chip" data-demo="empty">Сбросить — новый юзер</button>'
       '<button class="chip" data-demo="seed">4 овоща</button>'
       '<button class="chip" data-demo="house">4 комнатных</button>'
       '<button class="chip" data-demo="mixed">Смешанный — 2 + 2</button></div></div>')
for g in GROUPS:
    items = [s for s in SCR if s['group'] == g]
    if not items: continue
    idx += f'<div class="grp"><div class="gt">{g}</div><div class="chips">' + ''.join(
        f'<button class="chip" data-go="{s["id"]}">{s["title"]}</button>' for s in items) + '</div></div>'

toks = '<div class="tok">' + ''.join(
    f'<div class="tk"><i style="background:{hx}"></i><b>{hx}</b><s>{lbl}</s></div>'
    for v, hx, lbl in TOKENS) + '</div>'

import json
JS_EXTRA = (JS_SRC.replace('__ICONS__', json.dumps(ICON_JS, ensure_ascii=False))
                  .replace('__SPECIES__', json.dumps(PLANTS, ensure_ascii=False)))
HTML = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>HOMEGROWN — прототип</title>
<style>{CSS}</style></head><body>
<div class="stage">
  <div class="stage-bar"><span class="t" id="scr-title">Landing</span><span class="s" id="scr-id">landing</span></div>
  <main class="phone">{screens_html}<div id="toast" role="status" aria-live="polite"></div><input id="cam" type="file" accept="image/*" capture="environment" aria-label="Take a photo" tabindex="-1" hidden></main>
  <div class="hint" id="scr-note"></div>
</div>
<div class="side">
  <div style="font-size:var(--t-11);font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)">
    HOMEGROWN · кликабельный прототип · {len(SCR)} экранов</div>
  <h1 class="cap-f" style="margin-top:8px">Потыкай прототип</h1>
  <div class="lede">Кликай прямо в телефоне: кнопки, опции, растения, таб-бар. Задачи отмечаются по тапу и
    двигают прогресс-бар. Ниже — переход на любой экран и карта флоу.</div>
  {idx}
  <div class="grp"><div class="gt">Флоу</div><div class="flow">{FLOW}</div></div>
  <div class="grp"><div class="gt">Токены — все проверены на WCAG AA</div>{toks}
    <div class="flow" style="line-height:1.6"><b>Что изменилось против прошлой версии.</b>
      Нюдовая палитра убрана целиком. Ink #0B1F14 даёт 17.2:1 вместо прежних 9. Кнопки на #0E7A3C —
      5.43:1 с белым текстом, то есть AA проходит без оговорок. Лайм #B4F461 работает только на тёмном,
      где даёт 13.2:1. Тёплый акцент заменён на flame #FF7043 и живёт лишь на тёмных экранах.
      Акцентный блок — градиент, а не плоскость: это единственное отступление от Hers, и оно осознанное,
      потому что именно оно даёт «живость» из твоих референсов.</div></div>
</div>
<script>
{JS_EXTRA}
const NOTES = {json.dumps(notes, ensure_ascii=False)};
let PW_FROM = 'home';
const ONB = ['q0','qwhat','q1','q2','q3','q2i','q4','q5'];
const STEPS = {{plan_out:['q0','qwhat','q1','q2','q3','q4','q5'],
               plan_in:['q0','qwhat','q1','q2i','q4','q5'],
               own_out:['q0','add-plant','q1','q2','q3'],
               own_in:['q0','add-plant','q1','q2i']}};
function renderPg(id){{
  const key = (ONB_MODE === 'own' ? 'own_' : 'plan_') + (CHOICES.outdoor ? 'out' : 'in');
  const path = STEPS[key];
  const k = path.indexOf(id); if(k < 0) return;
  document.querySelectorAll('#s-'+id+' [data-pg]').forEach(function(el){{
    el.innerHTML = path.map(function(_, i){{
      return '<i class="'+(i <= k ? 'on' : '')+'"></i>'; }}).join('');
  }});
}}
function go(id){{
  const el = document.getElementById('s-'+id); if(!el) return;
  if(id==='paywall'){{ const cur=document.querySelector('.screen.on');
    PW_FROM = (cur && cur.id==="s-save") ? "home" : (cur? cur.id.slice(2):'home');
    if(PW_FROM==='paywall') PW_FROM='home'; }}
  document.querySelectorAll('.screen.on').forEach(s=>s.classList.remove('on'));
  resetScreen(id);
  if(id==='q1') renderQ1();
  if(id==='q4') renderQ4();
  if(id==='q5') renderQ5();
  if(ONB.indexOf(id)>-1) renderPg(id);
  if(id==='preview') try{{ renderPreview(); }}catch(e){{}}
  if(id==='save') renderSave();
  if(id==='add-plant'){{ const q=document.getElementById('spq'); if(q){{q.value='';
      q.parentElement.classList.remove('has');}} PENDING=[]; renderLibrary('');
    /* в онбординге экран ведёт себя иначе: назад к развилке, без таб-бара */
    el.classList.toggle('onb', ONB_MODE === 'own');
    const bk = el.querySelector('.back');
    if(bk) bk.dataset.go = ONB_MODE === 'own' ? 'q0' : 'home';
    const h = el.querySelector('.h1');
    if(h) h.textContent = ONB_MODE === 'own' ? 'What do you have?' : 'Add a plant';
  }}
  if(id==='home') renderHome();
  if(id==='week-empty') renderWeekEmpty();
  if(id==='week-back'||id==='week-long') renderBack();
  if(id==='week-done') renderWeekDone();
  if(id==='plant') renderDetail();
  if(id==='growth'){{ renderDash(); renderPlantCards(); }}
  if(id==='harvest') renderMilestone();
  if(id==='season-end') renderRecap();
  if(id==='shopping') renderShopping();
  if(id==='week-lock') renderLock();
  if(id==='settings') renderSettings();
  if(id==='pick') renderPick();
  if(id==='calendar') renderCalendar();
  stampRoles(el);
  el.classList.add('on');
  /* Сдвиг лаймового баннера считается от РЕАЛЬНОЙ высоты подвала и таб-бара.
     Раньше он был захардкожен тремя правилами, и стоило подвалу вырасти на
     строку, как баннер ложился на кнопку. Мерить можно только после .on. */
  const ft = el.querySelector('.foot'), nv = el.querySelector('.nav');
  const nh = nv ? nv.offsetHeight : 0;
  /* Подвал плавает над контентом, поэтому его надо посадить ровно над таб-баром:
     иначе кнопка накрывает навигацию. offsetHeight уже включает safe-area. */
  if(ft) ft.style.bottom = nh + 'px';
  const fh = ft ? ft.offsetHeight : 0;
  /* место под плавающие кнопку и баннер освобождает нижний отступ прокрутки */
  el.style.setProperty('--ofr-bottom', (fh + nh + 12) + 'px');
  el.style.setProperty('--foot-h', (fh + nh + 16) + 'px');
  el.querySelectorAll('.bd').forEach(b=>b.scrollTop=0);
  el.querySelectorAll('.dark,.overlay').forEach(b=>b.scrollTop=0);
  document.querySelectorAll('.chip').forEach(c=>c.classList.toggle('act', c.dataset.go===id));
  const n = NOTES[id]||['',''];
  document.getElementById('scr-title').textContent = n[0];
  document.getElementById('scr-id').textContent = id;
  document.getElementById('scr-note').innerHTML = n[1];
  history.replaceState(null,'','#'+id);
}}
const MAXG = 3;
function resetScreen(id){{
  const el = document.getElementById('s-'+id); if(!el) return;
  el.querySelectorAll('.opt').forEach(function(o){{
    o.classList.remove('sel','dim'); o.setAttribute('aria-checked','false'); }});
  el.querySelectorAll('.pl').forEach(o=>o.classList.remove('locked'));
  el.querySelectorAll('[data-cta]').forEach(b=>b.classList.add('off'));
  const z = el.querySelector('[data-zip]');
  if(z){{ z.textContent='— — — — —'; z.classList.add('ph');
          el.querySelector('[data-zipres]').style.display='none'; }}
  const c = el.querySelector('[data-count]'); if(c) c.textContent='nothing selected yet';
  const h = el.querySelector('[data-hint]'); if(h) h.textContent='Pick at least one.';
  const ac = el.querySelector('[data-addcount]'); if(ac) ac.textContent='nothing selected';
  const lm = el.querySelector('[data-limit]'); if(lm) lm.style.display='none';
}}
function syncMulti(wrap){{
  const scr = wrap.closest('.screen');
  const n = wrap.querySelectorAll('.opt.sel').length;
  wrap.querySelectorAll('.opt').forEach(o=>o.classList.toggle('dim', n>=MAXG && !o.classList.contains('sel')));
  const c = scr.querySelector('[data-count]');
  if(c) c.textContent = n===0 ? 'nothing selected yet' : n+' selected';
  const h = scr.querySelector('[data-hint]');
  if(h) h.innerHTML = n===0 ? 'Pick at least one.'
      : (n>=MAXG ? 'That&rsquo;s three. Tap one again to swap it out.' : 'You can pick '+(MAXG-n)+' more.');
  const b = scr.querySelector('[data-cta]'); if(b) b.classList.toggle('off', n===0);
}}
const optLabel = o => o.querySelector('div').childNodes[0].textContent.trim();
document.addEventListener('click', e=>{{
  const single = e.target.closest('[data-single]');
  if(single){{
    single.parentElement.querySelectorAll('.opt').forEach(function(o){{
      o.classList.remove('sel'); o.setAttribute('aria-checked','false'); }});
    single.classList.add('sel'); single.setAttribute('aria-checked','true');
    try{{ recordChoice(single.closest('.screen').id, optLabel(single)); }}catch(err){{}}
    let nx = onbNext(single.closest('.screen').id, single.dataset.next);
    if(nx && nx!=='None') setTimeout(()=>go(nx), 300);
    return;
  }}
  const multi = e.target.closest('[data-multi]');
  if(multi){{
    const wrap = multi.parentElement;
    if(multi.classList.contains('sel')) multi.classList.remove('sel');
    else if(wrap.querySelectorAll('.opt.sel').length < MAXG) multi.classList.add('sel');
    multi.setAttribute('aria-checked', multi.classList.contains('sel') ? 'true' : 'false');
    syncMulti(wrap);
    CHOICES.goals = Array.from(wrap.querySelectorAll('.opt.sel'))
      .map(o=>goalTag(optLabel(o))).filter(Boolean);
    return;
  }}
  const zip = e.target.closest('[data-zip]');
  if(zip){{
    zip.textContent = CHOICES.zip || '78704';
    zip.classList.remove('ph'); CHOICES.zip = CHOICES.zip || '78704';
    const zi = zipInfo();
    const scr = zip.closest('.screen');
    scr.querySelector('#zipcity').textContent = zi.city;
    scr.querySelector('#zipfrost').textContent = zi.frost;
    scr.querySelector('#zipseason').textContent = zi.season + ' days';
    scr.querySelector('[data-zipres]').style.display='block';
    scr.querySelector('[data-cta]').classList.remove('off'); return;
  }}
  const t = e.target.closest('[data-task]');
  if(t){{ const on = t.classList.toggle('done');
          t.setAttribute('aria-checked', on ? 'true' : 'false'); return; }}
  const seg = e.target.closest('[data-seg]');
  if(seg){{ seg.parentElement.querySelectorAll('[data-seg]').forEach(function(d){{
             d.classList.remove('on'); d.setAttribute('aria-checked','false'); }});
           seg.classList.add('on'); seg.setAttribute('aria-checked','true');
           price(seg); return; }}
  if(e.target.closest('[data-scan]')){{ openCamera(null, 'scan'); return; }}
  if(e.target.closest('[data-scanpick]')){{ SCAN_KEEP = SCAN_URL; SCAN_URL = null;
    go('add-plant'); return; }}
  const sa = e.target.closest('[data-scanadd]');
  if(sa){{ const id = sa.dataset.scanadd;
    const k = MY_PLANTS.findIndex(function(p){{ return p.s.id === id; }});
    if(k > -1){{ SELECTED = k; SCAN_URL = null; renderAll(); go('plant');
      toast('<span>You already keep a ' + lc(MY_PLANTS[k].s.name) + ' \u2014 here it is</span>');
      return; }}
    if(!IS_PRO && MY_PLANTS.length >= FREE_LIMIT){{ SCAN_URL = null; go('paywall'); return; }}
    MY_PLANTS.push(mkPlant(id, 0, 0, SCAN_URL ? [{{u: SCAN_URL, day: 0}}] : []));
    SCAN_URL = null; SELECTED = MY_PLANTS.length-1; renderAll(); go('home'); return; }}
  if(e.target.closest('[data-progtoggle]')){{ WEEK_OPEN = !WEEK_OPEN; renderWeek(); return; }}
  const br = e.target.closest('[data-brtoggle]');
  if(br){{ const t2 = WEEK[+br.dataset.brtoggle]; if(!t2) return;
           const k = tkey(t2); DONE[k] = !DONE[k]; renderWeek(); checkWeekDone(); return; }}
  const wa = e.target.closest('[data-water]');
  if(wa){{ const p = MY_PLANTS[+wa.dataset.water]; if(p){{ p.since = 0; renderAll();
    const t3=document.getElementById('toast');
    t3.innerHTML='<span>'+p.s.name+' watered</span><b data-gogrowth>See journal</b>';
    t3.classList.add('on'); clearTimeout(UNDOT);
    UNDOT=setTimeout(function(){{t3.classList.remove('on')}},3000); }}
    return; }}
  if(e.target.closest('[data-addphoto]')){{ openCamera(); return; }}
  const sh = e.target.closest('[data-shoot]');
  if(sh){{ openCamera(+sh.dataset.shoot); return; }}
  if(e.target.closest('[data-gogrowth]')){{ document.getElementById('toast').classList.remove('on');
                                            go('growth'); return; }}
  if(e.target.closest('[data-buy]')){{ buyPro(); return; }}
  if(e.target.closest('[data-unpro]')){{ dropPro(); return; }}
  const sw = e.target.closest('[data-sw]');
  if(sw){{ toggleSetting(sw.dataset.sw); return; }}
  const st2 = e.target.closest('[data-set]');
  if(st2){{ PICK_KEY = st2.dataset.set; go('pick'); return; }}
  const pv = e.target.closest('[data-pickval]');
  if(pv){{ applyPick(pv.dataset.pickval); return; }}
  if(e.target.closest('[data-export]')){{ exportPlants(); return; }}
  if(e.target.closest('[data-del-acct]')){{
    toast('<span>Type DELETE to confirm — not wired up in the prototype</span>', 4000); return; }}
  const row = e.target.closest('.tglrow');
  if(row){{ const t4 = row.querySelector('.tgl');
            const on = t4.classList.toggle('on');
            row.setAttribute('aria-checked', on ? 'true' : 'false'); return; }}
  if(e.target.closest('[data-undo]')){{ undoRemove(); return; }}
  if(e.target.closest('[data-remove]')){{ removePlant(SELECTED); go('home'); return; }}
  const op = e.target.closest('[data-open]');
  if(op){{ SELECTED = +op.dataset.open; renderDetail(); go('plant'); return; }}
  const ad = e.target.closest('[data-add]');
  if(ad){{ const n = ad.dataset.sp; const k = PENDING.indexOf(n);
    if(k>-1) PENDING.splice(k,1);
    else if(MY_PLANTS.length+PENDING.length < limit()) PENDING.push(n);
    else {{ const lim=document.querySelector('#s-add-plant [data-limit]');
            if(lim) lim.style.display='block'; return; }}
    const q=document.getElementById('spq'); renderLibrary(q?q.value:''); return; }}
  const cta = e.target.closest('#s-add-plant [data-cta]');
  if(cta && !cta.classList.contains('off')){{
    if(ONB_MODE === 'own'){{
      PENDING.forEach(function(n, i){{
        const ph = (i === 0 && SCAN_KEEP) ? [{{u: SCAN_KEEP, day: TODAY}}] : [];
        MY_PLANTS.push(mkPlant(n, 0, 0, ph));
      }});
      SCAN_KEEP = null; PENDING = [];
      CHOICES.track = trackFromPlants();
      renderAll(); go('q1'); return;
    }}
    PENDING.forEach(function(n, i){{
      /* снимок со скана прикрепляем к первому добавленному виду */
      const ph = (i === 0 && SCAN_KEEP) ? [{{u: SCAN_KEEP, day: TODAY}}] : [];
      MY_PLANTS.push(mkPlant(n, 0, 0, ph));
    }});
    if(SCAN_KEEP){{ toast('<span>Your photo is in the journal</span>'); SCAN_KEEP = null; }}
    PENDING=[]; renderAll(); go('home'); return; }}
  if(e.target.closest('[data-planadd]')){{ applyPlan(); return; }}
  if(e.target.closest('[data-planskip]')){{
    MY_PLANTS = []; ONB_MODE = null; renderAll(); go('save'); return; }}
  if(e.target.closest('[data-pw-exit]')){{ go(PW_FROM); return; }}
  const g = e.target.closest('[data-go]');
  if(g){{ go(g.dataset.go); }}
}});
function price(seg){{
  const card = seg.closest('.dark').querySelector('.pcard');
  if(!card) return;
  const yearly = seg.textContent.indexOf('Year')>-1;
  card.querySelector('.pr').innerHTML = yearly
    ? '$29<span style="font-size:var(--t-15);font-weight:500;color:#A9BCB0"> / year</span>'
    : '$4.99<span style="font-size:var(--t-15);font-weight:500;color:#A9BCB0"> / month</span>';
  card.querySelector('.pn').textContent = yearly
    ? 'Cheaper than one dead fiddle leaf fig. Covers every plant, all year.'
    : 'Month to month. A year runs about seven of these.';
  card.querySelector('.pill').style.display = yearly ? '' : 'none';
}}
document.addEventListener('input', e=>{{
  if(e.target.id==='spq'){{ e.target.parentElement.classList.toggle('has', !!e.target.value);
                            renderLibrary(e.target.value); }}
}});
document.addEventListener('click', e=>{{
  if(e.target.closest('#spx')){{ const q=document.getElementById('spq');
    q.value=''; q.parentElement.classList.remove('has'); renderLibrary(''); q.focus(); }}
}});
document.addEventListener('click', e=>{{
  const d = e.target.closest('[data-demo]');
  if(d){{ if(d.dataset.demo==='empty') MY_PLANTS=[];
          else if(d.dataset.demo==='mixed'){{ seedMixed(); CHOICES.track='both'; }}
          else if(d.dataset.demo==='house'){{ seedHouseDemo(); CHOICES.track='house';
            CHOICES.outdoor=false; CHOICES.space='living room';
            CHOICES.sun='an east or west window'; CHOICES.sunRank=1; }}
          else {{ seedPlants(); CHOICES.track='edible'; CHOICES.outdoor=true;
            CHOICES.space='patio'; CHOICES.sun='6–8 hours of sun'; CHOICES.sunRank=2; }}
          PENDING=[]; SELECTED=0; DONE={{}}; renderAll(); go('home'); }}
}});
(function(){{ const c=document.getElementById('cam');
  if(c) c.addEventListener('change', function(){{ attachShot(c.files && c.files[0]); }});
}})();
seedPlants(); renderAll();
const KEYROLES = ['button','link','checkbox','radio','switch'];
document.addEventListener('keydown', e=>{{
  if(e.key!==' ' && e.key!=='Enter') return;
  const t = e.target;
  if(!t || !t.getAttribute) return;
  if(KEYROLES.indexOf(t.getAttribute('role')) < 0) return;
  if(t.getAttribute('aria-disabled') === 'true') return;
  e.preventDefault(); t.click();
}});
go(location.hash.slice(1) || 'landing');
</script></body></html>'''

DIR = pathlib.Path(__file__).parent

# ── 1. review.html — рамка + индекс (для десктопного ревью)
(DIR / 'review.html').write_text(HTML, encoding='utf-8')

INSTALL_HTML = r'''
<div id="a2hs">
  <div class="a2-card">
    <div class="a2-txt">
      <span class="a2-pill">No address bar</span>
      <b class="a2-h">Put it on your<br>home screen</b>
      <s id="a2hint">Share &rarr; Add to Home Screen</s>
    </div>
    <div class="a2-act">
      <button id="a2btn" hidden>Install</button>
      <div id="a2x">&times;</div>
    </div>
  </div>
</div>
<script>
(function(){
  var standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  var bar = document.getElementById('a2hs');
  function showBar(){ bar.classList.add('on'); document.body.classList.add('a2-open'); }
  function hideBar(){ bar.classList.remove('on'); document.body.classList.remove('a2-open'); }
  if(!standalone && !localStorage.getItem('a2hs-off')) setTimeout(showBar, 1400);
  document.getElementById('a2x').onclick = function(){ hideBar(); localStorage.setItem('a2hs-off','1'); };
  var deferred = null;
  window.addEventListener('beforeinstallprompt', function(e){
    e.preventDefault(); deferred = e;
    document.getElementById('a2hint').textContent = 'One tap and it lives on your home screen';
    var b = document.getElementById('a2btn'); b.hidden = false;
    b.onclick = function(){ deferred.prompt(); deferred = null; hideBar(); };
  });
  window.addEventListener('appinstalled', function(){ hideBar(); localStorage.setItem('a2hs-off','1'); });
  if('serviceWorker' in navigator) window.addEventListener('load', function(){
    navigator.serviceWorker.register('sw.js').catch(function(){});
  });
})();
</script>
'''

# ── 2. index.html — мобильный веб, без рамки и без сайдбара
MOBILE_CSS = """
#a2hs{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:60;
  opacity:0;transform:translateY(16px);pointer-events:none;
  transition:opacity .26s ease-out,transform .26s cubic-bezier(.32,.72,0,1)}
#a2hs.on{opacity:1;transform:none;pointer-events:auto}
.a2-card{background:var(--lime);border-radius:var(--r-xl);padding:16px;display:flex;align-items:flex-end;
  gap:12px;box-shadow:0 16px 36px rgba(11,31,20,.34)}
.a2-txt{flex:1;min-width:0}
.a2-pill{display:inline-block;background:var(--deepest);color:var(--lime);border-radius:999px;
  padding:6px 12px;font-size:var(--t-11);font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.a2-h{display:block;font-size:var(--t-24);font-weight:700;line-height:1.06;letter-spacing:-.02em;
  color:var(--deepest);margin-top:8px}
#a2hs s{display:block;font-size:var(--t-12);color:#2C4A1E;text-decoration:none;margin-top:6px;
  font-weight:600;opacity:.78}
.a2-act{display:flex;align-items:center;gap:8px;flex:none}
#a2btn{background:var(--deepest);color:var(--lime);border:0;border-radius:999px;height:44px;padding:0 20px;
  font:700 var(--t-15) 'Inter Tight',sans-serif;cursor:pointer}
#a2x{width:44px;height:44px;border-radius:50%;background:rgba(11,31,20,.12);display:flex;align-items:center;
  justify-content:center;font-size:var(--t-20);color:var(--deepest);flex:none;cursor:pointer;line-height:1}
body.a2-open .bd{padding-bottom:172px}


html,body{height:100%}
body{display:block;padding:0;background:var(--ground);overflow:hidden}
.stage{display:contents}
.side,.stage-bar,.hint{display:none!important}
.mob{position:fixed;inset:0;display:flex;flex-direction:column;background:var(--ground)}
.mob .screen{position:absolute;inset:0}
.sb{display:none}
.hd{padding-top:calc(8px + env(safe-area-inset-top))}
.overlay .wm,.dark>*:first-child{margin-top:env(safe-area-inset-top)}
.overlay,.dark{padding-top:calc(24px + env(safe-area-inset-top))}
.shot,.scrim{top:0!important}
.nav{padding-bottom:env(safe-area-inset-bottom);height:calc(56px + env(safe-area-inset-bottom))}
#toast{top:calc(8px + env(safe-area-inset-top));bottom:auto}
@media (min-width:768px){
  body{background:#DDE2DA;display:flex;align-items:center;justify-content:center;height:100vh;overflow:hidden}
  .mob{position:relative;inset:auto;width:375px;height:812px;flex:none;border-radius:40px;overflow:hidden;
       box-shadow:0 24px 64px rgba(11,31,20,.28)}
  .hd{padding-top:16px}
  .overlay,.dark{padding-top:24px}
  #a2hs{display:none}
}
"""
PWA_HEAD = (
 '<title>HOMEGROWN</title>\n'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
 '<link rel="manifest" href="manifest.webmanifest">\n'
 '<meta name="theme-color" content="#F2F4F0">\n'
 '<meta name="mobile-web-app-capable" content="yes">\n'
 '<meta name="apple-mobile-web-app-capable" content="yes">\n'
 '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
 '<meta name="apple-mobile-web-app-title" content="HOMEGROWN">\n'
 '<link rel="apple-touch-icon" href="img/apple-touch-icon.png">\n'
 '<link rel="icon" href="img/icon-192.png">\n'
 '<script src="scan-config.js"></script>\n'
 '<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/Caprasimo-400-latin.woff2">\n'
 '<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/InterTight-400-latin.woff2">')

MOBILE = HTML
assert '<title>HOMEGROWN — прототип</title>' in MOBILE
MOBILE = MOBILE.replace('<title>HOMEGROWN — прототип</title>', PWA_HEAD)
MOBILE = MOBILE.replace('</style>', MOBILE_CSS + '</style>')
MOBILE = MOBILE.replace('<main class="phone">', '<main class="mob">')
i = MOBILE.index('<div class="side">'); j = MOBILE.index('<script>')
MOBILE = MOBILE[:i] + MOBILE[j:]
MOBILE = MOBILE.replace('</body>', INSTALL_HTML + '</body>')
(DIR / 'index.html').write_text(MOBILE, encoding='utf-8')


# ── service worker генерится вместе со сборкой: имя кэша = хэш index.html,
#    поэтому каждый деплой гарантированно инвалидирует старый кэш
import hashlib
BUILD = hashlib.sha1(MOBILE.encode()).hexdigest()[:10]
SW_SRC = """const CACHE = 'homegrown-%s';
const ASSETS = [
  './', './index.html', './manifest.webmanifest', './scan-config.js',
  './img/hero.jpg', './img/hero-farm.jpg', './img/hero-garden.jpg', './img/garden.jpg',
  './img/radish.jpg', './img/basil.jpg', './img/lettuce.jpg', './img/cherrytomato.jpg',
  './img/flowers.jpg', './img/containers.jpg',
  './img/leaves1.jpg', './img/leaves2.jpg', './img/leaves3.jpg',
  './img/icon-192.png', './img/icon-512.png', './img/apple-touch-icon.png',
  './fonts/Caprasimo-400-latin.woff2', './fonts/Caprasimo-400-latin-ext.woff2',
  './fonts/InterTight-400-latin.woff2', './fonts/InterTight-400-latin-ext.woff2'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const isDoc = req.mode === 'navigate' || req.destination === 'document';
  if (isDoc) {
    // HTML — только из сети, кэш лишь как офлайн-запасной. Иначе обновления
    // никогда не доходят до вернувшегося посетителя.
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put('./index.html', copy)).catch(() => {});
        return res;
      }).catch(() => caches.match('./index.html'))
    );
    return;
  }
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
      return res;
    }))
  );
});
""" % BUILD
(DIR / 'sw.js').write_text(SW_SRC, encoding='utf-8')
print('sw.js: cache', BUILD, '| стратегия network-first для HTML')

# ── 3. flow.html — документ пользовательского флоу
def frows(steps):
    out = []
    for scr, sees, does, nxt, note in steps:
        out.append(
          f'<tr><td class="c1"><b>{scr}</b></td><td>{sees}</td><td>{does}</td>'
          f'<td class="c4">{nxt}</td></tr>'
          f'<tr class="nt"><td></td><td colspan="3">{note}</td></tr>')
    return ''.join(out)

flow_body = ''
for title, lede, steps in FLOWS:
    flow_body += (f'<section><h2>{title}</h2><p class="lede">{lede}</p>'
                  '<table><thead><tr><th class="c1">Экран</th><th>Что видит пользователь</th>'
                  '<th>Что делает система</th><th class="c4">Куда ведёт</th></tr></thead><tbody>'
                  + frows(steps) + '</tbody></table></section>')

FLOW_HTML = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>HOMEGROWN — пользовательский флоу</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{T}
{FACES}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--ground);font-family:'Inter Tight',system-ui,sans-serif;color:var(--ink);
     padding:48px 40px 88px;max-width:1180px;margin:0 auto;line-height:1.5}}
.top{{font-size:var(--t-11);font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)}}
h1{{font-family:Caprasimo;font-size:var(--t-40);line-height:1.04;margin:8px 0 12px;font-weight:400}}
.intro{{font-size:var(--t-16);color:var(--ink-2);max-width:760px;line-height:1.6}}
section{{margin-top:44px}}
h2{{font-size:var(--t-20);font-weight:600;letter-spacing:-.01em}}
.lede{{font-size:var(--t-14);color:var(--muted);margin:4px 0 16px}}
table{{width:100%;border-collapse:collapse;background:var(--surface);border-radius:var(--r-lg);overflow:hidden}}
th{{text-align:left;font-size:var(--t-11);font-weight:600;letter-spacing:.1em;text-transform:uppercase;
   color:var(--muted);padding:16px 16px;background:#EAEEE8}}
td{{padding:16px 16px;font-size:var(--t-14);vertical-align:top;border-top:1px solid var(--hair)}}
.c1{{width:152px}}.c4{{width:180px;color:var(--primary);font-weight:600}}
tr.nt td{{border-top:0;padding-top:0;font-size:var(--t-13);color:var(--ink-2);background:#FAFBF9}}
tr.nt td:last-child:before{{content:"↳ ";color:var(--muted)}}
.legend{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
.lg{{background:var(--surface);border-radius:var(--r-lg);padding:12px 16px;font-size:var(--t-13);flex:1;min-width:240px}}
.lg b{{display:block;font-size:var(--t-12);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}
</style></head><body>
<div class="top">HOMEGROWN · пользовательский флоу · {len(SCR)} экранов</div>
<h1>Что будет и как будет</h1>
<div class="intro">Продукт — про растения в целом: комнатные и съедобные это виды одного домена,
а не два разных приложения. Каждый шаг разложен на четыре вещи: что человек видит, что в этот момент
делает система, куда его ведёт дальше и что важно не сломать. Стрелкой отмечены пометки — правила из
продуктовой спеки и места, где я от неё отступил.</div>
<div class="legend">
  <div class="lg"><b>Развилка трека</b>Q0 делит продукт на комнатные, съедобные и оба. От него зависят вопросы, библиотека и нужен ли ZIP.</div>
  <div class="lg"><b>Развилка места</b>ZIP и заморозки спрашиваем только на улице. Внутри сезон не кончается никогда.</div>
  <div class="lg"><b>Единственный запрет</b>Ничего не блокируем из того, что человек уже начал делать.</div>
  <div class="lg"><b>Отступление от спеки</b>Пэйволл сразу после регистрации — против §10.4. Помечено ⚠ в таблице.</div>
</div>
{flow_body}
</body></html>"""
(DIR / 'flow.html').write_text(FLOW_HTML, encoding='utf-8')

print('index.html (mobile):', len(MOBILE), '| review.html:', len(HTML), '| flow.html:', len(FLOW_HTML),
      '| screens:', len(SCR))
