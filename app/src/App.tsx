// Роутер на хеше. Хеш, а не history: GitHub Pages не умеет rewrite, а прототип
// и так адресовал экраны через #id — ссылки остаются рабочими.

import { useCallback, useEffect, useState } from 'react'
import { useAuthSession } from './screens/Auth'
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

  // Полоса «Unlock the full care plan» скрыта у Pro правилом body.is-pro .ofr —
  // правило перенесли, а класс ставить забыли, и апсейл висел уже после покупки.
  useEffect(() => {
    document.body.classList.toggle('is-pro', s.isPro)
  }, [s.isPro])

  // Пейволл закрывается туда, откуда пришли. Запоминаем предыдущий экран.
  useEffect(() => {
    if (id !== 'paywall') return
    const from = s.pwFrom
    if (from === 'paywall') d({ t: 'pwFrom', v: 'home' })
  }, [id, s.pwFrom, d])

  // Home — конец обоих онбордингов. Если человек ушёл с середины и вернулся
  // (состояние теперь переживает перезагрузку), режим не должен жить дальше:
  // иначе библиотека остаётся в онбординговом виде и без таб-бара.
  useEffect(() => {
    if (id === 'home' && s.onbMode) d({ t: 'onb', v: null })
  }, [id, s.onbMode, d])

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

  // Вход через Google возвращает человека уже с сессией: подхватываем её и
  // уводим на экран, с которого начинали.
  useAuthSession(goTracked)

  if (hash === 'review') return <Review />

  const openSpecies = (sp: Species) => {
    d({ t: 'cropId', v: sp.id })
    goTracked('crop')
  }

  return (
    <main className="mob">
      {(ROUTE(id) || ROUTES[0]).render({ go: goTracked, openSpecies })}
      <Toast />
    </main>
  )
}
