// Подтверждение необратимого действия. В приложении это ЕДИНСТВЕННЫЙ диалог:
// удаление растения переживается через Undo в тосте, выход из аккаунта
// обратим, и спрашивать там нечего. Здесь спросить обязательно — состояние
// живёт между сессиями, и «Delete account» уносит настоящие данные.

import { useEffect, useRef } from 'react'

export function Confirm({ title, body, yes, no, onYes, onNo }:
    { title: string; body: string; yes: string; no: string
      onYes: () => void; onNo: () => void }) {
  const box = useRef<HTMLDivElement>(null)

  // Escape закрывает, фокус уходит на лист: иначе с клавиатуры человек
  // остаётся в списке настроек под скримом.
  useEffect(() => {
    box.current?.focus()
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onNo() }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onNo])

  return (
    <div className="cf">
      <div className="cf-sc" onClick={onNo} aria-hidden="true" />
      <div className="cf-box" role="alertdialog" aria-modal="true" aria-label={title}
           tabIndex={-1} ref={box}>
        <div className="cf-t">{title}</div>
        <p className="cf-b">{body}</p>
        <div className="btn b-bad" role="button" tabIndex={0} onClick={onYes}
             onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onYes() } }}>
          {yes}
        </div>
        <div className="btn b-ghost" role="button" tabIndex={0} onClick={onNo}
             onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onNo() } }}>
          {no}
        </div>
      </div>
    </div>
  )
}
