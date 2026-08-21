// Роутер на хеше. Хеш, а не history: GitHub Pages не умеет rewrite, а прототип
// и так адресовал экраны через #id — ссылки остаются рабочими.

import { useCallback, useEffect, useState } from 'react'
import { Toast } from './components/parts'
import { Review } from './review/Review'
import { ROUTE, ROUTES } from './routes'
import { useStore } from './state/store'
import type { Species } from './data/species'

export function useHash(): [string, (id: string) => void] {
  const read = () => location.hash.slice(1) || 'home'
  const [id, setId] = useState(read)
  useEffect(() => {
    const on = () => setId(read())
    addEventListener('hashchange', on)
    return () => removeEventListener('hashchange', on)
  }, [])
  const go = useCallback((next: string) => {
    if (location.hash.slice(1) === next) setId(next)
    else location.hash = next
  }, [])
  return [id, go]
}

export function App() {
  const [hash, go] = useHash()
  const { s, d } = useStore()
  const route = ROUTE(hash)
  const id = route ? hash : 'home'

  // Режим для CSS: мобильные оверрайды применяются только к приложению,
  // на /review нужна рамка телефона со статус-баром и обычный скролл.
  useEffect(() => {
    document.body.dataset.mode = hash === 'review' ? 'review' : 'app'
  }, [hash])

  // Пейволл закрывается туда, откуда пришли. Запоминаем предыдущий экран.
  useEffect(() => {
    if (id !== 'paywall') return
    const from = s.pwFrom
    if (from === 'paywall') d({ t: 'pwFrom', v: 'home' })
  }, [id, s.pwFrom, d])

  // Вход на экран: сброс того, что не должно переживать уход.
  useEffect(() => {
    if (id === 'calendar') d({ t: 'enterCalendar' })
    if (id === 'add-plant') d({ t: 'enterLibrary', seek: s.libSeek })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  const goTracked = useCallback((next: string) => {
    // save ведёт в пейволл, но возвращаться из него надо на home, а не на save
    if (next === 'paywall') d({ t: 'pwFrom', v: id === 'save' ? 'home' : id })
    go(next)
  }, [go, d, id])

  if (hash === 'review') return <Review />

  const openSpecies = (sp: Species) => {
    d({ t: 'libSeek', v: sp.id })
    goTracked('add-plant')
  }

  return (
    <main className="mob">
      {(ROUTE(id) || ROUTES[0]).render({ go: goTracked, openSpecies })}
      <Toast />
    </main>
  )
}
