// Мелкие переиспользуемые куски. Все SVG-формулы перенесены из proto.py как есть:
// кольцо рисуется на SVG, а не conic-gradient, потому что conic не умеет
// круглые концы.

import type { ReactNode } from 'react'
import { Icon, IcBig } from '../icons/Icon'
import { bg } from '../lib/assets'
import type { Species } from '../data/species'

/** Кольцо прогресса, светлый и тёмный вариант. Повторяет ring() из proto.py. */
export function Ring({ pct, dark = false, sz = 38, sw = 3.2 }:
                     { pct: number; dark?: boolean; sz?: number; sw?: number }) {
  const r = (sz - sw) / 2
  const circ = 2 * Math.PI * r
  const off = circ * (1 - Math.max(0, Math.min(100, pct)) / 100)
  return (
    <svg aria-hidden="true" width={sz} height={sz} viewBox={`0 0 ${sz} ${sz}`}>
      <circle cx={sz / 2} cy={sz / 2} r={r} fill="none"
              stroke={dark ? 'rgba(255,255,255,.20)' : '#DDE3DC'} strokeWidth={sw} />
      <circle cx={sz / 2} cy={sz / 2} r={r} fill="none"
              stroke={dark ? 'var(--lime)' : 'var(--bright)'} strokeWidth={sw}
              strokeLinecap="round" strokeDasharray={circ.toFixed(1)}
              strokeDashoffset={off.toFixed(1)}
              transform={`rotate(-90 ${sz / 2} ${sz / 2})`} />
    </svg>
  )
}

/** Дуга для виджетов. arc() из proto.py. */
export function Arc({ pct, sz, dark }: { pct: number; sz: number; dark?: boolean }) {
  const sw = 5
  const r = (sz - sw) / 2
  const c = 2 * Math.PI * r
  const off = c * (1 - Math.min(100, pct) / 100)
  return (
    <svg aria-hidden="true" width={sz} height={sz} viewBox={`0 0 ${sz} ${sz}`}>
      <circle cx={sz / 2} cy={sz / 2} r={r} fill="none"
              stroke={dark ? 'rgba(255,255,255,.18)' : '#E4E8E2'} strokeWidth={sw} />
      <circle cx={sz / 2} cy={sz / 2} r={r} fill="none"
              stroke={dark ? '#B4F461' : '#22A559'} strokeWidth={sw} strokeLinecap="round"
              strokeDasharray={c.toFixed(1)} strokeDashoffset={off.toFixed(1)}
              transform={`rotate(-90 ${sz / 2} ${sz / 2})`} />
    </svg>
  )
}

/** Большое кольцо на тёмном (health score). ringBig() из proto.py. */
export function RingBig({ pct, sz }: { pct: number; sz: number }) {
  const sw = 6
  const r = (sz - sw) / 2
  const c = 2 * Math.PI * r
  const off = c * (1 - pct / 100)
  return (
    <svg aria-hidden="true" width={sz} height={sz} viewBox={`0 0 ${sz} ${sz}`}>
      <circle cx={sz / 2} cy={sz / 2} r={r} fill="none" stroke="rgba(255,255,255,.16)" strokeWidth={sw} />
      <circle cx={sz / 2} cy={sz / 2} r={r} fill="none" stroke="var(--lime)" strokeWidth={sw}
              strokeLinecap="round" strokeDasharray={c.toFixed(1)} strokeDashoffset={off.toFixed(1)}
              transform={`rotate(-90 ${sz / 2} ${sz / 2})`} />
    </svg>
  )
}

export function MetricRow({ items }: { items: Array<[string, ReactNode]> }) {
  return (
    <div className="mrow">
      {items.map(([k, v], i) => <div key={i}><s>{k}</s><b>{v}</b></div>)}
    </div>
  )
}

/** Фон плитки вида: настоящий снимок либо тёмный градиент под иконку. */
export const photoStyle = (s: Species): React.CSSProperties =>
  s.img
    ? { backgroundImage: bg(s.img) }
    : { background: 'linear-gradient(150deg,#17683C 0%,#0F3A24 60%,#0B1F14 100%)' }

/**
 * Плитка вида. Если у вида нет настоящей фотографии — рисуем плитку с иконкой,
 * а не битую картинку. Выдумывать ассеты нельзя.
 */
export function PhotoTile({ s, cls, style, children }:
    { s: Species; cls: string; style?: React.CSSProperties; children?: ReactNode }) {
  return (
    <div className={cls + (s.img ? '' : ' no-ph')} style={{ ...photoStyle(s), ...style }}>
      {!s.img && <span className="ph-ic"><IcBig name={s.icon} /></span>}
      {children}
    </div>
  )
}

/** Круглая миниатюра вида для списков. */
export function SpThumb({ s }: { s: Species }) {
  return s.img
    ? <div className="spic has" style={{ backgroundImage: bg(s.img) }} />
    : <div className="spic"><Icon name={s.icon} color="var(--primary)" size={15} sw={1.9} /></div>
}

export function Note({ title, children, cta, mt = 16 }:
                     { title: string; children?: ReactNode; cta?: ReactNode; mt?: number }) {
  // Отступ сверху в прототипе проставлен по месту, а не один на все вызовы:
  // в пустой ветке week-back его нет вовсе.
  return (
    <div className="note" style={{ marginTop: mt }}>
      <b>{title}</b>
      {children && <p>{children}</p>}
      {cta}
    </div>
  )
}

export function SectionLabel({ children }: { children: ReactNode }) {
  return <div className="sl">{children}</div>
}

export function Tappable({ cls, onClick, children, label, style }:
    { cls: string; onClick?: () => void; children: ReactNode; label?: string; style?: React.CSSProperties }) {
  return (
    <div className={cls} role="button" tabIndex={0} aria-label={label} style={style}
         onClick={onClick}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onClick?.() } }}>
      {children}
    </div>
  )
}
