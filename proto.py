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
    return (f'<svg class="rg" width="{sz}" height="{sz}" viewBox="0 0 {sz} {sz}">'
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
    return (f'<svg viewBox="0 0 24 24" width="{sz}" height="{sz}" fill="none" stroke="{c}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{STROKE_GLYPHS[n]}"/></svg>')

def ic(n, c='currentColor', sz=22, sw=None):
    if n in STROKE_GLYPHS:
        return stroke_ic(n, c, sz, float(sw) if sw else 2.4)
    """Solid-иконка Phosphor. sw сохранён в сигнатуре — вызовы его передают, заливке он не нужен."""
    return (f'<svg viewBox="0 0 256 256" width="{sz}" height="{sz}" fill="{c}">{inner(n)}</svg>')

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
  --r-lg:28px; --r-md:20px; --r-sm:14px;
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
.stage-bar .t{font-size:15px;font-weight:600}
.stage-bar .s{font-size:13px;color:#5C6660}
.hint{font-size:12.5px;color:#5C6660;margin-top:12px;max-width:390px;line-height:1.45}
.hint b{color:var(--ink)}

/* ───── правая колонка: индекс + флоу */
.side{flex:1;min-width:0;padding-bottom:60px}
.side h1{font-size:40px;line-height:1.05}
.side .lede{font-size:15px;color:var(--ink-2);line-height:1.55;max-width:760px;margin-top:8px}
.grp{margin-top:24px}
.grp .gt{font-size:11.5px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:var(--surface);border:0;border-radius:999px;padding:8px 16px;font:500 13.5px/1 'Inter Tight',sans-serif;
      color:var(--ink);cursor:pointer;box-shadow:0 1px 2px rgba(11,31,20,.06)}
.chip:hover{background:var(--lime)}
.chip.act{background:var(--primary);color:#fff}
.tok{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.tk{background:var(--surface);border-radius:var(--r-sm);padding:8px 12px;width:168px}
.tk i{display:block;height:32px;border-radius:8px;margin-bottom:8px}
.tk b{font-size:12.5px;display:block}
.tk s{font-size:11.5px;color:var(--muted);text-decoration:none;display:block;margin-top:2px}
.flow{background:var(--surface);border-radius:var(--r-md);padding:16px;margin-top:12px;font-size:13.5px;line-height:2;color:var(--ink-2)}
.flow b{color:var(--ink);font-weight:600}
.flow code{font:500 12.5px ui-monospace,monospace;background:var(--ground);padding:2px 8px;border-radius:8px;color:var(--primary)}

/* ───── app chrome */
.sb{height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 24px;flex:none;
    font-size:13px;font-weight:600}
.hd{padding:4px 16px 8px;display:flex;justify-content:center;align-items:center;flex:none;min-height:52px;background:var(--ground);position:relative;z-index:5}
.hd-l,.hd-r{position:absolute;top:0;bottom:8px;display:flex;align-items:center;width:44px}
.hd-l{left:12px;justify-content:flex-start}
.hd-r{right:12px;justify-content:flex-end}
.back{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;flex:none}
.back svg{transform:rotate(180deg)}
.back:active{background:#E6EBE4}
.wm{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:19px;letter-spacing:.01em;color:var(--primary);line-height:1}
.av{width:32px;height:32px;border-radius:50%;background:var(--lime);display:flex;align-items:center;
    justify-content:center;font-size:12.5px;font-weight:700;color:var(--deepest);cursor:pointer}
.bd{flex:1;overflow-y:auto;overflow-x:hidden;padding:8px 20px 8px;scrollbar-width:none;min-height:0}
.foot{flex:none;padding:8px 20px 24px;background:var(--ground);box-shadow:0 -14px 22px -14px rgba(11,31,20,.14)}
.foot .btn{margin-top:0}
.bd::-webkit-scrollbar{display:none}
.greet{font-size:14px;color:var(--muted);margin-top:16px}
.h1{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:30px;line-height:1.06;letter-spacing:0;margin-top:8px}
.h1 .m{color:#9EA8A2}
.sl{font-size:12.5px;font-weight:600;letter-spacing:-.02em;color:var(--muted);margin:20px 0 8px}

/* ───── ACCENT BLOCK (референс 1) */
.acc{border-radius:var(--r-lg);padding:20px;margin-top:16px;color:#fff;position:relative;overflow:hidden;
     background:linear-gradient(150deg,#17683C 0%,#0F3A24 52%,#0B1F14 100%)}
.acc:after{content:"";position:absolute;width:232px;height:232px;right:-88px;top:-112px;border-radius:50%;
     background:radial-gradient(circle,rgba(180,244,97,.30),rgba(180,244,97,0) 70%)}
.acc .row1{display:flex;justify-content:space-between;align-items:center;position:relative}
.addtop{display:flex;align-items:center;gap:4px;height:36px;padding:0 16px;border-radius:999px;
        background:#fff;color:var(--deepest);font-size:14px;font-weight:700;cursor:pointer;flex:none;
        position:relative;box-shadow:0 2px 8px rgba(11,31,20,.30)}
.addtop svg{fill:var(--deepest)}
.addtop:after{content:"";position:absolute;inset:-4px}
.addtop:active{background:#EAF5EE}
.acc .tag{background:var(--lime);color:var(--deepest);font-size:11px;font-weight:700;letter-spacing:.06em;
     padding:4px 12px;border-radius:999px}
.acc .lbl{font-size:13px;color:#B7C7BD;margin-top:16px;letter-spacing:-.02em}
.acc .big{font-size:34px;font-weight:600;letter-spacing:-.02em;line-height:1.05;margin-top:4px}
.acc .sub{font-size:13.5px;color:#B7C7BD;margin-top:8px;line-height:1.45}
.acc .duo{display:flex;gap:8px;margin-top:16px}
.acc .cell{flex:1;background:#17492F;border-radius:var(--r-sm);padding:12px 12px}
.acc .cell s{display:block;font-size:11.5px;color:#A9BCB0;text-decoration:none;white-space:nowrap}
.acc .cell b{display:block;font-size:18px;font-weight:600;margin-top:4px;white-space:nowrap}
.acc .plants{margin-top:16px;position:relative}
.accwhy{margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,.14);position:relative;
        font-size:14px;line-height:1.5;color:#C2D3C8}
.accwhy b{color:#fff;font-weight:600}
.accwhy .warn{display:block;margin-top:8px;color:var(--lime)}
.acc .prow{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.10)}
.acc .prow:last-child{border-bottom:0}
.acc .prow .nm{flex:1}
.acc .prow .nm b{display:block;font-size:15px;font-weight:600}
.acc .prow .nm s{display:block;font-size:12px;color:#A9BCB0;text-decoration:none;margin-top:1px}
.acc .prow .rt{font-size:12.5px;color:var(--lime);font-weight:600}
.rw{width:40px;height:40px;flex:none;position:relative;display:flex;align-items:center;justify-content:center}
.rw i{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.acc-photo{height:152px;border-radius:20px;background-size:cover;background-position:center;
           margin:-4px 0 16px;position:relative}

/* ───── карточки, задачи */
.card{background:var(--surface);border-radius:var(--r-md);padding:16px}
.task{background:var(--surface);border-radius:var(--r-md);padding:16px;margin-bottom:8px;display:flex;gap:12px;cursor:pointer;align-items:center}
.task:active{transform:scale(.985)}
.box{width:24px;height:24px;border-radius:8px;box-shadow:inset 0 0 0 2px #C9D2CC;flex:none;margin-top:1px;
     display:flex;align-items:center;justify-content:center;transition:background .16s,box-shadow .16s}
.box svg{opacity:0;transform:scale(.6);transition:opacity .16s,transform .16s}
.task.done .box{background:var(--bright);box-shadow:none}
.task.done .box svg{opacity:1;transform:scale(1)}
.tt{flex:1}.tt .t{font-size:16px;font-weight:600;line-height:1.3}
.tt .b{font-size:14px;color:var(--ink-2);line-height:1.42;margin-top:4px}
.min{font-size:13px;color:var(--muted);flex:none;margin-top:2px;font-weight:500}
.task.done .t{color:#9EA8A2;text-decoration:line-through;text-decoration-color:#C9D2CC}
.wk{background:var(--surface);border-radius:28px;margin-top:16px;overflow:hidden;
     box-shadow:0 1px 3px rgba(11,31,20,.07)}
.wk-h{display:flex;align-items:center;gap:10px;height:56px;padding:0 16px 0 12px;cursor:pointer}
.pb-ic{display:flex;flex:none}
.pb-n{font-size:15px;font-weight:700;letter-spacing:-.02em;flex:none}
.pb-track{flex:1;height:8px;border-radius:999px;background:#E4E8E2;overflow:hidden;min-width:0}
.pb-track i{display:block;height:100%;background:var(--bright);border-radius:999px;transition:width .3s}
.pb-pct{font-size:15px;font-weight:700;color:var(--muted);flex:none;letter-spacing:-.02em}
.pb-chev{display:flex;flex:none;transition:transform .2s}
.wk.open .pb-chev{transform:rotate(90deg)}
.wk-list{padding:4px 16px 8px;border-top:1px solid var(--hair)}
.branch{position:relative;margin-left:12px;padding-left:20px}
.branch:before{content:"";position:absolute;left:0;top:20px;bottom:24px;width:2px;
     border-radius:2px;background:#E4E8E2}
.br-row{display:flex;align-items:center;gap:12px;padding:12px 0;cursor:pointer;position:relative}
.br-row:before{content:"";position:absolute;left:-20px;top:50%;width:14px;height:2px;
     border-radius:2px;background:#E4E8E2}
.br-dot{width:24px;height:24px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 2px #C9D2CC;
     display:flex;align-items:center;justify-content:center;background:var(--surface)}
.br-dot.on{background:var(--primary);box-shadow:none}
.br-t{flex:1;font-size:15.5px;font-weight:600;letter-spacing:-.02em;line-height:1.25;min-width:0}
.br-t s{display:block;font-size:13.5px;font-weight:400;color:var(--ink-2);text-decoration:none;
     margin-top:3px;line-height:1.35}
.br-t.done{color:#9EA8A2;text-decoration:line-through;text-decoration-color:#C9D2CC}
.br-m{font-size:13px;color:var(--muted);flex:none;font-weight:500;align-self:flex-start;margin-top:4px}
.prog{display:flex;align-items:center;gap:12px;margin:16px 2px 0}
.bar{flex:1;height:8px;border-radius:999px;background:#DDE3DC;overflow:hidden}
.bar i{display:block;height:100%;background:var(--bright);border-radius:999px;transition:width .35s}
.pct{font-size:13px;color:var(--muted);font-weight:500}
.blur{height:12px;border-radius:999px;background:#E1E6E0}

/* ───── кнопки */
.btn{display:flex;align-items:center;justify-content:center;height:52px;border-radius:999px;
     font-size:17px;font-weight:600;margin-top:12px;cursor:pointer}
.b-pri{background:var(--primary);color:#fff}
.b-lime{background:var(--lime);color:var(--deepest)}
.b-white{background:#fff;color:var(--deepest)}
.b-ghost{background:#E6EBE4;color:var(--ink)}
.b-dark{background:var(--deepest);color:#fff}
.pill{display:inline-flex;align-items:center;height:32px;padding:0 16px;border-radius:999px;
      font-size:12.5px;font-weight:700;letter-spacing:.04em}

/* ───── навигация */
.nav{height:56px;background:var(--surface);display:flex;padding:6px 4px 0;flex:none;border-top:1px solid var(--hair)}
.ni{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;cursor:pointer;position:relative;color:#8E9A93;padding-top:2px}
.ni span{font-size:10px;font-weight:600;letter-spacing:.01em}
.ni.on{color:var(--primary)}
.ni.on span{font-weight:700}
.bdg{position:absolute;top:-4px;left:calc(50% + 8px);width:8px;height:8px;border-radius:50%;background:var(--flame)}
.ofr{position:absolute;left:0;right:0;bottom:calc(56px + env(safe-area-inset-bottom));
     padding:0 12px;cursor:pointer;z-index:20}
.ofr:last-child{bottom:calc(12px + env(safe-area-inset-bottom))}
.screen:has(.ofr) .bd{padding-bottom:84px}
.screen:has(.foot) .ofr{bottom:calc(88px + env(safe-area-inset-bottom))}
.screen:has(.foot):has(.nav) .ofr{bottom:calc(144px + env(safe-area-inset-bottom))}
body.is-pro .ofr{display:none}
body.is-pro .ofr{display:none}
.ofr-in{display:flex;align-items:center;gap:12px;border-radius:999px;height:52px;padding:0 8px 0 8px;
        background:var(--lime);position:relative;overflow:hidden;
        box-shadow:0 6px 18px rgba(120,190,40,.34)}
.ofr-ic{width:36px;height:36px;border-radius:50%;background:var(--deepest);display:flex;align-items:center;
        justify-content:center;flex:none;position:relative}
.ofr-tx{flex:1;position:relative}
.ofr-tx b{font-size:15px;font-weight:700;color:var(--deepest);letter-spacing:-.01em}
.ofr-tx s{font-size:15px;color:#2C4A1E;text-decoration:none;font-weight:600;opacity:.72;margin-left:8px}
.ofr-go{width:36px;height:36px;border-radius:50%;background:var(--deepest);display:flex;align-items:center;
        justify-content:center;flex:none;position:relative}
.pro{background:var(--deepest);color:var(--lime)}

/* ───── онбординг */
.pg{display:flex;gap:8px;margin-top:16px}
.pg i{height:4px;flex:1;border-radius:999px;background:#DDE3DC}
.pg i.on{background:var(--primary)}
.opt{background:var(--surface);border-radius:var(--r-md);padding:16px 16px;margin-bottom:8px;font-size:16px;min-height:56px;
     font-weight:600;display:flex;justify-content:space-between;align-items:center;cursor:pointer;
     border:2px solid transparent}
.opt s{display:block;font-size:13px;color:var(--muted);font-weight:400;text-decoration:none;margin-top:4px}
.opt.sel{border-color:var(--primary);background:#EAF5EE}
.opt.sel s{color:var(--ink-2)}
.opt.dim{color:#A6B0AA;pointer-events:none}.opt.dim s{color:#B8C1BB}
.opt-tick{width:24px;height:24px;border-radius:50%;background:var(--primary);display:flex;
          align-items:center;justify-content:center;flex:none;margin-left:12px;
          opacity:0;transform:scale(.65);transition:opacity .14s,transform .14s}
.opt.sel .opt-tick{opacity:1;transform:scale(1)}
.btn.off{background:#DDE3DC;color:#9EA8A2;pointer-events:none;box-shadow:none}
.zip.ph{color:#B4BEB8;letter-spacing:.22em}
.tgl{width:48px;height:28px;border-radius:999px;background:#D3DAD4;flex:none;position:relative;
     cursor:pointer;transition:background .18s}
.tgl i{position:absolute;left:4px;top:4px;width:20px;height:20px;border-radius:50%;background:#fff;
       transition:left .18s;box-shadow:0 1px 3px rgba(11,31,20,.22)}
.tgl.on{background:var(--bright)}
.tgl.on i{left:24px}
.zipres{display:none}
.search{display:flex;align-items:center;gap:8px;background:var(--surface);border-radius:16px;
        padding:0 16px;height:52px;margin-top:16px}
.search input{flex:1;border:0;outline:0;background:transparent;font:500 15.5px 'Inter Tight',sans-serif;
        color:var(--ink);min-width:0}
.search input::placeholder{color:#9EA8A2;font-weight:400}
.search .sx{display:none;cursor:pointer}
.search.has .sx{display:block}
.gsec{font-size:12.5px;font-weight:600;letter-spacing:-.02em;color:var(--muted);margin:20px 0 8px}
.empty{text-align:center;color:var(--muted);font-size:14.5px;padding:24px 8px;line-height:1.5}
.del{width:44px;height:44px;border-radius:50%;background:#F0F2EF;display:flex;align-items:center;
     justify-content:center;flex:none;cursor:pointer;margin-left:8px}
.del:active{background:#E2E6E0}
.addbtn{width:32px;height:32px;border-radius:50%;background:#EDF1EB;display:flex;align-items:center;
        justify-content:center;flex:none}
.pl.added .addbtn{background:var(--bright)}
.pl.added .addbtn svg:first-child,.pl.added .addbtn svg:last-child{display:none}
.pl.added .addbtn svg:last-child{display:block}
.pl.have{opacity:.55}
.wgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
.wg{border-radius:20px;padding:16px;min-width:0}
.wg.span2{grid-column:1 / -1}
.wg-lite{background:var(--surface)}
.wg-dark{background:var(--deepest);color:#fff}
.wg-top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px}
.wg .num{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:36px;line-height:1;letter-spacing:-.02em}
.wg .num span{font-size:18px;margin-left:2px}
.wg .lbl{font-size:13px;color:var(--muted);margin-top:8px;letter-spacing:-.02em}
.wg-dark .lbl{color:#A9BCB0}
.wg-h{display:flex;align-items:baseline;justify-content:space-between;gap:8px}
.wg-h b{font-size:15px;font-weight:600;letter-spacing:-.02em}
.wg-h s{font-size:12.5px;color:var(--muted);text-decoration:none}
.wg-dark .wg-h s{color:#A9BCB0}
.mrow{display:flex;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid var(--hair)}
.wg-dark .mrow{border-top-color:rgba(255,255,255,.14)}
.mrow>div{flex:1;min-width:0}
.mrow s{display:block;font-size:11.5px;color:var(--muted);text-decoration:none;letter-spacing:-.02em}
.wg-dark .mrow s{color:#A9BCB0}
.mrow b{display:block;font-size:15px;font-weight:600;margin-top:2px;letter-spacing:-.02em}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-top:12px}
.cal i{aspect-ratio:1;border-radius:50%;display:flex;align-items:center;justify-content:center;
       font-size:12px;font-weight:600;font-style:normal;color:#8DA396;background:rgba(255,255,255,.06)}
.cal i.fut{color:#4C6155;background:rgba(255,255,255,.03)}
.cal i.m-sow{background:transparent;box-shadow:inset 0 0 0 2px var(--lime);color:var(--lime)}
.cal i.m-photo{background:#2E5C3A;color:#fff}
.cal i.m-pick{background:var(--lime);color:var(--deepest)}
.callg{display:flex;gap:14px;margin-top:12px;font-size:11.5px;color:#A9BCB0}
.callg span{display:flex;align-items:center;gap:5px}
.callg i{width:10px;height:10px;border-radius:50%;font-style:normal;flex:none}
.callg i.m-sow{box-shadow:inset 0 0 0 2px var(--lime)}
.callg i.m-photo{background:#2E5C3A}
.callg i.m-pick{background:var(--lime)}
.ccard{background:var(--surface);border-radius:var(--r-md);padding:12px;margin-bottom:8px}
.chead{display:flex;align-items:center;gap:12px;cursor:pointer;padding:4px}
.chead .nm b{display:block;font-size:16px;font-weight:600;letter-spacing:-.02em}
.chead .nm s{display:block;font-size:13px;color:var(--muted);text-decoration:none;margin-top:2px}
.cstrip{display:flex;gap:4px;margin-top:8px}
.cstrip>div{flex:0 0 calc(25% - 3px);aspect-ratio:1;border-radius:12px;background-size:cover;background-position:center;background-color:#DDE3DC}
.cmore{display:flex;align-items:center;justify-content:center;background:#E8EDE6!important;
       color:var(--muted);font-size:14px;font-weight:700}
.cempty{display:flex;align-items:center;gap:8px;margin-top:8px;padding:12px;border-radius:12px;
        background:var(--ground);color:var(--muted);font-size:13px;font-weight:600;cursor:pointer}
.cempty svg{flex:none}
.jgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.jc{background:var(--surface);border-radius:16px;padding:8px;margin:0}
.jph{aspect-ratio:1;border-radius:12px;background-size:cover;background-position:center;background-color:#DDE3DC}
.jc figcaption{padding:8px 4px 4px}
.jc figcaption b{display:block;font-size:14px;font-weight:600;line-height:1.2}
.jc figcaption s{display:block;font-size:12px;color:var(--muted);text-decoration:none;margin-top:2px}
.btn-dash{height:48px;border-radius:999px;border:2px dashed var(--primary);color:var(--primary);
       display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px;
       font-size:15px;font-weight:700;cursor:pointer}
.btn-dash svg{fill:var(--primary)}
.btn-dash:active{background:#EAF5EE}
.herostub{height:152px;border-radius:var(--r-lg);background:var(--surface);margin-top:16px;
          display:flex;align-items:center;gap:16px;padding:0 20px;border:2px dashed #C2CCC5}
.herostub b{display:block;font-size:16px;font-weight:600}
.herostub s{display:block;font-size:13.5px;color:var(--muted);text-decoration:none;margin-top:4px;line-height:1.4}
#toast{position:absolute;left:16px;right:16px;bottom:160px;background:var(--deepest);color:#fff;
       border-radius:16px;padding:16px 16px;display:flex;justify-content:space-between;align-items:center;
       font-size:14.5px;opacity:0;transform:translateY(10px);pointer-events:none;transition:.22s;z-index:20}
#toast.on{opacity:1;transform:none;pointer-events:auto}
#toast b{color:var(--lime);font-weight:700;cursor:pointer}
.zip{background:var(--surface);border-radius:var(--r-md);padding:16px 16px;font-size:32px;font-weight:700;letter-spacing:.08em}

/* ───── full-bleed фото */
.shot{position:absolute;inset:0;background-size:cover;background-position:center}
.scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,31,20,.55) 0%,rgba(11,31,20,.05) 32%,rgba(11,31,20,.82) 72%,rgba(11,31,20,.96) 100%)}
.overlay{position:absolute;inset:0;display:flex;flex-direction:column;padding:24px 24px;color:#fff}

/* ───── тёмный экран (paywall / harvest) */
.dark{position:absolute;inset:0;background:var(--deepest);padding:24px 24px;display:flex;flex-direction:column;color:#fff;overflow-y:auto;scrollbar-width:none}
.dark::-webkit-scrollbar{display:none}
.glow{position:absolute;width:420px;height:420px;left:-60px;top:-152px;border-radius:50%;
      background:radial-gradient(circle,rgba(180,244,97,.34),rgba(180,244,97,0) 68%);pointer-events:none}
.glow.b{left:auto;right:-140px;top:280px;width:340px;height:340px;
      background:radial-gradient(circle,rgba(34,165,89,.34),rgba(34,165,89,0) 68%)}
.xbtn{width:44px;height:44px;border-radius:50%;background:#1B3527;display:flex;align-items:center;
      justify-content:center;cursor:pointer;flex:none}
.seg{display:flex;background:#152B1F;border-radius:999px;padding:4px;margin:16px auto 0;width:fit-content;position:relative}
.seg div{height:36px;display:flex;align-items:center;padding:0 28px;border-radius:999px;font-size:14.5px;font-weight:600;cursor:pointer;color:#9DB0A4}
.seg div.on{background:var(--lime);color:var(--deepest)}
.pcard{border-radius:24px;padding:20px;margin-top:16px;background:#122A1D;border:1.5px solid var(--lime);position:relative}
.pcard .pr{font-size:27px;font-weight:700}
.pcard .pn{font-size:13.5px;color:#A9BCB0;line-height:1.45;margin-top:8px}
.feat{margin-top:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,.12)}
.feat div{display:flex;align-items:flex-start;gap:8px;font-size:14.5px;margin-bottom:12px;color:#E4EEE6}
.feat i{width:8px;height:8px;border-radius:50%;background:var(--lime);flex:none;margin-top:8px}
.stat{background:#122A1D;border-radius:var(--r-md);padding:16px}
.stat b{font-size:36px;font-weight:600;display:block;line-height:1}
.stat s{font-size:12px;color:#A9BCB0;text-decoration:none;display:block;margin-top:8px;line-height:1.35}
.sg2{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:16px}

/* ───── прочее */
.plist{background:var(--surface);border-radius:var(--r-md);padding:4px 16px}
.pl{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--hair);cursor:pointer}
.pl:last-child{border-bottom:0}

.nm{flex:1}.nm b{display:block;font-size:15.5px;font-weight:600}
.nm s{display:block;font-size:13px;color:var(--muted);text-decoration:none;margin-top:1px}
.eta{font-size:13px;color:var(--muted);font-weight:500}
.addbtn{width:32px;height:32px;border-radius:50%;background:#E6EFE8;display:flex;align-items:center;
        justify-content:center;flex:none}
.addbtn svg:last-child{display:none}
.pl.added .addbtn{background:var(--bright)}
.pl.added .addbtn svg:first-child{display:none}
.pl.added .addbtn svg:last-child{display:block}
.pl.locked{opacity:.42;pointer-events:none}
.gal{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}
.gal div{aspect-ratio:1;border-radius:var(--r-sm);background-size:cover;background-position:center;background-color:#DDE3DC}
.strip{display:flex;gap:8px}
.strip div{width:72px;height:92px;border-radius:16px;background-size:cover;background-position:center;
           background-color:#DDE3DC;flex:none}
.note{background:var(--surface);border-radius:var(--r-md);padding:16px}
.note b{font-size:17px;font-weight:600;display:block;line-height:1.3}
.quote{background:var(--surface);border-radius:var(--r-md);padding:16px;margin-top:16px;position:relative}
.quote .qmark{font-family:Caprasimo,Georgia,serif;font-size:44px;line-height:.7;color:var(--bright);
              opacity:.32;height:24px}
.quote p{font-size:15px;line-height:1.45;color:var(--ink);margin-top:4px}
.qwho{display:flex;align-items:center;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid var(--hair)}
.qav{width:36px;height:36px;border-radius:50%;background:var(--deepest);color:var(--lime);flex:none;
     display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;letter-spacing:.04em}
.qwho b{display:block;font-size:14px;font-weight:600}
.qwho s{display:block;font-size:12.5px;color:var(--muted);text-decoration:none;margin-top:2px}
.note p{font-size:14.5px;color:var(--ink-2);line-height:1.45;margin-top:8px}
"""

# ───────────────────────────── helpers
SCR = []
def screen(sid, html, title, note, group):
    SCR.append(dict(id=sid, html=html, title=title, note=note, group=group))

def sb():
    return ('<div class="sb"><span>9:41</span><span style="letter-spacing:.06em">' +
            ic('sun', 'var(--ink)', 15, '2') + '</span></div>')

NAVI = [('Week', 'calendar-days', 'home'), ('Plants', 'sprout', 'plants'),
        ('Growth', 'camera', 'growth'), ('Settings', 'settings-2', 'settings')]
def nav(active='Week', badge=False):
    out = []
    for name, icon, target in NAVI:
        on = ' on' if name == active else ''
        b = '<div class="bdg"></div>' if (badge and name == 'Week') else ''
        out.append(f'<div class="ni{on}" data-go="{target}">{b}{ic(icon, "currentColor", 23)}<span>{name}</span></div>')
    return '<div class="nav">' + ''.join(out) + '</div>'

def hd(initial='Y', back=None):
    """Шапка: лого всегда по центру, «назад» слева, аватар справа."""
    left = (f'<div class="back" data-go="{back}">{ic("caret-right", "var(--ink)", 20)}</div>'
            if back else '')
    right = '' if back else f'<div class="av" data-go="settings">{initial}</div>'
    return (f'<div class="hd"><div class="hd-l">{left}</div>'
            f'<div class="wm">HOMEGROWN</div>'
            f'<div class="hd-r">{right}</div></div>')

def ofr(txt='Unlock all 30 weeks', sub='$29/yr', go='paywall'):
    return (f'<div class="ofr" data-go="{go}"><div class="ofr-in">'
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
    return (f'<div class="task{" done" if done else ""}" data-task>'
            + '<div class="box">' + ic('check', '#fff', 16, '3') + '</div>'
            + f'<div class="tt"><div class="t">{t}</div>{b}</div>'
            + f'<div class="min">{mins}</div></div>')

def ringrow(icon, name, sub, right, pct, dark=False, go=None, pick=False):
    g = ' data-add' if pick else (f' data-go="{go}"' if go else '')
    col = 'var(--lime)' if dark else 'var(--primary)'
    rr = f'<div class="rw">{ring(pct, dark)}<i>{ic(icon, col, 15, "1.9")}</i></div>' 
    if dark:
        return (f'<div class="prow"{g}>{rr}'
                f'<div class="nm"><b>{name}</b><s>{sub}</s></div><div class="rt">{right}</div></div>')
    rt = (f'<div class="addbtn">{ic("plus","var(--primary)",17,"2.4")}'
          f'{ic("check","#fff",17,"3")}</div>') if pick else f'<div class="eta">{right}</div>'
    return (f'<div class="pl"{g}>{rr}'
            f'<div class="nm"><b>{name}</b><s>{sub}</s></div>{rt}</div>')

def opt(label, sub=None, next=None, multi=False):
    """Опция онбординга. Ни одна не выбрана заранее — состояние появляется от тапа."""
    s = f'<s>{sub}</s>' if sub else ''
    attr = ' data-multi' if multi else f' data-single data-next="{next}"'
    return (f'<div class="opt"{attr}><div>{label}{s}</div>'
            f'<div class="opt-tick">{ic("check", "#fff", 14, "3")}</div></div>')

def foot(html):
    """Подвал экрана: прибит к низу, не скроллится вместе с контентом."""
    return f'<div class="foot">{html}</div>'

def pg(n, total=5):
    return '<div class="pg">' + ''.join(f'<i class="{"on" if i < n else ""}"></i>' for i in range(total)) + '</div>'

IMG = 'img/'

# ═════════════════════════════ 1. ОНБОРДИНГ
screen('landing',
 f'{sb()}<div class="shot" style="background-image:url({IMG}hero.jpg);top:48px"></div>'
 '<div class="scrim" style="top:48px"></div>'
 '<div class="overlay" style="top:48px">'
 '<div class="wm" style="color:#fff">HOMEGROWN</div>'
 '<div style="flex:1"></div>'
 '<div class="cap-f" style="font-size:41px;line-height:1.02">Grow real food<br>'
 '<span style="color:var(--lime)">where you live</span></div>'
 '<div style="font-size:16.5px;line-height:1.5;margin-top:16px;color:#DCE7DE">'
 'Patio, deck, porch or a sunny windowsill. Tell us your ZIP and how much light you get &mdash; '
 'we&rsquo;ll tell you exactly what to plant this weekend.</div>'
 '<div class="btn b-lime" style="margin-top:24px" data-go="q1">Build my free plan</div>'
 '<div style="font-size:13px;color:#C3D2C7;text-align:center;margin-top:12px">No card. Takes 90 seconds.</div></div>',
 'Landing', 'Фото на весь экран, лайм-кнопка. Никаких попапов и логина — §4.2.', 'Онбординг')

screen('q1',
 f'{sb()}{hd(back="landing")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Where will you grow?</div>' + pg(1) +
 '<div style="margin-top:16px">' +
 opt('Patio', next='q2') + opt('Deck', next='q2') + opt('Porch', next='q2') +
 opt('Backyard', next='q2') + opt('Raised bed', next='q2') + opt('Driveway / side yard', next='q2') +
 opt('Apartment balcony', next='q2') +
 opt('Windowsill / indoors', 'Herbs and greens, year-round', next='q2i') + '</div></div>',
 'Q1 · Space', 'Windowsill ведёт в <b>indoor-ветку</b> — другой вопрос о свете и план без конца сезона.', 'Онбординг')

screen('q2',
 f'{sb()}{hd(back="q1")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">What&rsquo;s your ZIP?</div>' + pg(2) +
 '<div style="margin-top:16px"><div class="zip ph" data-zip>— — — — —</div>'
 '<div style="font-size:14.5px;color:var(--muted);line-height:1.5;margin-top:16px">'
 'Your frost dates decide what you can plant right now. Tap to enter.</div>'
 '<div class="acc zipres" data-zipres style="margin-top:16px"><div class="row1"><span class="tag">Matched</span></div>'
 '<div class="lbl">Climate profile</div><div class="big">Austin, TX</div>'
 '<div class="duo"><div class="cell"><s>Last frost</s><b>Mar 3</b></div>'
 '<div class="cell"><s>Season</s><b>270 days</b></div></div></div>'
 '</div></div>' + foot('<div class="btn b-pri off" data-cta data-go="q3">Continue</div>'),
 'Q2 · ZIP', 'ZIP резолвится в climate_profile. Акцент-блок подтверждает, что система что-то <b>узнала</b>.', 'Онбординг')

screen('q3',
 f'{sb()}{hd(back="q2")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">How much direct sun<br>does that spot get?</div>' + pg(3) +
 '<div style="margin-top:16px">' +
 opt('3&ndash;5 hours', 'Mostly shade or morning sun', next='q4') +
 opt('6&ndash;8 hours', 'Good sun most of the day', next='q4') +
 opt('8+ hours', 'Full blazing sun', next='q4') +
 opt('Not sure yet', 'We&rsquo;ll start you safe and check later', next='q4') + '</div></div>',
 'Q3 · Sun', 'Главный фильтр качества плана. not_sure → 3-5 + задача Sun check.', 'Онбординг')

screen('q2i',
 f'{sb()}{hd(back="q1")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Which way does<br>your window face?</div>' + pg(3) +
 '<div style="margin-top:16px">' +
 opt('South', 'Brightest &mdash; basil and peppers work', next='q4') +
 opt('East or West', 'Good for greens and most herbs', next='q4') +
 opt('North', 'Low light &mdash; microgreens and mint only', next='q4') +
 opt('Not sure', 'We&rsquo;ll start you safe', next='q4') + '</div>'
 '<div class="card" style="margin-top:12px;display:flex;gap:12px;align-items:center">' +
 ic('lightbulb', 'var(--primary)', 24) +
 '<div style="font-size:14px;color:var(--ink-2);line-height:1.4">Got a grow light? '
 '<b style="color:var(--ink)">Tell us</b> &mdash; it upgrades your options.</div></div></div>',
 'Q3-indoor · Window', 'Для indoor солнце меряется <b>стороной окна</b>, не часами. Ложится в тот же sun_bucket.', 'Онбординг')

screen('q4',
 f'{sb()}{hd(back="q3")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">What do you want to eat?</div>'
 '<div style="font-size:14px;color:var(--muted);margin-top:4px">Up to 3 &middot; '
 '<span data-count>nothing selected yet</span></div>' + pg(4) +
 '<div style="margin-top:16px">' +
 opt('Salads &amp; greens', multi=True) + opt('Fresh herbs', multi=True) +
 opt('Fast first harvest', multi=True) + opt('Tomatoes', multi=True) +
 opt('Peppers', multi=True) + opt('Beans &amp; peas', multi=True) +
 opt('Roots: radish, carrot', multi=True) + opt('Kid-friendly project', multi=True) + '</div>'
 '</div>' + foot('<div style="font-size:13px;color:var(--muted);margin-bottom:8px;text-align:center" data-hint>'
 'Pick at least one.</div><div class="btn b-pri off" data-cta data-go="q5">Continue</div>'),
 'Q4 · Goals', 'Лимит 3. Лишние <b>гаснут, а не исчезают</b> — §4.6.', 'Онбординг')

screen('q5',
 f'{sb()}{hd(back="q4")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">How much time can<br>you give it?</div>' + pg(5) +
 '<div style="margin-top:16px">' +
 opt('About 10 minutes', 'Keep it very simple &middot; 3 crops', next='preview') +
 opt('About 20 minutes', 'I can do a bit more &middot; 4 crops', next='preview') +
 opt('30+ minutes', 'I want a real garden &middot; 5&ndash;6 crops', next='preview') + '</div></div>',
 'Q5 · Effort', 'Определяет количество культур и максимум задач в неделю.', 'Онбординг')

screen('preview',
 f'{sb()}{hd(back="q5")}<div class="bd">'
 '<div class="greet">Your plan is ready</div>'
 '<div class="cap-f" id="planhead" style="font-size:31px;line-height:1.06;margin-top:4px">4 crops.</div>'
 '<div style="font-size:13.5px;color:var(--muted);margin-top:8px" id="planmeta">Austin, TX</div>'
  '<div class="quote"><div class="qmark">&ldquo;</div>'
 '<p>Radish and leaf lettuce are what we hand every first-timer &mdash; they finish before anyone '
 'has time to lose interest. The container sizes here are the ones we actually recommend.</p>'
 '<div class="qwho"><div class="qav">MG</div><div><b>Placeholder name</b>'
 '<s>Extension master gardener &middot; sample quote</s></div></div></div>'
'<div class="acc"><div class="row1"><span class="tag">Your plan</span></div>'
 '<div class="plants" id="planrows"></div>'
 '<div class="accwhy" id="planwhy"></div></div>'
 '</div>' + foot('<div class="btn b-pri" data-go="save">Start this week&rsquo;s tasks</div>')
 + ofr('See all 30 weeks', '$29/yr'),
 'Plan Preview', '⚠ Цитата — <b>плейсхолдер</b>: настоящий отзыв надо получить у реального человека с его согласия, выдумывать его нельзя. Момент ценности. <b>План до регистрации</b> — §4.8. У каждой культуры поле why из движка.', 'Онбординг')

screen('save',
 f'<div class="shot" style="background-image:url({IMG}hero.jpg)"></div><div class="scrim"></div>'
 '<div class="overlay">'
 f'{sb().replace("var(--ink)","#fff").replace(chr(34)+"sb"+chr(34), chr(34)+"sb"+chr(34))}'
 '<div style="flex:1"></div>'
 '<span class="pill b-lime" style="align-self:flex-start">4 CROPS &middot; 30 WEEKS</span>'
 '<div class="cap-f" style="font-size:37px;line-height:1.03;margin-top:16px">Save your plan<br>'
 '<span style="color:var(--lime)">so we can remind you.</span></div>'
 '<div style="font-size:16px;color:#DCE7DE;line-height:1.5;margin-top:12px">'
 'Your plan is already built. This just saves it. We email you 3 tasks a week &mdash; nothing else.</div>'
 '<div class="btn b-lime" style="margin-top:20px" data-go="paywall">Continue with Google</div>'
 '<div class="btn b-white" data-go="paywall">Continue with email</div></div>',
 'Save Plan', 'Фото на весь экран. Регистрация — <b>после</b> показанной ценности, magic link без пароля (§4.9).', 'Онбординг')

# ═════════════════════════════ 2. HOME — два состояния
screen('home',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet" id="homegreet">Good morning</div>'
 '<div class="h1" id="homeh1">Let&rsquo;s get you growing.</div>'
 '<div id="homeacc"></div>'
 '<div id="homeprog"></div>'
 '<div id="hometasks"></div>'
 '<div id="wkwid"></div>'
 '</div>' + ofr() + nav('Week', badge=True),
 'Home', 'Один экран, два состояния. Пусто → акцентный блок зовёт добавить растение. '
 'Есть растения → в том же блоке они сами. Всё рендерится из <b>MY_PLANTS</b>, '
 'поэтому добавил одно — появится одно.', 'Home')

screen('add-plant',
 f'{sb()}{hd(back="home")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Add a plant</div>'
 '<div style="font-size:14px;color:var(--muted);margin-top:4px">'
 'Fits your patio &middot; <span data-addcount>0 of 3 chosen</span></div>'
 '<div class="search"><span class="si">' + ic('search', '#8E9A93', 19, '2') + '</span>'
 '<input id="cropq" placeholder="Search 22 crops — tomato, mint, kale…" autocomplete="off">'
 '<span class="sx" id="cropx">' + ic('x', '#8E9A93', 17, '2.4') + '</span></div>'
 '<div id="croplist"></div>'
 '<div class="note zipres" data-limit style="margin:12px 0 4px"><b>That&rsquo;s the free limit</b>'
 '<p>Free plans grow 3 crops. Pro grows everything your light and space allow &mdash; '
 'and keeps the schedule for all of them.</p>'
 '<div class="btn b-pri" data-go="paywall">Unlock &mdash; $29/yr</div></div>'
 '</div>' + foot('<div class="btn b-pri off" data-cta data-go="home">Add to my plan</div>') + nav('Plants'),
 'Add a plant', 'Культуры сгруппированы по скорости отдачи. Неподходящие <b>показаны, но погашены</b> — '
 'честнее, чем спрятать. OFF-04 стоит внизу как soft-lock.', 'Home')

screen('week-lock',
 f'{sb()}{hd(back="home")}<div class="bd">'
 '<div class="h1">Week 5 <span class="m">&middot; Apr 11&ndash;17</span></div>'
 '<div style="font-size:14px;color:var(--muted);margin-top:4px">3 tasks planned for this week</div>'
 '<div id="lockbody"></div>'
 '</div>' + nav('Week'),
 'Soft-lock', '<b>Даты и объём видны</b>, скрыты только формулировки — §10.3. Это не стена.', 'Home')


screen('week-empty',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet">Good morning &middot; Week 6 &middot; Apr 18 &ndash; Apr 24</div>'
 '<div class="h1">Nothing needed<br><span class="m">this week.</span></div>'
 '<div class="note" style="margin-top:16px"><b>Just water and watch</b>'
 '<p>Everything is on schedule. The next real job is thinning on Apr 27 &mdash; '
 'we&rsquo;ll put it on next week&rsquo;s card.</p></div>'
 '<div class="sl">Your plants</div><div id="wkplants"></div>'
 '</div>' + ofr() + nav('Week'),
 'Week · пусто', '<b>§18</b> «Nothing needed this week. Water, watch, enjoy.» '
 'Пустая неделя — это подтверждение, что всё идёт по плану, а не сломанный экран.', 'Home')

screen('week-back',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet">You were away 2 weeks</div>'
 '<div class="h1">Welcome back.<br><span class="m">Here&rsquo;s what matters now.</span></div>'
 '<div class="note" style="margin-top:16px"><b>Most of it doesn&rsquo;t matter now</b>'
 '<p>Nine tasks stopped being useful and closed themselves. Two still pay off.</p></div>'
 '<div class="sl">Two things still help</div>' +
 task('Thin your radish', '2 min', 'Crowded roots stay small &mdash; this one still pays off.') +
 task('Water deeply today', '3 min', 'Until it runs from the drainage holes.') +
 '<div class="btn b-pri" data-go="home">Continue with this week</div>'
 '</div>' + ofr() + nav('Week', badge=True),
 'Week · возврат', '<b>§6.4</b> Продукт <b>никогда</b> не показывает список из двадцати просроченных задач. '
 'Движок сворачивает пропуск в две задачи, остальное закрывается статусом expired без обвинения.', 'Home')

screen('week-long',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet">Last visit: 6 weeks ago</div>'
 '<div class="h1">It&rsquo;s been a while.<br><span class="m">Let&rsquo;s restart from today.</span></div>'
 '<div class="note" style="margin-top:16px"><b>Your plan is out of date</b>'
 '<p>Six weeks changed what&rsquo;s worth planting. We&rsquo;ll rebuild the schedule from today and keep '
 'everything you already did &mdash; 11 tasks and 4 photos stay.</p>'
 '<div class="btn b-pri" data-go="home">Rebuild my plan</div>'
 '<div class="btn b-ghost" data-go="home">Keep the old one</div></div>'
 '<div style="font-size:14px;color:var(--muted);line-height:1.45;margin-top:16px;padding:0 4px">'
 'Radish and lettuce may have bolted in the heat. If they did, that&rsquo;s normal &mdash; '
 'we&rsquo;ll sow again in the fall window.</div>'
 '</div>' + ofr() + nav('Week'),
 'Week · долгий пропуск', '<b>§19.1 №7</b> Пересчёт <b>предлагается</b>, но никогда не делается автоматически. '
 'Выполненное и журнал сохраняются, plan.version инкрементируется.', 'Home')

screen('season-end',
 '<div class="dark"><div class="glow"></div>'
 '<div class="xbtn" style="align-self:flex-end" data-go="growth">' + ic('x', '#CFE0D4', 20) + '</div>'
 '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative">'
 f'<div style="height:200px;border-radius:24px;background:url({IMG}radish.jpg) center/cover"></div>'
 '<span class="pill b-lime" style="align-self:flex-start;margin-top:20px">SEASON 2026 &middot; AUSTIN, TX</span>'
 '<div class="cap-f" style="font-size:40px;line-height:1.02;margin-top:12px">14 harvests.<br>187 days.</div>'
 '<div style="font-size:16px;color:#A9BCB0;line-height:1.5;margin-top:12px">'
 'Radish, leaf lettuce and basil all made it to the table. Your first pick was April 12 &mdash; day 31.</div></div>'
 '<div class="btn b-lime" data-go="paywall">Plan next year now</div>'
 '<div class="btn" style="background:#1B3527;color:#fff" data-go="growth">Download season recap</div></div>',
 'Season ended · OFF-11', '<b>§7.5</b> Триггер <b>today &ge; first_frost</b>. Итог сезона + план на следующий год. '
 'Для indoor-трека это состояние <b>не наступает никогда</b>.', 'Home')

# ═════════════════════════════ 3. PLANTS
screen('plants',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Your plants</div>'
 '<div style="font-size:14px;color:var(--muted);margin-top:4px" id="plantsmeta">&nbsp;</div>'
 '<div id="plantlist"></div>'
 '<div class="btn b-ghost" data-go="add-plant" style="margin-top:16px">Add a plant</div>'
 '</div>' + ofr() + nav('Plants'),
 'Plants', 'Список из состояния. У каждой строки — крестик удаления с <b>Undo</b>: '
 'удаление не должно быть страшным, растения гибнут и пересеваются (§19.1 №8).', 'Plants')

screen('plant',
 f'{sb()}{hd(back="plants")}<div class="bd" id="pdetail"></div>' + nav('Plants'),
 'Plant detail', 'Карточка выбранного растения. Если фото ещё нет — <b>плитка «Add a photo»</b>, '
 'а не пустые серые квадраты. Внизу — удаление с подтверждением через Undo.', 'Plants')

# ═════════════════════════════ 4. GROWTH
screen('growth',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="h1">Your season</div>'
 '<div style="font-size:14px;color:var(--muted);margin-top:4px" id="seasonsub">&nbsp;</div>'
 '<div id="dash"></div>'
 '<div id="cropcards"></div>'
 '</div>' + ofr('Keep every photo', '$29/yr') + nav('Growth'),
 'Growth', 'Пересобрано: раньше здесь были <b>две сущности про одно и то же</b> — список культур и '
 'отдельная сетка фото, хотя каждое фото и так принадлежит культуре. Теперь один дашборд сезона '
 'и карточки культур, у каждой свои снимки и своя статистика. Тап по карточке ведёт в растение, '
 'где лежит полный таймлайн и полоса «типичный диапазон».', 'Growth')

screen('harvest',
 '<div class="dark" style="padding:0">'
 f'<div class="shot" style="background-image:url({IMG}radish.jpg);height:58%"></div>'
 '<div class="scrim" style="height:58%;background:linear-gradient(180deg,rgba(11,31,20,.45),rgba(11,31,20,0) 40%,var(--deepest))"></div>'
 '<div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:24px 24px">'
 '<div class="xbtn" style="align-self:flex-end" data-go="growth">' + ic('x', '#CFE0D4', 17, '2') + '</div>'
 '<div style="flex:1"></div>'
 '<span class="pill b-lime" style="align-self:flex-start">Day 31</span>'
 '<div class="cap-f" style="font-size:40px;line-height:1.02;margin-top:12px;color:#fff">First harvest.</div>'
 '<div style="font-size:16px;color:#C6D6CA;line-height:1.5;margin-top:12px">'
 'You grew this on your patio. Sow the next round Apr 15 &mdash; your lettuce is 6 days out.</div>'
 '<div class="btn b-lime" style="margin-top:20px" data-go="growth">Add a photo</div>'
 '<div class="btn" style="background:#1B3527;color:#fff" data-go="growth">Get my harvest card</div></div></div>',
 'Harvest Moment', 'Тёмный экран с настоящим фото вместо нюдового. Пик удержания и лучшая точка конверсии — §9.', 'Growth')

screen('shopping',
 f'{sb()}{hd(back="home")}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Shopping list</div>'
 '<div style="font-size:14px;color:var(--muted);margin-top:4px">Everything for week 1 &middot; about $47</div>'
 '<div class="sl">Containers</div>' +
 task('1-gallon pot &times;2', '~$8', 'Basil and the cherry tomato.') +
 task('Window box, 24 inch', '~$14', 'Lettuce and radish share it.') +
 task('Saucers &times;3', '~$6') +
 '<div class="sl">SOIL &amp; SEED</div>' +
 task('Potting mix, 1 cu ft', '~$12', 'Not garden soil &mdash; too much clay for a pot.') +
 task('Radish + lettuce seed', '~$7') +
 '<div class="btn b-ghost" data-go="paywall">Printable PDF &mdash; Pro</div>'
 '</div>' + nav('Week'),
 'Shopping list', 'Free — список на экране, Pro — печатный PDF. Ценность видна до покупки.', 'Growth')

# ═════════════════════════════ 5. PAYWALL (референс Fit AI)
FEATS = ['All 30 weeks of tasks, not just this one', 'Every crop and every succession sowing',
         'Printable shopping list as PDF', 'Unlimited journal photos + season recap',
         'Up to 5 growing spaces']
screen('paywall',
 '<div class="dark"><div class="glow"></div><div class="glow b"></div>'
 '<div style="display:flex;justify-content:space-between;align-items:center;position:relative">'
 '<div style="display:flex;align-items:center;gap:8px">' + ic('sprout', 'var(--lime)', 24, '2') +
 '<span style="font-size:14px;font-weight:700;letter-spacing:.1em">HOMEGROWN</span></div>'
 '<div class="xbtn" data-pw-exit>' + ic('x', '#CFE0D4', 17, '2') + '</div></div>'
 '<div style="text-align:center;margin-top:24px;position:relative">'
 '<div style="font-size:31px;font-weight:600;line-height:1.14;letter-spacing:-.02em">'
 'Grow the whole<br><span style="color:var(--lime)">season, planned.</span></div>'
 '<div style="font-size:14.5px;color:#A9BCB0;margin-top:8px">7 days free. Cancel anytime.</div></div>'
 '<div class="seg"><div class="on" data-seg>Season pass</div><div data-seg>Monthly</div></div>'
 '<div class="pcard"><div style="display:flex;justify-content:space-between;align-items:flex-start">'
 '<div><div class="pr">$29<span style="font-size:15px;font-weight:500;color:#A9BCB0"> / year</span></div>'
 '<div class="pn">Cheaper than one tray of seedlings. Covers a full season, start to frost.</div></div>'
 '<span class="pill b-lime">Best</span></div>'
 '<div class="feat">' + ''.join(f'<div><i></i><span>{f}</span></div>' for f in FEATS) + '</div></div>'
 '<div style="flex:1;min-height:16px"></div>'
 '<div class="btn b-white" data-buy>Start 7-day free trial</div>'
 '<div style="font-size:14px;color:#fff;text-align:center;margin-top:16px;cursor:pointer;font-weight:600" data-pw-exit>'
 'Continue with the free plan</div>'
 '<div style="font-size:12px;color:#6E8175;text-align:center;margin-top:8px;line-height:1.45">'
 'No card for the trial. Your plan and photos stay yours either way.</div></div>',
 'Paywall', 'Собран по референсу Fit AI: тёмный фон, лаймовый glow, сегмент-переключатель, '
 'фичи с точками, белый CTA. Годовой подан как <b>Season pass</b>, не как скидка — §12.2. '
 'Триал без карты — вариант B из §12.4. Показывается <b>сразу после регистрации</b> и закрывается ''в тот экран, откуда пришёл. Конфликт со спекой: §10.4 запрещает оффер до первой выполненной задачи ''(never_before_first_task = true).', 'Деньги')

screen('week-done',
 '<div class="dark"><div class="glow"></div>'
 '<div class="xbtn" style="align-self:flex-end" data-go="home">' + ic('x', '#CFE0D4', 17, '2') + '</div>'
 '<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative">'
 f'<div style="height:200px;border-radius:24px;background:url({IMG}garden.jpg) center/cover"></div>'
 '<span class="pill b-lime" style="align-self:flex-start;margin-top:20px">Week 3 Complete</span>'
 '<div style="font-size:30px;font-weight:600;line-height:1.15;margin-top:12px">Everything<br>'
 '<span style="color:var(--lime)">on time.</span></div>'
 '<div style="font-size:15.5px;color:#A9BCB0;line-height:1.5;margin-top:12px">'
 'Your radish is 14 days out. Pro maps the next 27 weeks so you never wonder what&rsquo;s next.</div>'
 '<div class="sg2"><div class="stat"><b style="color:var(--lime)">11</b><s>weeks in a row</s></div>'
 '<div class="stat"><b>4/4</b><s>tasks this week</s></div></div></div>'
 '<div class="btn b-lime" data-go="paywall">See the whole season</div>'
 '<div class="btn" style="background:#1B3527;color:#fff" data-go="home">Not now</div></div>',
 'Week complete · OFF-05', 'success_modal, <b>не чаще 1 раза в 7 дней</b>. Прозрачного скрима нет — полный экран.', 'Деньги')

# ═════════════════════════════ 6. SETTINGS
screen('settings',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="h1" style="margin-top:16px">Settings</div>'
 '<div id="planbox"></div>'
 '<div class="sl">Your space</div><div class="plist">'
 '<div class="pl"><div class="nm"><b>Space</b><s>Back patio</s></div>' + ic('chevron-right', '#B4BEB8', 18) + '</div>'
 '<div class="pl"><div class="nm"><b>ZIP</b><s>78704 &middot; Austin, TX</s></div>' + ic('chevron-right', '#B4BEB8', 18) + '</div>'
 '<div class="pl"><div class="nm"><b>Sun</b><s>6&ndash;8 hours</s></div>' + ic('chevron-right', '#B4BEB8', 18) + '</div>'
 '<div class="pl"><div class="nm"><b>Time per week</b><s>20 minutes</s></div>' + ic('chevron-right', '#B4BEB8', 18) + '</div></div>'
 '<div class="sl">Email</div><div class="plist">'
 '<div class="pl"><div class="nm"><b>Weekly tasks</b></div>'
 '<div class="tgl on" role="switch" aria-checked="true" tabindex="0"><i></i></div></div>'
 '<div class="pl"><div class="nm"><b>Harvest reminders</b></div>'
 '<div class="tgl on" role="switch" aria-checked="true" tabindex="0"><i></i></div></div>'
 '<div class="pl"><div class="nm"><b>Season updates</b></div>'
 '<div class="tgl"><i></i></div></div></div>'
 '<div class="sl">Data</div><div class="plist">'
 '<div class="pl"><div class="nm"><b>Units</b><s>Imperial</s></div>' + ic('chevron-right', '#B4BEB8', 18) + '</div>'
 '<div class="pl"><div class="nm"><b>Delete account</b><s>Requires typing DELETE</s></div>' + ic('chevron-right', '#B4BEB8', 18) + '</div></div>'
 '</div>' + nav('Settings'),
 'Settings', 'Смена света, ZIP или усилия <b>предлагает</b> пересчёт, но не делает его сама — §20.', 'Система')

# ═════════════════════════════ 7. INDOOR
screen('indoor',
 f'{sb()}{hd()}<div class="bd">'
 '<div class="greet">Good morning &middot; Week 12</div>'
 '<div class="h1">Basil is ready<br><span class="m">to cut again.</span></div>'
 f'<div class="acc"><div class="acc-photo" style="background-image:url({IMG}flowers.jpg)"></div>'
 '<div class="row1"><span class="tag">WINDOWSILL &middot; YEAR-ROUND</span></div>'
 '<div class="plants">' +
 ringrow('leaf', 'Basil', 'Cut 7 times &middot; regrows in 10d', 'ready', 100, dark=True, go='plant') +
 ringrow('wheat', 'Microgreens', 'Tray 3 &middot; day 8', '~2d', 80, dark=True) +
 ringrow('clover', 'Cilantro', 'Cut 2 times &middot; next in 9d', '~9d', 60, dark=True) +
 ringrow('sprout', 'Garlic chives', 'Day 34 &middot; first cut Jun 8', '~50d', 40, dark=True) +
 '</div>'
 '<div class="duo"><div class="cell"><s>Cuts this year</s><b style="color:var(--lime)">23</b></div>'
 '<div class="cell"><s>Season ends</s><b>never</b></div></div></div>'
 '<div class="sl">This week</div>' +
 task('Cut 6 basil leaves from the top', '2 min', 'Cut above a leaf pair &mdash; it branches and doubles.') +
 task('Sow a new microgreens tray', '5 min') +
 task('Water check: soil top dry?', '2 min') +
 '</div>' + ofr('Add a second windowsill', 'Pro') + nav('Week', badge=True),
 'Indoor · Home', '«Season ends: never» — вот почему indoor закрывает сезонность. '
 'Ритм — <b>срез каждую неделю</b>, а не один сбор за 30 дней.', 'Indoor')


# ── каталог культур для поиска и мини-движка плана (§15.1 + indoor)
CROPS = [
 ('Radish','carrot',25,35,'1 pint',1,['fast','roots','kids']),
 ('Leaf lettuce','salad',30,35,'0.5 gal',1,['salads','fast']),
 ('Swiss chard','leafy-green',30,40,'0.5 gal',1,['salads']),
 ('Mustard greens','leafy-green',35,40,'0.5 gal',1,['salads']),
 ('Microgreens','wheat',10,14,'tray',1,['fast','herbs','kids']),
 ('Cilantro','clover',28,42,'0.5 gal',1,['herbs','fast']),
 ('Basil','leaf',40,40,'1 gal',2,['herbs']),
 ('Bush beans','bean',45,60,'2 gal',2,['beans','kids']),
 ('Beets','carrot',50,60,'0.5 gal',1,['roots']),
 ('Summer squash','orange',50,60,'5 gal',2,[]),
 ('Cherry tomato','apple',55,100,'1 gal',2,['tomatoes','kids']),
 ('Tomato','apple',55,100,'5 gal',2,['tomatoes']),
 ('Kale','leafy-green',55,65,'5 gal',1,['salads']),
 ('Turnips','carrot',30,60,'3 gal',1,['roots']),
 ('Carrots','carrot',65,80,'1 quart',1,['roots','kids']),
 ('Cucumber','orange',70,80,'5 gal',2,[]),
 ('Green onions','plant',70,100,'0.5 gal',1,['herbs']),
 ('Parsley','leafy-green',70,84,'0.5 gal',1,['herbs']),
 ('Eggplant','pepper',75,100,'5 gal',2,[]),
 ('Garlic chives','plant',84,84,'0.5 gal',1,['herbs']),
 ('Bell pepper','pepper',110,120,'2 gal',2,['peppers']),
]
ICONSET = sorted({c[1] for c in CROPS} | {'plant','orange','pepper','flower','potted-plant','basket'})

JS_SRC = r'''
const ICONS = __ICONS__;
const CROPS = __CROPS__;
const RING_TRACK = '#DDE3DC', RING_ON = '#22A559';
const CHOICES = {space:'a patio', sun:'6-8 h sun', sunRank:2, goals:[], effort:4, indoor:false};

function ringSVG(pct, sz, dark, sw){
  sz = sz || 38; sw = sw || 3.2;
  const r = (sz-sw)/2, c = 2*Math.PI*r, off = c*(1-Math.max(0,Math.min(100,pct))/100);
  const tr = dark ? 'rgba(255,255,255,.20)' : RING_TRACK, on = dark ? '#B4F461' : RING_ON;
  return '<svg class="rg" width="'+sz+'" height="'+sz+'" viewBox="0 0 '+sz+' '+sz+'">'
   +'<circle cx="'+sz/2+'" cy="'+sz/2+'" r="'+r+'" fill="none" stroke="'+tr+'" stroke-width="'+sw+'"/>'
   +'<circle cx="'+sz/2+'" cy="'+sz/2+'" r="'+r+'" fill="none" stroke="'+on+'" stroke-width="'+sw+'"'
   +' stroke-linecap="round" stroke-dasharray="'+c.toFixed(1)+'" stroke-dashoffset="'+off.toFixed(1)+'"'
   +' transform="rotate(-90 '+sz/2+' '+sz/2+')"/></svg>';
}
function cropRow(c){
  const have = MY_PLANTS.some(p=>p.c[0]===c[0]);
  const pick = PENDING.includes(c[0]);
  return '<div class="pl'+(pick?' added':'')+(have?' have':'')+'" '+(have?'':'data-add ')+'data-crop="'+c[0]+'">'
   +'<div class="rw">'+ringSVG(0)+'<i>'+ICONS[c[1]]+'</i></div>'
   +'<div class="nm"><b>'+c[0]+'</b><s>'+c[2]+(c[3]!==c[2]?'–'+c[3]:'')+' days · '+c[4]
   +(c[5]>CHOICES.sunRank?' · needs more sun':'')+'</s></div>'
   +'<div class="addbtn">'+(have?ICONS._checkg:ICONS._plus+ICONS._check)+'</div></div>';
}
function renderCrops(q){
  q = (q||'').trim().toLowerCase();
  const box = document.getElementById('croplist'); if(!box) return;
  const cnt = document.querySelector('[data-addcount]');
  if(cnt) cnt.textContent = PENDING.length ? PENDING.length+' selected' : 'nothing selected yet';
  const cta = document.querySelector('#s-add-plant [data-cta]');
  if(cta){ cta.classList.toggle('off', !PENDING.length);
           cta.textContent = PENDING.length ? 'Add '+PENDING.length+' to my plan' : 'Add to my plan'; }
  const lim = document.querySelector('#s-add-plant [data-limit]');
  if(lim) lim.style.display = !IS_PRO && (MY_PLANTS.length+PENDING.length)>=FREE_LIMIT ? 'block' : 'none';
  const fits = CROPS.filter(c=>c[5]<=CHOICES.sunRank), rest = CROPS.filter(c=>c[5]>CHOICES.sunRank);
  const m = a => !q || a[0].toLowerCase().includes(q) || a[6].some(t=>t.includes(q));
  const A = fits.filter(m), B = rest.filter(m);
  if(!A.length && !B.length){
    box.innerHTML = '<div class="empty">Nothing matches “'+q+'”.<br>We grow 21 crops that finish in one season.</div>';
    return;
  }
  let h = '';
  if(A.length){
    const fast = A.filter(c=>c[2]<=35), slow = A.filter(c=>c[2]>35);
    if(fast.length) h += '<div class="gsec">Fast wins</div><div class="plist">'+fast.map(c=>cropRow(c)).join('')+'</div>';
    if(slow.length) h += '<div class="gsec">Worth the wait</div><div class="plist">'+slow.map(c=>cropRow(c)).join('')+'</div>';
  }
  if(B.length) h += '<div class="gsec">Needs more sun than you have</div><div class="plist" style="opacity:.5">'
                    +B.map(c=>cropRow(c)).join('')+'</div>';
  box.innerHTML = h;
}
function buildPlan(){
  const g = CHOICES.goals, n = CHOICES.effort;
  let pool = CROPS.filter(c=>c[5]<=CHOICES.sunRank);
  const score = c => (c[6].filter(t=>g.includes(t)).length*40) + (c[2]<=35?20:0) + (120-c[3])/12;
  pool = pool.slice().sort((a,b)=>score(b)-score(a));
  const out = [];
  for(const c of pool){
    if(out.length>=n) break;
    if(c[2]>70 && out.filter(x=>x[2]>70).length>=2) continue;
    out.push(c);
  }
  if(!out.some(c=>c[2]<=35)){ const f = pool.find(c=>c[2]<=35); if(f){ out.pop(); out.unshift(f); } }
  return out;
}
const MONTH = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function dateAfter(days){ const d = new Date(2026,2,14); d.setDate(d.getDate()+days); return MONTH[d.getMonth()]+' '+d.getDate(); }
function renderPreview(){
  const plan = buildPlan(); const first = Math.min.apply(null, plan.map(c=>c[2]));
  const el = document.getElementById('planrows'); if(!el) return;
  el.innerHTML = plan.map(c=>'<div class="prow"><div class="rw">'+ringSVG(0)+'<i>'+ICONS[c[1]]+'</i></div>'
    +'<div class="nm"><b>'+c[0]+'</b><s>'+c[4]+' · '+c[2]+(c[3]!==c[2]?'–'+c[3]:'')+' days</s></div>'
    +'<div class="rt">'+dateAfter(c[2])+'</div></div>').join('');
  document.getElementById('planhead').innerHTML = plan.length+' crops.<br>First pick '+dateAfter(first)+'.';
  document.getElementById('planmeta').textContent =
    'Austin, TX · '+CHOICES.sun+' · '+CHOICES.space+' · about '+(CHOICES.effort===3?10:CHOICES.effort===4?20:30)+' min a week';
  const got = new Set(plan.flatMap(c=>c[6]));
  const asked = CHOICES.goals.length ? CHOICES.goals : ['fast'];
  const kept = asked.filter(g=>got.has(g)), missed = asked.filter(g=>!got.has(g));
  const list = a => a.map(x=>GOALWORD[x]||x).reduce((s,x,i,arr)=>
      s + (i===0?'':(i===arr.length-1?' and ':', ')) + x, '');
  const fast = plan.reduce((a,b)=>b[2]<a[2]?b:a);
  let t = '<b>Why these:</b> you asked for ' + list(asked.length?asked:['fast'])
        + ', and ' + CHOICES.sun + ' is what decides the rest. '
        + fast[0] + ' is your fast win — ready in ' + fast[2] + ' days.';
  if(missed.length){
    const need = missed.map(m=>SUNNEED[m]).filter(Boolean)[0];
    t += '<span class="warn">' + list(missed).replace(/^./,c=>c.toUpperCase())
       + (need ? ' need ' + need + ' of direct sun. At your light they rarely finish, '
               : ' need more light than you have, ')
       + 'so we left them out and gave you ' + list(kept.length?kept:['a reliable harvest'])
       + ' instead. You can add them any time.</span>';
  }
  document.getElementById('planwhy').innerHTML = t;
}

/* ─────────── состояние: растения, фото, корзина добавления ─────────── */
let MY_PLANTS = [], SELECTED = 0, PENDING = [], UNDO = null, UNDOT = null, IS_PRO = false;
const PHOTOS = ['radish','leaves1','basil','leaves3','flowers'];
const FREE_LIMIT = 3;
const limit = () => IS_PRO ? 99 : FREE_LIMIT;

function crop(name){ return CROPS.find(c=>c[0]===name); }
function mk(name, day, photos){ return {c:crop(name), day:day, photos:photos||[]}; }
function seedPlants(){
  MY_PLANTS = [mk('Radish',27,[{f:'radish',day:24},{f:'leaves1',day:11}]),
               mk('Leaf lettuce',27,[{f:'leaves3',day:18}]),
               mk('Basil',27,[{f:'basil',day:21}]), mk('Cherry tomato',9,[])];
}
const pPct   = p => Math.min(100, Math.round(p.day / p.c[2] * 100));
const pStage = p => { const r = p.day/p.c[2];
  return r<0.1?'seed':r<0.35?'seedling':r<0.7?'growing':r<1?'nearly ready':'ready'; };
const pEta   = p => { const d = p.c[2]-p.day; return d<=0 ? 'ready' : '~'+d+'d'; };
const stageAt = (p,d) => { const r = d/p.c[2];
  return r<0.1?'seed':r<0.35?'seedling':r<0.7?'growing':r<1?'nearly ready':'ready'; };
const allPhotos = () => MY_PLANTS.flatMap(p=>p.photos.map(x=>
  ({f:x.f, u:x.u, n:p.c[0], day:x.day, st:stageAt(p,x.day)}))).sort((a,b)=>b.day-a.day);

/* ─────────── HOME ─────────── */
const WEEK_TASKS = [
  ['Thin radish to 1 inch apart','2 min','Pull the smallest seedlings so each root has room.'],
  ['Sow second round of lettuce','10 min',''],
  ['Water check: soil top dry?','2 min',''],
  ['Feed tomato','3 min',''],
  ['Stake the tomato','5 min',''],
  ['Pinch basil tops','2 min','']];
const CARDS_SHOWN = 4;
let DONE = [], WEEK_OPEN = true;
function taskHTML(t){
  return '<div class="task" data-task><div class="box">'+ICONS._check2+'</div><div class="tt">'
    +'<div class="t">'+t[0]+'</div>'+(t[2]?'<div class="b">'+t[2]+'</div>':'')
    +'</div><div class="min">'+t[1]+'</div></div>';
}
function renderHome(){
  const acc=document.getElementById('homeacc'); if(!acc) return;
  const g=document.getElementById('homegreet'), h=document.getElementById('homeh1'),
        pr=document.getElementById('homeprog'), tk=document.getElementById('hometasks');
  if(!MY_PLANTS.length){
    g.textContent='Good morning';
    h.innerHTML='Let&rsquo;s get you<br><span class="m">growing.</span>';
    acc.innerHTML='<div class="acc"><div class="acc-photo" style="background-image:url(img/garden.jpg)"></div>'
      +'<div class="row1"><span class="tag">Nothing Planted Yet</span></div>'
      +'<div class="lbl">Your patio &middot; 6&ndash;8 h sun</div>'
      +'<div class="big">4 crops fit<br>your space</div>'
      +'<div class="sub">Radish, leaf lettuce, basil and a cherry tomato all finish here. '
      +'First pick around April 12.</div>'
      +'<div class="btn b-lime" data-go="add-plant">Add your first plant</div></div>';
    pr.innerHTML='';
    tk.innerHTML='<div class="sl">First thing this week</div>'
      +taskHTML(['Buy containers + potting mix','25 min','Everything else waits on this one.'])
      +'<div class="btn b-ghost" data-go="shopping">See the shopping list</div>';
    return;
  }
  const n=MY_PLANTS.length;
  g.textContent='Good morning · Week 3 · Mar 28 – Apr 3';
  h.innerHTML=WEEK_TASKS.length+' things to do';
  acc.innerHTML='<div class="acc"><div class="row1"><span class="tag">Your plants &middot; '+n+'</span>'
    +'<div class="addtop" data-go="add-plant">'+ICONS._plusd+'<span>Add</span></div></div>'
    +'<div class="plants">'+MY_PLANTS.map((p,i)=>
       '<div class="prow" data-open="'+i+'"><div class="rw">'+ringSVG(pPct(p),38,true)+'<i>'+ICONS[p.c[1]]+'</i></div>'
      +'<div class="nm"><b>'+p.c[0]+'</b><s>Day '+p.day+' &middot; '+pStage(p)+'</s></div>'
      +'<div class="rt">'+pEta(p)+'</div></div>').join('')+'</div>'
    +'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px;padding-top:12px;'
    +'border-top:1px solid rgba(255,255,255,.12);position:relative">'
    +'<span style="font-size:13px;color:#B7C7BD">Next harvest <b style="color:#fff;font-weight:600">Apr 12</b></span>'
    +'<span style="font-size:13px;color:var(--lime);font-weight:600">11-week streak</span></div></div>';
  renderWeek();
}

/* ─────────── PLANTS + удаление ─────────── */
function renderPlants(){
  const box=document.getElementById('plantlist'); if(!box) return;
  document.getElementById('plantsmeta').textContent =
    MY_PLANTS.length ? MY_PLANTS.length+' growing · '+(IS_PRO ? 'Pro · unlimited crops' : MY_PLANTS.length+' of '+FREE_LIMIT+' free slots used')
                     : 'Nothing planted yet';
  if(!MY_PLANTS.length){
    box.innerHTML='<div class="note" style="margin-top:16px"><b>No plants yet</b>'
      +'<p>Pick something that finishes fast — radish is ready in 25 days.</p>'
      +'<div class="btn b-pri" data-go="add-plant">Add a plant</div></div>'; return;
  }
  box.innerHTML='<div class="plist" style="margin-top:16px">'+MY_PLANTS.map((p,i)=>
     '<div class="pl"><div data-open="'+i+'" style="display:flex;align-items:center;gap:12px;flex:1;min-width:0">'
    +'<div class="rw">'+ringSVG(pPct(p))+'<i>'+ICONS[p.c[1]]+'</i></div>'
    +'<div class="nm"><b>'+p.c[0]+'</b><s>Day '+p.day+' &middot; '+pStage(p)+' &middot; '+pEta(p)+'</s></div></div>'
    +'<div class="del" data-del="'+i+'">'+ICONS._x+'</div></div>').join('')+'</div>';
}
function removePlant(i){
  UNDO={p:MY_PLANTS[i], i:i}; MY_PLANTS.splice(i,1);
  renderPlants(); renderHome(); renderJournal();
  const t=document.getElementById('toast');
  t.innerHTML='<span>'+UNDO.p.c[0]+' removed</span><b data-undo>Undo</b>';
  t.classList.add('on'); clearTimeout(UNDOT);
  UNDOT=setTimeout(()=>{t.classList.remove('on'); UNDO=null;}, 4500);
}
function undoRemove(){
  if(!UNDO) return;
  MY_PLANTS.splice(UNDO.i,0,UNDO.p); UNDO=null;
  document.getElementById('toast').classList.remove('on');
  renderPlants(); renderHome(); renderJournal();
}

/* ─────────── PLANT DETAIL ─────────── */
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
  const box=document.getElementById('pdetail'); if(!box) return;
  const p=MY_PLANTS[SELECTED];
  if(!p){ box.innerHTML='<div class="note" style="margin-top:16px"><b>This plant is gone</b>'
      +'<p>You removed it. Nothing is lost — sow it again whenever you like.</p>'
      +'<div class="btn b-pri" data-go="add-plant">Add a plant</div></div>'; return; }
  const hero = p.photos.length
    ? '<div style="height:192px;border-radius:var(--r-lg);background:url(img/'+p.photos[0]
      +'.jpg) center/cover;margin-top:16px"></div>'
    : '<div class="herostub">'+ICONS._cam2+'<div><b>No photo yet</b><s>One shot a week builds the whole timeline.</s></div></div>';
  const strip = p.photos.length
    ? '<div class="jgrid">'+p.photos.map(x=>photoCard({f:x.f,n:p.c[0],day:x.day,st:stageAt(p,x.day)})).join('')
      +'</div>'+addPhotoBtn()
    : addPhotoBtn('Add the first photo');
  box.innerHTML = hero
    +'<div style="display:flex;align-items:center;gap:12px;margin-top:16px">'
    +'<div class="rw" style="width:52px;height:52px">'+ringSVG(pPct(p),52,false,4)+'<i>'+ICONS[p.c[1]]+'</i></div>'
    +'<div><div style="font-size:23px;font-weight:600">'+p.c[0]+'</div>'
    +'<div style="font-size:13.5px;color:var(--muted)">Sown Mar 14 &middot; '+p.c[4]+' &middot; patio</div></div></div>'
    +'<div class="card" style="margin-top:16px">'
    +'<div style="display:flex;justify-content:space-between;align-items:baseline">'
    +'<b style="font-size:16px">Day '+p.day+'</b>'
    +'<span style="font-size:13px;color:var(--muted)">typical '+p.c[2]+'–'+p.c[3]+'</span></div>'
    +'<div style="position:relative;height:32px;margin-top:8px">'
    +'<div style="position:absolute;top:12px;left:0;right:0;height:8px;border-radius:999px;background:#DDE3DC"></div>'
    +'<div style="position:absolute;top:12px;left:'+(p.c[2]/(p.c[3]*1.25)*100).toFixed(0)+'%;width:'
    +((p.c[3]-p.c[2])/(p.c[3]*1.25)*100).toFixed(0)+'%;height:8px;border-radius:999px;background:var(--lime)"></div>'
    +'<div style="position:absolute;top:8px;left:calc('+Math.min(96,p.day/(p.c[3]*1.25)*100).toFixed(0)
    +'% - 9px);width:16px;height:16px;border-radius:50%;background:var(--primary);box-shadow:0 0 0 3px #fff"></div></div>'
    +'<div style="font-size:14px;color:var(--ink-2);line-height:1.45">'
    +(p.day>=p.c[2] ? 'Ready to pick. Most of these finish between day '+p.c[2]+' and '+p.c[3]+'.'
                    : 'On track. Most of these finish between day '+p.c[2]+' and '+p.c[3]+'.')+'</div></div>'
    +'<div class="sl">Timeline'+(p.photos.length?' &middot; '+p.photos.length+' photos':'')+'</div>'+strip
    +'<div class="sl">Task history</div>'
    +'<div class="task done" data-task><div class="box">'+ICONS._check2+'</div>'
    +'<div class="tt"><div class="t">Sow '+p.c[0].toLowerCase()+'</div></div><div class="min">Mar 14</div></div>'
    +(p.day>=p.c[2] ? '<div class="btn b-pri" data-go="harvest">Harvest it — ready now</div>' : '')
    +'<div class="btn b-ghost" data-remove>Remove from my plan</div>';
}

/* ─────────── JOURNAL ─────────── */
function renderJournal(){
  const box=document.getElementById('journal'); if(!box) return;
  const ph=allPhotos(); const lab=document.getElementById('jlab');
  if(lab) lab.textContent = !ph.length ? 'Journal'
    : (IS_PRO ? 'Journal · '+ph.length+' photos' : 'Journal · '+ph.length+' of 5 free photos');
  if(!ph.length){
    box.innerHTML='<div class="note"><b>Take one photo today</b>'
      +'<p>In 30 days you&rsquo;ll want to see it. One shot a week is enough to build the whole timeline.</p>'
      +addPhotoBtn('Take the first photo')+'</div>'; return;
  }
  box.innerHTML='<div class="jgrid">'+ph.map(photoCard).join('')+'</div>'+addPhotoBtn();
}

function buyPro(){
  IS_PRO = true;
  document.body.classList.add('is-pro');
  renderAll(); renderLock(); renderSettingsPlan();
  const t=document.getElementById('toast');
  t.innerHTML='<span>Pro unlocked — all 30 weeks are open</span><b data-unpro>Undo</b>';
  t.classList.add('on'); clearTimeout(UNDOT);
  UNDOT=setTimeout(()=>t.classList.remove('on'), 5000);
  go(PW_FROM);
}
function dropPro(){
  IS_PRO = false; document.body.classList.remove('is-pro');
  renderAll(); renderLock(); renderSettingsPlan();
  document.getElementById('toast').classList.remove('on');
}
function renderLock(){
  const box=document.getElementById('lockbody'); if(!box) return;
  if(IS_PRO){
    box.innerHTML='<div class="sl">This week</div>'
      +taskHTML(['Thin the carrots','4 min','Crowded roots stay small.'])
      +taskHTML(['Feed the tomato','3 min',''])
      +taskHTML(['Sow the next round of beans','10 min',''])
      +'<div class="note" style="margin-top:12px"><b>You have the whole season</b>'
      +'<p>All 30 weeks are planned. Nothing is hidden any more.</p></div>';
    return;
  }
  box.innerHTML='<div class="sl">This week</div>'
    +'<div class="task"><div class="box"></div><div class="tt"><div class="blur" style="width:76%;margin-bottom:8px">'
    +'</div><div class="blur" style="width:52%"></div></div><div class="min">4 min</div></div>'
    +'<div class="task"><div class="box"></div><div class="tt"><div class="blur" style="width:60%"></div></div>'
    +'<div class="min">3 min</div></div>'
    +'<div class="task"><div class="box"></div><div class="tt"><div class="blur" style="width:68%"></div></div>'
    +'<div class="min">10 min</div></div>'
    +'<div class="acc" style="margin-top:16px"><div class="row1"><span class="tag">Locked</span></div>'
    +'<div class="big" style="font-size:24px;margin-top:16px">Pro unlocks<br>all 30 weeks</div>'
    +'<div class="sub">The dates and the workload are real — only the wording is hidden.</div>'
    +'<div class="btn b-lime" data-go="paywall">Unlock full season</div></div>';
}
function renderSettingsPlan(){
  const el=document.getElementById('planbox'); if(!el) return;
  el.innerHTML = IS_PRO
   ? '<div class="acc" style="margin-top:16px"><div class="row1"><span class="tag">Pro · season pass</span></div>'
     +'<div class="big" style="font-size:24px;margin-top:16px">Everything is open</div>'
     +'<div class="sub">All 30 weeks, every crop, unlimited photos, up to 5 spaces. Renews Mar 14, 2027.</div>'
     +'<div class="btn" style="background:#17492F;color:#fff" data-unpro>Back to Free (demo)</div></div>'
   : '<div class="acc" style="margin-top:16px"><div class="row1"><span class="tag">Free plan</span></div>'
     +'<div class="big" style="font-size:24px;margin-top:16px">1 space · 3 crops<br>this week only</div>'
     +'<div class="btn b-lime" data-go="paywall">Compare with Pro</div></div>';
}


/* ─────────── камера: снимок с устройства попадает в журнал ─────────── */
let CAM_TARGET = null;
function openCamera(target){
  CAM_TARGET = (target===undefined || target===null) ? SELECTED : target;
  const el = document.getElementById('cam');
  if(el){ el.value=''; el.click(); }
}
function attachShot(file){
  if(!file || !MY_PLANTS.length) return;
  const i = (CAM_TARGET!==null && MY_PLANTS[CAM_TARGET]) ? CAM_TARGET : 0;
  const p = MY_PLANTS[i];
  p.photos.unshift({u: URL.createObjectURL(file), day: p.day});
  renderAll();
  const t=document.getElementById('toast');
  t.innerHTML='<span>Photo added to '+p.c[0]+'</span><b data-gogrowth>See journal</b>';
  t.classList.add('on'); clearTimeout(UNDOT);
  UNDOT=setTimeout(()=>t.classList.remove('on'), 4000);
}



/* ─────────── прогресс-пилюля с раскрывающимся чеклистом ─────────── */
function progHTML(){
  const n = DONE.filter(Boolean).length, m = WEEK_TASKS.length;
  const pct = m ? Math.round(n / m * 100) : 0;
  return '<div class="wk' + (WEEK_OPEN ? ' open' : '') + '">'
    + '<div class="wk-h" data-progtoggle>'
    + '<span class="pb-ic">' + (n ? ICONS._checkp : ICONS._circ) + '</span>'
    + '<span class="pb-n">' + n + ' of ' + m + '</span>'
    + '<span class="pb-track"><i style="width:' + pct + '%"></i></span>'
    + '<span class="pb-pct">' + pct + '%</span>'
    + '<span class="pb-chev">' + ICONS._chevd + '</span></div>'
    + (WEEK_OPEN ? '<div class="wk-list"><div class="branch">' + WEEK_TASKS.map(function(t, i){
        return '<div class="br-row" data-brtoggle="' + i + '">'
          + '<span class="br-dot' + (DONE[i] ? ' on' : '') + '">'
          + (DONE[i] ? ICONS._check2 : '') + '</span>'
          + '<span class="br-t' + (DONE[i] ? ' done' : '') + '">' + t[0]
          + (t[2] && !DONE[i] ? '<s>' + t[2] + '</s>' : '') + '</span>'
          + '<span class="br-m">' + t[1] + '</span></div>';
      }).join('') + '</div></div>' : '')
    + '</div>';
}
function renderWeek(){
  const pr = document.getElementById('homeprog'), tk = document.getElementById('hometasks');
  if(!pr) return;
  pr.innerHTML = progHTML();
  if(tk) tk.innerHTML = '';
  const w = document.getElementById('wkwid');
  if(w) w.innerHTML = MY_PLANTS.length
    ? '<div class="sl">At a glance</div>' + weekWidgets() : '';
}

/* ─────────── виджет-сетка дашборда (по референсу с карточками) ─────────── */
const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const SOW = new Date(2026, 2, 14);                       // 14 марта — день посева
function dayOffset(d){ const x = new Date(SOW); x.setDate(x.getDate() + d); return x; }
function arc(pct, sz, dark){
  const sw = 5, r = (sz - sw) / 2, c = 2 * Math.PI * r, off = c * (1 - Math.min(100, pct) / 100);
  return '<svg width="' + sz + '" height="' + sz + '" viewBox="0 0 ' + sz + ' ' + sz + '">'
   + '<circle cx="' + sz/2 + '" cy="' + sz/2 + '" r="' + r + '" fill="none" stroke="'
   + (dark ? 'rgba(255,255,255,.18)' : '#E4E8E2') + '" stroke-width="' + sw + '"/>'
   + '<circle cx="' + sz/2 + '" cy="' + sz/2 + '" r="' + r + '" fill="none" stroke="'
   + (dark ? '#B4F461' : '#22A559') + '" stroke-width="' + sw + '" stroke-linecap="round"'
   + ' stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '"'
   + ' transform="rotate(-90 ' + sz/2 + ' ' + sz/2 + ')"/></svg>';
}
function metricRow(items, dark){
  return '<div class="mrow">' + items.map(function(m){
    return '<div><s>' + m[0] + '</s><b>' + m[1] + '</b></div>';
  }).join('') + '</div>';
}
function calWidget(){
  // отмечаем: день посева, дни со снимками, дни готовности культур
  const marks = {};
  MY_PLANTS.forEach(function(p){
    p.photos.forEach(function(x){ marks[x.day] = marks[x.day] || 'photo'; });
    if(p.day >= p.c[2]) marks[p.c[2]] = 'pick';
  });
  marks[0] = 'sow';
  const today = MY_PLANTS.length ? Math.max.apply(null, MY_PLANTS.map(function(p){return p.day;})) : 0;
  let cells = '';
  for(let d = 0; d <= 34; d++){
    const m = marks[d], future = d > today;
    cells += '<i class="' + (m ? 'm-' + m : '') + (future ? ' fut' : '') + '">'
           + dayOffset(d).getDate() + '</i>';
  }
  return '<div class="wg wg-dark span2"><div class="wg-h"><b>Season calendar</b>'
    + '<s>' + MON[SOW.getMonth()] + ' \u2013 ' + MON[dayOffset(34).getMonth()] + '</s></div>'
    + '<div class="cal">' + cells + '</div>'
    + '<div class="callg"><span><i class="m-sow"></i>sown</span>'
    + '<span><i class="m-photo"></i>photo</span><span><i class="m-pick"></i>first pick</span></div></div>';
}
function weekWidgets(){
  if(!MY_PLANTS.length) return '';
  const st = seasonStats();
  const growing = MY_PLANTS.filter(function(p){ return p.day < p.c[2]; });
  const next = growing.length ? growing.reduce(function(a,b){
                 return (b.c[2]-b.day) < (a.c[2]-a.day) ? b : a; }) : null;
  return '<div class="wgrid">'
   + '<div class="wg wg-dark"><div class="wg-top"><div class="num">' + (next ? (next.c[2]-next.day) : 0)
   + '<span>d</span></div>' + arc(next ? pPct(next) : 100, 44, true) + '</div>'
   + '<div class="lbl">' + (next ? 'Until ' + next.c[0].toLowerCase() : 'All ready to pick') + '</div>'
   + metricRow([['Growing', growing.length], ['Ready', st.crops]]) + '</div>'
   + '<div class="wg wg-lite"><div class="wg-top"><div class="num">' + st.picks + '</div>'
   + arc(Math.min(100, st.picks * 12), 44, false) + '</div>'
   + '<div class="lbl">Harvests logged</div>'
   + metricRow([['Crops', st.crops], ['Photos', st.photos]]) + '</div>'
   + '</div>';
}
function seasonWidgets(){
  const st = seasonStats();
  const seasonPct = Math.min(100, Math.round(st.days / 187 * 100));
  return '<div class="wgrid">' + calWidget()
   + '<div class="wg wg-lite span2"><div class="wg-h"><b>Season progress</b><s>day ' + st.days
   + ' of 187</s></div><div class="pb-track" style="margin-top:12px;height:10px">'
   + '<i style="width:' + seasonPct + '%"></i></div>'
   + metricRow([['Sown', MON[SOW.getMonth()] + ' ' + SOW.getDate()],
                ['Today', 'day ' + st.days], ['Frost', 'Nov 28']]) + '</div>'
   + '</div>';
}

/* ─────────── GROWTH: дашборд + карточки культур с их фото ─────────── */
function seasonStats(){
  const harvested = MY_PLANTS.filter(p=>p.day >= p.c[2]);
  const picks = harvested.reduce((n,p)=>n + Math.max(1, Math.floor((p.day - p.c[2]) / 7) + 1), 0);
  return {picks: picks, crops: harvested.length, photos: allPhotos().length,
          days: MY_PLANTS.length ? Math.max.apply(null, MY_PLANTS.map(p=>p.day)) : 0};
}
function renderDash(){
  const el = document.getElementById('dash'); if(!el) return;
  const st = seasonStats();
  const sub = document.getElementById('seasonsub');
  if(sub) sub.textContent = MY_PLANTS.length
    ? 'Sown Mar 14 · day ' + st.days : 'Nothing sown yet';
  if(!MY_PLANTS.length){
    el.innerHTML = '<div class="note" style="margin-top:16px"><b>Your season starts with one seed</b>'
      + '<p>Add a plant and this page fills itself — harvests, photos, how long everything took.</p>'
      + '<div class="btn b-pri" data-go="add-plant">Add a plant</div></div>';
    return;
  }
  el.innerHTML = '<div class="acc dash"><div class="row1"><span class="tag">Season counter</span></div>'
    + '<div class="lbl">Harvests logged</div><div class="huge">' + st.picks + '</div>'
    + '<div class="sub">' + (st.crops
        ? st.crops + (st.crops===1?' crop has':' crops have') + ' reached the table. '
          + st.photos + (st.photos===1?' photo':' photos') + ' in the journal.'
        : 'Nothing ready yet — the first pick is the one that matters.') + '</div>'
    + '<div class="duo"><div class="cell"><s>Days</s><b>' + st.days + '</b></div>'
    + '<div class="cell"><s>Harvested</s><b>' + st.crops + (st.crops===1?' crop':' crops') + '</b></div>'
    + '<div class="cell"><s>Streak</s><b>11 wk</b></div></div></div>'
    + seasonWidgets();
}
function cropCard(p, i){
  const ready = p.day >= p.c[2];
  const picks = ready ? Math.max(1, Math.floor((p.day - p.c[2]) / 7) + 1) : 0;
  const strip = p.photos.length
    ? '<div class="cstrip">' + p.photos.slice(0,4).map(x=>
        '<div style="background-image:url(' + phUrl(x) + ')"></div>').join('')
      + (p.photos.length>4 ? '<div class="cmore">+' + (p.photos.length-4) + '</div>' : '') + '</div>'
    : '<div class="cempty" data-shoot="' + i + '">' + ICONS._cam + '<span>No photos yet — take one</span></div>';
  return '<div class="ccard"><div class="chead" data-open="' + i + '">'
    + '<div class="rw">' + ringSVG(pPct(p)) + '<i>' + ICONS[p.c[1]] + '</i></div>'
    + '<div class="nm"><b>' + p.c[0] + '</b><s>'
    + (ready ? picks + (picks===1?' harvest':' harvests') + ' · day ' + p.day
             : 'Day ' + p.day + ' · ' + pStage(p) + ' · ' + pEta(p))
    + '</s></div>' + ICONS._chev + '</div>' + strip + '</div>';
}
function renderCropCards(){
  const el = document.getElementById('cropcards'); if(!el) return;
  if(!MY_PLANTS.length){ el.innerHTML=''; return; }
  const ready = [], growing = [];
  MY_PLANTS.forEach((p,i)=>(p.day >= p.c[2] ? ready : growing).push([p,i]));
  let h = '';
  if(ready.length)   h += '<div class="sl">Made it to the table</div>'
                          + ready.map(x=>cropCard(x[0],x[1])).join('');
  if(growing.length) h += '<div class="sl">Still growing</div>'
                          + growing.map(x=>cropCard(x[0],x[1])).join('');
  h += addPhotoBtn();
  el.innerHTML = h;
}

function checkWeekDone(){
  if(DONE.filter(Boolean).length === WEEK_TASKS.length) setTimeout(function(){{ go('week-done'); }}, 600);
}
function renderAll(){ renderHome(); renderPlants(); renderDetail(); renderJournal();
                      try{ renderDash(); renderCropCards(); }catch(e){}
                      try{ renderLock(); renderSettingsPlan(); }catch(e){} }

const SUNLABEL = {
 '3\u20135 hours':'3\u20135 hours of sun', '6\u20138 hours':'6\u20138 hours of sun',
 '8+ hours':'8+ hours of sun', 'Not sure yet':'a safe 3\u20135 hours until you check',
 'South':'a south-facing window', 'East or West':'an east or west window',
 'North':'a north window', 'Not sure':'a cautious low-light start'};
const GOALWORD = {salads:'salads', herbs:'herbs', fast:'a fast first harvest',
 tomatoes:'tomatoes', peppers:'peppers', beans:'beans', roots:'root crops', kids:'a kid project'};
const SUNNEED = {tomatoes:'6\u20138 hours', peppers:'6\u20138 hours', beans:'6\u20138 hours'};
const SUNRANK = {'3–5 hours':1,'6–8 hours':2,'8+ hours':3,'Not sure yet':1,
                 'South':2,'East or West':1,'North':1,'Not sure':1};
const GOALTAG = {'Salads & greens':'salads','Fresh herbs':'herbs','Fast first harvest':'fast',
                 'Tomatoes':'tomatoes','Peppers':'peppers','Beans & peas':'beans',
                 'Roots: radish, carrot':'roots','Kid-friendly project':'kids'};
function recordChoice(scr, label){
  if(scr==='s-q1'){ CHOICES.space = label.toLowerCase().indexOf('windowsill')>-1 ? 'a windowsill' : 'a '+label.toLowerCase();
                    CHOICES.indoor = label.indexOf('Windowsill')>-1; }
  if(scr==='s-q3'||scr==='s-q2i'){ CHOICES.sun = SUNLABEL[label] || 'your light';
                    CHOICES.sunRank = SUNRANK[label]||1; }
  if(scr==='s-q5'){ CHOICES.effort = label.indexOf('10')>-1?3:label.indexOf('20')>-1?4:5; }
}
'''

ICON_JS = {n: ic(n, 'var(--primary)', 15, '1.9') for n in ICONSET}
ICON_JS['_plus'] = ic('plus', 'var(--primary)', 17, '2.4')
ICON_JS['_check'] = ic('check', '#fff', 17, '3')
ICON_JS['_check2'] = ic('check', '#fff', 16, '3')
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


# ═════════════════════════════ ДОКУМЕНТ ФЛОУ
FLOWS = [
 ("1 · Первый заход", "От лендинга до первой отмеченной задачи. Цель — 90 секунд и пять вопросов.", [
  ("Landing", "Фото на весь экран, один заголовок, одна кнопка.",
   "Ничего не считает. Ждёт тапа.",
   "Q1", "Логина нет — в спеке он на лендинге не предусмотрен, возврат идёт по ссылке из письма. "
         "Никаких попапов и cookie-модалок поверх первого экрана."),
  ("Q1 · Space", "Восемь пространств. Ни одно не выбрано заранее.",
   "Пишет space.type. От него зависят объём контейнера, предупреждения о дренаже и набор культур.",
   "Q2 · либо Q3-indoor, если выбран Windowsill",
   "Windowsill — единственная развилка онбординга. Она уводит в трек без сезона."),
  ("Q2 · ZIP", "Пустое поле-плейсхолдер, Continue выключен.",
   "После ввода резолвит ZIP в climate_profile: даты заморозков, длина сезона, зона USDA. "
   "Показывает результат карточкой — подтверждение, что система что-то узнала.",
   "Q3", "ZIP не найден → выбор штата и ближайшего города. Онбординг не блокируем никогда."),
  ("Q3 · Sun", "Четыре варианта светового бюджета.",
   "Пишет sun_bucket — главный фильтр качества плана. Плодовым нужно 6-8 ч, листовым хватает 3-5.",
   "Q4", "«Not sure» → назначаем 3-5 как безопасный вариант и добавляем задачу Sun check в первую неделю."),
  ("Q3-indoor · Window", "Сторона окна вместо часов солнца.",
   "South → ранг 2, East/West и North → ранг 1. Ложится в тот же sun_bucket, движок не переписывается.",
   "Q4", "Новый экран, которого нет в спеке. Следствие усиления indoor-трека."),
  ("Q4 · Goals", "Мультивыбор, максимум три. Ничего не выбрано заранее.",
   "Пишет plan.goals. При достижении лимита остальные гаснут, а не исчезают.",
   "Q5", "Если цель конфликтует со светом — не отказываем, а честно объясняем на Plan Preview."),
  ("Q5 · Effort", "Три уровня усилия.",
   "Пишет effort_level: 3 / 4 / 5-6 культур и 3 / 5 / 7 задач в неделю. "
   "Интерфейс всё равно показывает максимум 5, остальное под «+2 more».",
   "Plan Preview", "Вопросов об опыте садоводства нет — они не нужны движку и увеличивают отвал."),
  ("Plan Preview", "План собран: культуры, контейнеры, дата первого сбора, блок «почему».",
   "Прогоняет мини-движок: фильтр по свету → скоринг по целям → лимиты состава "
   "(минимум одна культура до 35 дней, максимум две дольше 70).",
   "Save Plan", "Ключевое решение продукта: план показывается ДО регистрации. "
                "Эндпоинт /api/onboarding/preview работает без авторизации."),
  ("Save Plan", "Фото на весь экран, Google или email.",
   "Создаёт User, привязывает план. Пароля нет — magic link.",
   "Paywall", "Регистрация только после того, как ценность показана."),
  ("Paywall", "Тёмный экран, Season pass предвыбран, триал без карты.",
   "Ничего не блокирует. Закрывается в тот экран, откуда пришёл.",
   "Home", "⚠ Показ сразу после регистрации — решение заказчика. Спека §10.4 это запрещает "
           "(never_before_first_task = true). Риск: отвал до первой ценности."),
 ]),
 ("2 · Недельный цикл", "То, ради чего продукт существует. 80% времени пользователя.", [
  ("Home · пусто", "Акцентный блок зовёт добавить растение. Ниже — единственная задача: купить контейнеры.",
   "MY_PLANTS пуст. Экран знает это и меняется целиком.",
   "Add a plant", "Пустой экран не должен быть пустым: он продаёт ближайшее будущее."),
  ("Add a plant", "Поиск по 21 культуре, группы «быстрые» и «долгие», внизу — то, чему не хватает света.",
   "Фильтрует по sun_bucket. Выбранное копится в корзине, счётчик растёт. "
   "Кнопка пишет, сколько именно добавится.",
   "Home", "Добавил одно — появится одно. Неподходящие культуры показаны и погашены, а не спрятаны."),
  ("Home · есть растения", "Тот же акцентный блок, внутри растения с кольцами. Ниже — задачи недели.",
   "Кольцо = день / days_to_harvest_min. Стадия считается детерминированно, а не со слов пользователя.",
   "Plant detail · Week complete", "Задачи текущей недели всегда бесплатны — это ядро обещания."),
  ("Отметка задачи", "Один тап, без подтверждения. Прогресс-бар двигается.",
   "task.status = done → пересчёт стадии → обновление streak → проверка OFF-05.",
   "Week complete, если отмечены все", "Просроченная задача не красная и не имеет жёсткого дедлайна."),
  ("Week complete", "Тёмный экран с фото, стрик, предложение Pro.",
   "success_modal. Частота — не чаще раза в 7 дней.",
   "Paywall или Home", "Оффер привязан к моменту успеха, а не к блокировке."),
 ]),
 ("3 · Растения", "Управление составом плана.", [
  ("Plants", "Список с кольцами. У каждой строки крестик.",
   "Рендерится из MY_PLANTS. Показывает, сколько из трёх бесплатных слотов занято.",
   "Plant detail", "Удаление доступно всегда — растения гибнут, это часть процесса."),
  ("Удаление", "Крестик убирает строку, снизу всплывает «Undo» на 4.5 секунды.",
   "Растение удаляется из состояния, но хранится в буфере отмены вместе с позицией.",
   "остаётся на Plants", "Провал не должен быть страшным. §23.1 запрещает обвинять пользователя."),
  ("Plant detail", "Фото, кольцо, полоса «типичный диапазон», timeline, история задач.",
   "Полоса строится из days_to_harvest_min/max, точка — фактический день.",
   "Harvest, если созрело", "Нет фото → вместо пустых серых квадратов стоит плитка «Add a photo»."),
 ]),
 ("4 · Урожай и сезон", "Пик удержания и главный источник органики.", [
  ("Harvest Moment", "Тёмный экран, настоящее фото, «First harvest. Day 31».",
   "Создаёт Harvest, помечает is_first_of_plan, проверяет OFF-06.",
   "Growth", "Единственный момент, когда пользователь получает физическое доказательство."),
  ("Growth · дашборд", "Счётчик сезона в акцентном блоке: сборы, дни, культуры, стрик. Ниже журнал.",
   "Считает по §9.4. Эти же четыре цифры в конце сезона становятся Season Recap.",
   "Paywall при 6-м фото", "Нет фото → блок «Take one photo today», а не пустая сетка."),
 ]),
 ("5 · Indoor", "Ветка, которая закрывает сезонность.", [
  ("Indoor · Home", "«Season ends: never». Ритм — срез каждую неделю.",
   "Нет first_frost, нет horizon_weeks. Вместо дней до урожая — счётчик срезов и время до следующего.",
   "тот же цикл", "Нужны поля cut_count и regrow_days, которых в спеке нет."),
 ]),
 ("6 · Точки оффера", "Видно часто, давления нет.", [
  ("Баннер над навигацией", "Лаймовая полоса, не перекрывает контент, не требует закрытия.",
   "persistent_line. Видна всегда.",
   "Paywall", "Около 90% всех показов оффера приходится на неперекрывающие форматы."),
  ("Soft-lock недели +2", "Задачи размыты, но количество и даты видны.",
   "Показывает, что за платой стоит реальный контент, а не пустота.",
   "Paywall", "Это не стена. §10.3."),
  ("Лимит культур", "Четвёртая культура упирается в блок «That\u2019s the free limit».",
   "Не отказ: культура добавляется визуально и помечается is_premium.",
   "Paywall", "Мы не блокируем то, что человек уже начал."),
  ("Anti-annoyance", "Если модалку показывать нельзя, оффер деградирует в inline, а не исчезает.",
   "max 1 модалка в 7 дней, 2 закрытия подряд → только inline, 5 → только баннер и Settings.",
   "—", "Если session-drop после показа > 10%, частота падает до 1 раза в 14 дней автоматически."),
 ]),
]

# ═════════════════════════════ СБОРКА
GROUPS = ['Онбординг', 'Home', 'Plants', 'Growth', 'Деньги', 'Система', 'Indoor']
HOME_NEW_GONE = True
FLOW = """
<b>Основной путь.</b> <code>landing</code> → пять вопросов → <code>preview</code> (план виден без регистрации)
→ <code>save</code> → <code>home-new</code> → добавил растение → <code>home</code> → чекает задачи →
<code>week-done</code> → <code>paywall</code><br>
<b>Ветка indoor.</b> В <code>q1</code> выбор «Windowsill» уводит в <code>q2i</code> — вопрос о стороне окна вместо
часов солнца. Дальше тот же поток, но конца сезона нет.<br>
<b>Ветка урожая.</b> <code>plant</code> → «Harvest it» → <code>harvest</code> → <code>growth</code>.<br>
<b>Ветки оффера.</b> <code>week-lock</code> (soft-lock недели +2), <code>add-plant</code> (лимит культур),
журнал на 6-м фото, <code>week-done</code> — все ведут в <code>paywall</code>, и все закрываются в <code>home</code>.
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
       '<button class="chip" data-demo="seed">Заполнить — 4 растения</button></div></div>')
for g in GROUPS:
    items = [s for s in SCR if s['group'] == g]
    if not items: continue
    idx += f'<div class="grp"><div class="gt">{g}</div><div class="chips">' + ''.join(
        f'<button class="chip" data-go="{s["id"]}">{s["title"]}</button>' for s in items) + '</div></div>'

toks = '<div class="tok">' + ''.join(
    f'<div class="tk"><i style="background:{hx}"></i><b>{hx}</b><s>{lbl}</s></div>'
    for v, hx, lbl in TOKENS) + '</div>'

import json
JS_EXTRA = JS_SRC.replace('__ICONS__', json.dumps(ICON_JS, ensure_ascii=False)).replace('__CROPS__', json.dumps(CROPS, ensure_ascii=False))
HTML = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>HOMEGROWN — прототип</title>
<style>{CSS}</style></head><body>
<div class="stage">
  <div class="stage-bar"><span class="t" id="scr-title">Landing</span><span class="s" id="scr-id">landing</span></div>
  <div class="phone">{screens_html}<div id="toast"></div><input id="cam" type="file" accept="image/*" capture="environment" hidden></div>
  <div class="hint" id="scr-note"></div>
</div>
<div class="side">
  <div style="font-size:11.5px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)">
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
function go(id){{
  const el = document.getElementById('s-'+id); if(!el) return;
  if(id==='paywall'){{ const cur=document.querySelector('.screen.on');
    PW_FROM = (cur && cur.id==="s-save") ? "home" : (cur? cur.id.slice(2):'home');
    if(PW_FROM==='paywall') PW_FROM='home'; }}
  document.querySelectorAll('.screen.on').forEach(s=>s.classList.remove('on'));
  resetScreen(id);
  if(id==='preview') try{{ renderPreview(); }}catch(e){{}}
  if(id==='add-plant'){{ const q=document.getElementById('cropq'); if(q){{q.value='';
      q.parentElement.classList.remove('has');}} PENDING=[]; renderCrops(''); }}
  if(id==='home') renderHome();
  if(id==='plants') renderPlants();
  if(id==='week-empty'){{ const w=document.getElementById('wkplants');
    if(w) w.innerHTML='<div class="plist">'+MY_PLANTS.map((p,i)=>
      '<div class="pl" data-open="'+i+'"><div class="rw">'+ringSVG(pPct(p))+'<i>'+ICONS[p.c[1]]+'</i></div>'
      +'<div class="nm"><b>'+p.c[0]+'</b><s>Day '+p.day+' &middot; '+pStage(p)+'</s></div>'
      +'<div class="eta">'+pEta(p)+'</div></div>').join('')+'</div>'; }}
  if(id==='plant') renderDetail();
  if(id==='growth'){{ renderDash(); renderCropCards(); }}
  if(id==='week-lock') renderLock();
  if(id==='settings') renderSettingsPlan();
  el.classList.add('on'); el.querySelectorAll('.bd').forEach(b=>b.scrollTop=0);
  el.querySelectorAll('.dark,.overlay').forEach(b=>b.scrollTop=0);
  document.querySelectorAll('.chip').forEach(c=>c.classList.toggle('act', c.dataset.go===id));
  const n = NOTES[id]||['',''];
  document.getElementById('scr-title').textContent = n[0];
  document.getElementById('scr-id').textContent = id;
  document.getElementById('scr-note').innerHTML = n[1];
  history.replaceState(null,'','#'+id);
}}
const MAXG = 3, MAXP = 3;
function resetScreen(id){{
  const el = document.getElementById('s-'+id); if(!el) return;
  el.querySelectorAll('.opt').forEach(o=>o.classList.remove('sel','dim'));
  el.querySelectorAll('.pl').forEach(o=>o.classList.remove('added','locked'));
  el.querySelectorAll('[data-cta]').forEach(b=>b.classList.add('off'));
  const z = el.querySelector('[data-zip]');
  if(z){{ z.textContent='— — — — —'; z.classList.add('ph');
          el.querySelector('[data-zipres]').style.display='none'; }}
  const c = el.querySelector('[data-count]'); if(c) c.textContent='nothing selected yet';
  const h = el.querySelector('[data-hint]'); if(h) h.textContent='Pick at least one.';
  const ac = el.querySelector('[data-addcount]'); if(ac) ac.textContent='0 of 3 chosen';
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
document.addEventListener('click', e=>{{
  const single = e.target.closest('[data-single]');
  if(single){{
    single.parentElement.querySelectorAll('.opt').forEach(o=>o.classList.remove('sel'));
    single.classList.add('sel');
    try{{ recordChoice(single.closest('.screen').id, single.querySelector('div').childNodes[0].textContent.trim()); }}catch(e){{}}
    const nx = single.dataset.next;
    if(nx && nx!=='None') setTimeout(()=>go(nx), 300);
    return;
  }}
  const multi = e.target.closest('[data-multi]');
  if(multi){{
    const wrap = multi.parentElement;
    if(multi.classList.contains('sel')) multi.classList.remove('sel');
    else if(wrap.querySelectorAll('.opt.sel').length < MAXG) multi.classList.add('sel');
    syncMulti(wrap);
    CHOICES.goals = Array.from(wrap.querySelectorAll('.opt.sel'))
      .map(o=>GOALTAG[o.querySelector('div').childNodes[0].textContent.trim()]).filter(Boolean);
    return;
  }}
  const zip = e.target.closest('[data-zip]');
  if(zip){{
    zip.textContent='78704'; zip.classList.remove('ph');
    const scr = zip.closest('.screen');
    scr.querySelector('[data-zipres]').style.display='block';
    scr.querySelector('[data-cta]').classList.remove('off'); return;
  }}
  const t = e.target.closest('[data-task]');
  if(t){{ t.classList.toggle('done'); sync(t.closest('.bd')); return; }}
  const seg = e.target.closest('[data-seg]');
  if(seg){{ seg.parentElement.querySelectorAll('div').forEach(d=>d.classList.remove('on'));
           seg.classList.add('on'); price(seg); return; }}
  const pick = e.target.closest('[data-pick]');
  if(pick){{ pick.parentElement.querySelectorAll('.opt').forEach(o=>o.classList.remove('sel'));
            pick.classList.add('sel'); return; }}
  if(e.target.closest('[data-progtoggle]')){{ WEEK_OPEN = !WEEK_OPEN; renderWeek(); return; }}
  const br = e.target.closest('[data-brtoggle]');
  if(br){{ const i = +br.dataset.brtoggle; DONE[i] = !DONE[i]; renderWeek(); checkWeekDone(); return; }}
  const wt = e.target.closest('[data-wtask]');
  if(wt){{ const i = +wt.dataset.wtask; DONE[i] = !DONE[i]; renderWeek(); checkWeekDone(); return; }}
  if(e.target.closest('[data-addphoto]')){{ openCamera(); return; }}
  const sh = e.target.closest('[data-shoot]');
  if(sh){{ openCamera(+sh.dataset.shoot); return; }}
  if(e.target.closest('[data-gogrowth]')){{ document.getElementById('toast').classList.remove('on');
                                            go('growth'); return; }}
  if(e.target.closest('[data-buy]')){{ buyPro(); return; }}
  if(e.target.closest('[data-unpro]')){{ dropPro(); return; }}
  const tg = e.target.closest('.tgl');
  if(tg){{ const on = tg.classList.toggle('on');
           tg.setAttribute('aria-checked', on ? 'true' : 'false'); return; }}
  if(e.target.closest('[data-undo]')){{ undoRemove(); return; }}
  const del = e.target.closest('[data-del]');
  if(del){{ removePlant(+del.dataset.del); return; }}
  if(e.target.closest('[data-remove]')){{ removePlant(SELECTED); go('plants'); return; }}
  const op = e.target.closest('[data-open]');
  if(op){{ SELECTED = +op.dataset.open; renderDetail(); go('plant'); return; }}
  const ad = e.target.closest('[data-add]');
  if(ad){{ const n = ad.dataset.crop; const k = PENDING.indexOf(n);
    if(k>-1) PENDING.splice(k,1);
    else if(MY_PLANTS.length+PENDING.length < limit()) PENDING.push(n);
    else {{ const lim=document.querySelector('#s-add-plant [data-limit]'); if(lim) lim.style.display='block'; return; }}
    renderCrops(document.getElementById('cropq').value); return; }}
  const cta = e.target.closest('#s-add-plant [data-cta]');
  if(cta && !cta.classList.contains('off')){{
    PENDING.forEach(n=>MY_PLANTS.push(mk(n, 0, []))); PENDING=[]; renderAll(); go('home'); return; }}
  if(e.target.closest('[data-pw-exit]')){{ go(PW_FROM); return; }}
  const g = e.target.closest('[data-go]');
  if(g){{ go(g.dataset.go); }}
}});
function sync(bd){{
  if(!bd) return;
  const all = bd.querySelectorAll('[data-task]'), done = bd.querySelectorAll('[data-task].done');
  const bar = bd.querySelector('.bar i'), pct = bd.querySelector('.pct');
  if(bar) bar.style.width = (all.length? done.length/all.length*100:0)+'%';
  if(pct) pct.textContent = done.length+' of '+all.length+' done';
  if(all.length && done.length===all.length && bd.closest('#s-home')) setTimeout(()=>go('week-done'), 550);
}}
function price(seg){{
  const card = seg.closest('.dark').querySelector('.pcard');
  const yearly = seg.textContent.indexOf('Season')>-1;
  card.querySelector('.pr').innerHTML = yearly
    ? '$29<span style="font-size:15px;font-weight:500;color:#A9BCB0"> / year</span>'
    : '$4.99<span style="font-size:15px;font-weight:500;color:#A9BCB0"> / month</span>';
  card.querySelector('.pn').textContent = yearly
    ? 'Cheaper than one tray of seedlings. Covers a full season, start to frost.'
    : 'Month to month. A season runs about seven of these.';
  card.querySelector('.pill').style.display = yearly ? '' : 'none';
}}
document.addEventListener('input', e=>{{
  if(e.target.id==='cropq'){{ e.target.parentElement.classList.toggle('has', !!e.target.value);
                              renderCrops(e.target.value); }}
}});
document.addEventListener('click', e=>{{
  if(e.target.closest('#cropx')){{ const q=document.getElementById('cropq');
    q.value=''; q.parentElement.classList.remove('has'); renderCrops(''); q.focus(); }}
}});
document.addEventListener('click', e=>{{
  const d = e.target.closest('[data-demo]');
  if(d){{ if(d.dataset.demo==='empty') MY_PLANTS=[]; else seedPlants();
          PENDING=[]; SELECTED=0; renderAll(); go('home'); }}
}});
(function(){{ const c=document.getElementById('cam');
  if(c) c.addEventListener('change', function(){{ attachShot(c.files && c.files[0]); }});
}})();
seedPlants(); renderAll(); renderLock(); renderSettingsPlan();
document.addEventListener('keydown', e=>{{
  if((e.key===' '||e.key==='Enter') && e.target.classList && e.target.classList.contains('tgl')){{
    e.preventDefault(); e.target.click(); }}
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
  opacity:0;transform:translateY(16px);pointer-events:none;transition:.26s}
#a2hs.on{opacity:1;transform:none;pointer-events:auto}
.a2-card{background:var(--lime);border-radius:24px;padding:16px;display:flex;align-items:flex-end;
  gap:12px;box-shadow:0 16px 36px rgba(11,31,20,.34)}
.a2-txt{flex:1;min-width:0}
.a2-pill{display:inline-block;background:var(--deepest);color:var(--lime);border-radius:999px;
  padding:6px 12px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.a2-h{display:block;font-size:24px;font-weight:700;line-height:1.06;letter-spacing:-.02em;
  color:var(--deepest);margin-top:8px}
#a2hs s{display:block;font-size:12.5px;color:#2C4A1E;text-decoration:none;margin-top:6px;
  font-weight:600;opacity:.78}
.a2-act{display:flex;align-items:center;gap:8px;flex:none}
#a2btn{background:var(--deepest);color:var(--lime);border:0;border-radius:999px;height:44px;padding:0 20px;
  font:700 15px 'Inter Tight',sans-serif;cursor:pointer}
#a2x{width:44px;height:44px;border-radius:50%;background:rgba(11,31,20,.12);display:flex;align-items:center;
  justify-content:center;font-size:22px;color:var(--deepest);flex:none;cursor:pointer;line-height:1}
body.a2-open .bd{padding-bottom:172px}
body.a2-open #toast{bottom:calc(196px + env(safe-area-inset-bottom))}

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
#toast{bottom:calc(160px + env(safe-area-inset-bottom))}
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
 '<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,'
 'user-scalable=no,viewport-fit=cover">\n'
 '<link rel="manifest" href="manifest.webmanifest">\n'
 '<meta name="theme-color" content="#F2F4F0">\n'
 '<meta name="mobile-web-app-capable" content="yes">\n'
 '<meta name="apple-mobile-web-app-capable" content="yes">\n'
 '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
 '<meta name="apple-mobile-web-app-title" content="HOMEGROWN">\n'
 '<link rel="apple-touch-icon" href="img/apple-touch-icon.png">\n'
 '<link rel="icon" href="img/icon-192.png">\n'
 '<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/Caprasimo-400-latin.woff2">\n'
 '<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/InterTight-400-latin.woff2">')

MOBILE = HTML
assert '<title>HOMEGROWN — прототип</title>' in MOBILE
MOBILE = MOBILE.replace('<title>HOMEGROWN — прототип</title>', PWA_HEAD)
MOBILE = MOBILE.replace('</style>', MOBILE_CSS + '</style>')
MOBILE = MOBILE.replace('<div class="phone">', '<div class="mob">')
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
  './', './index.html', './manifest.webmanifest',
  './img/hero.jpg', './img/garden.jpg', './img/radish.jpg', './img/basil.jpg',
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
.top{{font-size:11.5px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)}}
h1{{font-family:Caprasimo;font-size:44px;line-height:1.04;margin:8px 0 12px;font-weight:400}}
.intro{{font-size:16px;color:var(--ink-2);max-width:760px;line-height:1.6}}
section{{margin-top:44px}}
h2{{font-size:22px;font-weight:600;letter-spacing:-.01em}}
.lede{{font-size:14.5px;color:var(--muted);margin:4px 0 16px}}
table{{width:100%;border-collapse:collapse;background:var(--surface);border-radius:16px;overflow:hidden}}
th{{text-align:left;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
   color:var(--muted);padding:16px 16px;background:#EAEEE8}}
td{{padding:16px 16px;font-size:14.5px;vertical-align:top;border-top:1px solid var(--hair)}}
.c1{{width:152px}}.c4{{width:180px;color:var(--primary);font-weight:600}}
tr.nt td{{border-top:0;padding-top:0;font-size:13.5px;color:var(--ink-2);background:#FAFBF9}}
tr.nt td:last-child:before{{content:"↳ ";color:var(--muted)}}
.legend{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
.lg{{background:var(--surface);border-radius:16px;padding:12px 16px;font-size:13.5px;flex:1;min-width:240px}}
.lg b{{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}
</style></head><body>
<div class="top">HOMEGROWN · пользовательский флоу · {len(SCR)} экранов</div>
<h1>Что будет и как будет</h1>
<div class="intro">Каждый шаг разложен на четыре вещи: что человек видит, что в этот момент делает система,
куда его ведёт дальше и что важно не сломать. Стрелкой отмечены пометки — правила из продуктовой спеки
и места, где я от неё отступил.</div>
<div class="legend">
  <div class="lg"><b>Развилка</b>Windowsill в Q1 уводит в indoor-трек: другой вопрос о свете, план без конца сезона.</div>
  <div class="lg"><b>Единственный запрет</b>Ничего не блокируем из того, что человек уже начал делать.</div>
  <div class="lg"><b>Отступление от спеки</b>Пэйволл сразу после регистрации — против §10.4. Помечено ⚠ в таблице.</div>
</div>
{flow_body}
</body></html>"""
(DIR / 'flow.html').write_text(FLOW_HTML, encoding='utf-8')

print('index.html (mobile):', len(MOBILE), '| review.html:', len(HTML), '| flow.html:', len(FLOW_HTML),
      '| screens:', len(SCR))
