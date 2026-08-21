// Роутер на хеше. Хеш, а не history: GitHub Pages не умеет rewrite, а прототип
// и так адресовал экраны через #id — ссылки остаются рабочими.
//
// Портированы четыре экрана. Всё остальное из 29 живёт в старом прототипе на
// index.html и здесь честно помечено заглушкой, а не притворяется готовым.

import { useCallback, useEffect, useState } from 'react'
import { Screen } from './components/Chrome'
import { Note } from './components/bits'
import { CalendarScreen } from './screens/Calendar'
import { GrowthScreen } from './screens/Growth'
import { HomeScreen } from './screens/Home'
import { PlantScreen } from './screens/Plant'
import { Review } from './review/Review'
import { useStore } from './state/store'
import { ASSET_ROOT } from './lib/assets'
import type { Species } from './data/species'

export const DONE_SCREENS = ['home', 'growth', 'plant', 'calendar'] as const
export type ScreenId = string

export function useHash(): [string, (id: string) => void] {
  const read = () => (location.hash.slice(1) || 'home')
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

/** Экран, которого в React ещё нет: не притворяемся, а говорим прямо. */
function NotPorted({ id, go }: { id: string; go: (v: string) => void }) {
  return (
    <Screen id={id} back={() => go('home')} nav={{ active: 'Week', go }} scrollKey={id}>
      <div className="h1" style={{ marginTop: 16 }}>Not ported yet</div>
      <Note title={`Экран «${id}» пока живёт в прототипе`}
            cta={<a className="btn b-pri" href={`${ASSET_ROOT}index.html#${id}`}>
                   Открыть его в прототипе
                 </a>}>
        На React перенесены четыре экрана: Home, Growth, Plant detail и Harvest calendar.
        Остальные 25 не тронуты и работают в исходном прототипе — так решено намеренно,
        чтобы сначала проверить подход на самых сложных экранах.
      </Note>
    </Screen>
  )
}

export function App() {
  const [id, go] = useHash()
  const { d } = useStore()

  // Режим для CSS: мобильные оверрайды применяются только к приложению,
  // на /review нужна рамка телефона со статус-баром и обычный скролл.
  useEffect(() => {
    document.body.dataset.mode = id === 'review' ? 'review' : 'app'
  }, [id])

  // Вход на календарь всегда про «сейчас»: пролистанный месяц не переживает
  // уход с экрана.
  useEffect(() => { if (id === 'calendar') d({ t: 'enterCalendar' }) }, [id, d])

  if (id === 'review') return <Review />

  const openSpecies = (sp: Species) => { d({ t: 'libSeek', v: sp.id }); go('add-plant') }

  const body = () => {
    switch (id) {
      case 'home': return <HomeScreen go={go} />
      case 'growth': return <GrowthScreen go={go} />
      case 'plant': return <PlantScreen go={go} />
      case 'calendar': return <CalendarScreen go={go} openSpecies={openSpecies} />
      default: return <NotPorted id={id} go={go} />
    }
  }
  return <main className="mob">{body()}</main>
}
