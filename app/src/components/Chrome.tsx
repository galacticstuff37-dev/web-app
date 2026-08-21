// Шасси экрана. Структура DOM повторяет прототип буквально
// (.screen.on > .sb + .hd + .bd + .ofr + .nav), потому что CSS перенесён
// дословно и рассчитывает именно на неё. Отступ под плавающими баннером и
// подвалом считается от РЕАЛЬНЫХ высот через --ofr-bottom и --foot-h:
// три правила под конкретные высоты один раз уже положили баннер на кнопку.

import { useLayoutEffect, useRef, type ReactNode } from 'react'
import { Icon } from '../icons/Icon'

export function StatusBar() {
  return (
    <div className="sb">
      <span>9:41</span>
      <span style={{ letterSpacing: '.06em' }}>
        <Icon name="sun" color="var(--ink)" size={15} sw={2} />
      </span>
    </div>
  )
}

export function Header({ back, onBack }: { back?: boolean; onBack?: () => void }) {
  return (
    <div className="hd">
      <div className="hd-l">
        {back && (
          <div className="back" role="button" tabIndex={0} aria-label="Back"
               onClick={onBack} onKeyDown={e => {
                 if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onBack?.() }
               }}>
            <Icon name="caret-right" color="var(--ink)" size={20} />
          </div>
        )}
      </div>
      <div className="wm">HOMEGROWN</div>
      <div className="hd-r" />
    </div>
  )
}

const NAVI: Array<[string, string, string]> = [
  ['Week', 'calendar-days', 'home'],
  ['Growth', 'camera', 'growth'],
  ['Settings', 'settings-2', 'settings'],
]

export function Nav({ active, badge, go }: { active: string; badge?: boolean; go: (id: string) => void }) {
  return (
    <nav className="nav" aria-label="Main">
      {NAVI.map(([name, icon, target]) => {
        const on = name === active
        return (
          <div key={name} className={'ni' + (on ? ' on' : '')} role="link" tabIndex={0}
               aria-current={on ? 'page' : undefined}
               onClick={() => go(target)}
               onKeyDown={e => {
                 if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(target) }
               }}>
            {badge && name === 'Week' && <div className="bdg" aria-hidden="true" />}
            <Icon name={icon} color="currentColor" size={23} />
            <span>{name}</span>
          </div>
        )
      })}
    </nav>
  )
}

export function Offer({ txt = 'Unlock the full care plan', sub = '$29/yr', onClick }:
                      { txt?: string; sub?: string; onClick?: () => void }) {
  return (
    <div className="ofr" role="button" tabIndex={0} onClick={onClick}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onClick?.() } }}>
      <div className="ofr-in">
        <div className="ofr-ic"><Icon name="sprout" color="var(--lime)" size={19} sw={2} /></div>
        <div className="ofr-tx"><b>{txt}</b><s>{sub}</s></div>
        <div className="ofr-go"><Icon name="chevron-right" color="var(--lime)" size={18} sw={2.4} /></div>
      </div>
    </div>
  )
}

interface ScreenProps {
  id: string
  children: ReactNode
  back?: () => void
  nav?: { active: string; badge?: boolean; go: (id: string) => void }
  offer?: { txt?: string; sub?: string; onClick?: () => void }
  /**
   * Подвал: прибит к низу и НЕ скроллится с контентом. Обязан быть соседом
   * .bd, а не его потомком: .bd — скролл-контейнер, и absolute внутри него
   * уезжает вместе с содержимым и обрезается.
   */
  foot?: ReactNode
  /** сбрасывать прокрутку при смене этого значения (в прототипе — при go()) */
  scrollKey?: string
}

export function Screen({ id, children, back, nav, offer, foot, scrollKey }: ScreenProps) {
  const root = useRef<HTMLDivElement>(null)
  const bd = useRef<HTMLDivElement>(null)

  // Плавающие элементы: подвал садится ровно над таб-баром, иначе кнопка
  // накрывает навигацию. Мерить можно только после того, как всё в DOM.
  useLayoutEffect(() => {
    const el = root.current
    if (!el) return
    const navEl = el.querySelector<HTMLElement>('.nav')
    const footEl = el.querySelector<HTMLElement>('.foot')
    const nh = navEl ? navEl.offsetHeight : 0
    if (footEl) footEl.style.bottom = nh + 'px'
    const fh = footEl ? footEl.offsetHeight : 0
    el.style.setProperty('--ofr-bottom', fh + nh + 12 + 'px')
    el.style.setProperty('--foot-h', fh + nh + 16 + 'px')
  })

  useLayoutEffect(() => { if (bd.current) bd.current.scrollTop = 0 }, [scrollKey])

  return (
    <div className="screen on" id={'s-' + id} ref={root}>
      <StatusBar />
      <Header back={!!back} onBack={back} />
      <div className="bd" ref={bd}>{children}</div>
      {foot && <div className="foot">{foot}</div>}
      {offer && <Offer {...offer} />}
      {nav && <Nav {...nav} />}
    </div>
  )
}
