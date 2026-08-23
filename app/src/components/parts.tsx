// Части, которые появились вместе с остальными 25 экранами.
// Разметка повторяет proto.py буквально: перенесённый CSS рассчитывает
// на те же имена классов и ту же вложенность.

import { useEffect, useRef, type ReactNode } from 'react'
import { Icon, IcCheck2, IcCheckG, IcChev } from '../icons/Icon'
import { useStore } from '../state/store'
import { STEPS } from '../data/onboarding'

/** Опция онбординга. Ни одна не выбрана заранее — состояние появляется от тапа. */
export function Opt({ label, sub, on, multi, dim, onPick }:
    { label: string; sub?: string | null; on?: boolean; multi?: boolean
      dim?: boolean; onPick: () => void }) {
  return (
    <div className={'opt' + (on ? ' sel' : '') + (dim ? ' off' : '')}
         role={multi ? 'checkbox' : 'radio'} tabIndex={0} aria-checked={!!on}
         onClick={onPick}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onPick() } }}>
      <div>{label}{sub && <s>{sub}</s>}</div>
      <div className="opt-tick"><Icon name="check" color="#fff" size={14} sw={3} /></div>
    </div>
  )
}

/* Подвал больше не отдельный компонент: он обязан быть соседом .bd, а не его
   потомком, поэтому живёт пропом foot у Screen — см. components/Chrome.tsx. */

/** Точки прогресса. Путь зависит от ветки онбординга и от того, улица или дом. */
export function Pg({ id }: { id: string }) {
  const { s } = useStore()
  const key = (s.onbMode === 'own' ? 'own_' : 'plan_') + (s.choices.outdoor ? 'out' : 'in')
  const path = STEPS[key]
  const k = path.indexOf(id)
  if (k < 0) return <div className="pg" />
  return (
    <div className="pg">
      {path.map((_, i) => <i key={i} className={i <= k ? 'on' : undefined} />)}
    </div>
  )
}

/** Тёмный полноэкранный блок: paywall, milestone, recap, week complete, scan. */
export function Dark({ id, children, className = 'dark', style }:
    { id: string; children: ReactNode; className?: string; style?: React.CSSProperties }) {
  return <div className={'screen on'} id={'s-' + id}>
    <div className={className} style={style}>{children}</div>
  </div>
}

export function Task({ t, done, onToggle, locked, bars }:
    { t: [string, string, string?]; done?: boolean; onToggle?: () => void; locked?: boolean
      bars?: number[] }) {
  if (locked) {
    // Ширины полос задаёт вызывающий: у трёх строк soft-lock они разные, и
    // одинаковый скелетон читается как три копии одной задачи.
    const w = bars || [76, 52]
    return (
      <div className="task">
        <div className="box" />
        <div className="tt">
          {w.map((x, i) => (
            <div key={i} className="blur"
                 style={{ width: `${x}%`, ...(i < w.length - 1 ? { marginBottom: 8 } : null) }} />
          ))}
        </div>
        <div className="min">{t[1]}</div>
      </div>
    )
  }
  return (
    <div className={'task' + (done ? ' done' : '')} role="checkbox" tabIndex={0}
         aria-checked={!!done} onClick={onToggle}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onToggle?.() } }}>
      <div className="box" aria-hidden="true"><IcCheck2 /></div>
      <div className="tt">
        <div className="t">{t[0]}</div>
        {t[2] && <div className="b">{t[2]}</div>}
      </div>
      <div className="min">{t[1]}</div>
    </div>
  )
}

export function SetRow({ label, value, onOpen }:
    { label: string; value: string; onOpen: () => void }) {
  return (
    <div className="pl" role="button" tabIndex={0}
         aria-label={`${label}: ${value}. Opens a list of options`}
         onClick={onOpen}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpen() } }}>
      <div className="nm"><b>{label}</b><s>{value}</s></div>
      <IcChev />
    </div>
  )
}

export function SwRow({ label, on, sub, onToggle }:
    { label: string; on: boolean; sub?: string; onToggle: () => void }) {
  return (
    <div className="pl tglrow" role="switch" tabIndex={0} aria-label={label} aria-checked={on}
         onClick={onToggle}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onToggle() } }}>
      <div className="nm"><b>{label}</b>{sub && <s>{sub}</s>}</div>
      <div className={'tgl' + (on ? ' on' : '')} aria-hidden="true"><i /></div>
    </div>
  )
}

export function PickRow({ label, sub, on, onPick }:
    { label: string; sub: string; on: boolean; onPick: () => void }) {
  return (
    <div className={'pl pickrow' + (on ? ' on' : '')} role="radio" tabIndex={0} aria-checked={on}
         onClick={onPick}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onPick() } }}>
      <div className="nm"><b>{label}</b><s>{sub}</s></div>
      <span className="picktick"><IcCheckG /></span>
    </div>
  )
}

/** Тост. Живёт над всеми экранами, поэтому монтируется один раз в App. */
export function Toast() {
  const { s, d } = useStore()
  const timer = useRef<number | undefined>(undefined)
  useEffect(() => {
    if (!s.toast) return
    clearTimeout(timer.current)
    timer.current = window.setTimeout(() => d({ t: 'toast', v: null }), s.toast.ms)
    return () => clearTimeout(timer.current)
  }, [s.toast, d])
  const t = s.toast
  return (
    <div id="toast" className={t ? 'on' : undefined}>
      <span dangerouslySetInnerHTML={{ __html: t ? t.html : '' }} />
      {t?.undo && <b role="button" tabIndex={0} onClick={() => d({ t: 'undo' })}>Undo</b>}
      {t?.unpro && <b role="button" tabIndex={0}
                      onClick={() => { d({ t: 'pro', v: false }); d({ t: 'toast', v: null }) }}>Undo</b>}
    </div>
  )
}

/** Максимальная сторона снимка: журнал показывает кадр на ширину экрана,
    а квота localStorage одна на все фотографии. */
const SHOT_MAX = 1280

/** Кадр в data-URL. blob-URL умирает вместе со страницей: после перезагрузки
    журнал показывал бы битые картинки вместо снимков. */
async function toDataUrl(f: File): Promise<string> {
  const bmp = await createImageBitmap(f, { imageOrientation: 'from-image' })
  const k = Math.min(1, SHOT_MAX / Math.max(bmp.width, bmp.height))
  const c = document.createElement('canvas')
  c.width = Math.round(bmp.width * k)
  c.height = Math.round(bmp.height * k)
  c.getContext('2d')!.drawImage(bmp, 0, 0, c.width, c.height)
  bmp.close()
  return c.toDataURL('image/jpeg', 0.8)
}

/** Скрытый input для «камеры»: настоящий выбор файла, снимок уходит в журнал. */
export function useCamera(onShot: (url: string) => void) {
  const ref = useRef<HTMLInputElement>(null)
  const input = (
    <input ref={ref} type="file" accept="image/*" capture="environment"
           style={{ display: 'none' }}
           onChange={e => {
             const f = e.target.files?.[0]
             e.target.value = ''
             // Формат, который браузер не декодирует (бывает с HEIC): показываем
             // кадр как есть. Перезагрузку он не переживёт, но и не пропадёт сейчас.
             if (f) toDataUrl(f).then(onShot, () => onShot(URL.createObjectURL(f)))
           }} />
  )
  return { input, open: () => ref.current?.click() }
}
