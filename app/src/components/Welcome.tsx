// Приветствие вернувшемуся. Показывается один раз за визит ВМЕСТО экрана входа:
// человеку с живой сессией предлагать «Continue with Google» — это предлагать
// сделать то, что уже сделано.
//
// Лист снизу, а не карточка по центру: в приложении ровно одна форма всплывающего
// слоя, и она уже задана подтверждением удаления. Две разные формы для двух
// всплывашек читались бы как две разные системы.
//
// role=dialog, а НЕ alertdialog: alertdialog остаётся единственным и только на
// необратимом. Здесь ничего не решается — есть кнопка «дальше», Escape и тап по
// затемнению, и любой из трёх выходов равнозначен.

import { useEffect, useRef } from 'react'
import { tkey, weekTasks } from '../lib/plants'
import { useStore } from '../state/store'

export function Welcome({ onClose, onAccount }:
    { onClose: () => void; onAccount: () => void }) {
  const { s } = useStore()
  const box = useRef<HTMLDivElement>(null)

  useEffect(() => {
    box.current?.focus()
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])

  // Приветствие без содержания — это шум. Поэтому первой строкой идёт то, зачем
  // человек и открыл приложение: сколько на нём висит на этой неделе.
  const left = weekTasks(s.plants, s.care).filter(t => !s.done[tkey(t)]).length
  const line = !s.plants.length
    ? 'Your garden is empty — add a plant and the week fills itself in.'
    : left === 0 ? 'Everything is on schedule.'
    : left === 1 ? 'One task is waiting this week.'
    : `${left} tasks are waiting this week.`

  return (
    <div className="cf">
      <div className="cf-sc" onClick={onClose} aria-hidden="true" />
      <div className="cf-box" role="dialog" aria-modal="true" aria-label="Welcome back"
           tabIndex={-1} ref={box}>
        <div className="cf-t">Welcome back</div>
        <p className="cf-b">{line}</p>
        {s.account && (
          <p className="cf-who">Signed in as <b>{s.account.email}</b></p>
        )}
        <div className="btn b-pri" role="button" tabIndex={0} onClick={onClose}
             onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onClose() } }}>
          Keep going
        </div>
        <div className="tlink2" role="button" tabIndex={0} onClick={onAccount}
             onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onAccount() } }}>
          Manage account
        </div>
      </div>
    </div>
  )
}
