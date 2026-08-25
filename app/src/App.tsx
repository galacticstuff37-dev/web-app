// Роутер на хеше. Хеш, а не history: GitHub Pages не умеет rewrite, а прототип
// и так адресовал экраны через #id — ссылки остаются рабочими.

import { useCallback, useEffect, useRef, useState } from 'react'
import { useAuthSession } from './screens/Auth'
import { supa } from './lib/supabase'
import { lastReport, runSync, type SyncReport } from './lib/sync'
import { Toast } from './components/parts'
import { Welcome } from './components/Welcome'
import { Review } from './review/Review'
import { ROUTE, ROUTES } from './routes'
import { useStore, type Pulled } from './state/store'
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

/**
 * Синхронизация с базой. Здесь только повод её запустить — вся работа в
 * lib/sync.ts.
 *
 * Три повода: изменилось синхронизируемое (с задержкой, иначе каждая буква в
 * ZIP была бы запросом), вкладку снова открыли (с другого устройства могло
 * приехать новое) и появился аккаунт. Таймера нет: приложение и без сети
 * полное, а опрос по расписанию — это трафик без повода.
 *
 * Ошибки наружу не выходят: неудачная синхронизация ничего не показывает и
 * повторится в следующий раз. Посмотреть, чем закончилась, можно из консоли —
 * window.__sync() гоняет проход и отдаёт отчёт.
 */
function useSync() {
  const { s, d } = useStore()
  // Проход асинхронный, за это время состояние успевает измениться: отправлять
  // надо СВЕЖЕЕ, а не то, что было на момент запуска.
  const cur = useRef(s)
  useEffect(() => { cur.current = s }, [s])
  const apply = useCallback((p: Pulled) => d({ t: 'pulled', v: p }), [d])
  // catch, а не голый then: без сети import() клиента отваливается, и без него
  // это стало бы необработанным отказом промиса — то есть ошибкой в консоли,
  // на которую свип вёрстки справедливо ругается.
  const run = useCallback((): Promise<SyncReport> =>
    supa().then(sb => runSync(sb, () => cur.current, apply))
          .catch(e => ({ ok: false, error: e instanceof Error ? e.message : String(e) })),
    [apply])
  const timer = useRef<ReturnType<typeof setTimeout>>()
  const kick = useCallback((ms: number) => {
    clearTimeout(timer.current)
    timer.current = setTimeout(() => { void run() }, ms)
  }, [run])

  const on = s.account !== null

  useEffect(() => {
    if (!on) return
    kick(1500)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [on, s.plants, s.choices, s.isPro, s.units, s.remind, s.care, s.mail, s.done, s.calView])

  useEffect(() => {
    if (!on) return
    const back = () => { if (!document.hidden) kick(0) }
    document.addEventListener('visibilitychange', back)
    return () => document.removeEventListener('visibilitychange', back)
  }, [on, kick])

  // Крючок для стендов, как __state()/__audit(): проход по требованию и отчёт.
  useEffect(() => {
    window.__sync = run
    window.__syncReport = lastReport
  }, [run])

  useEffect(() => () => clearTimeout(timer.current), [])
}

declare global {
  interface Window {
    __sync?: () => Promise<SyncReport>
    __syncReport?: () => SyncReport
  }
}

/** Приветствие показано в этом визите. Визит = вкладка, отсюда sessionStorage. */
const GREET_KEY = 'hg.greeted'

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

  // Экрана входа для вошедшего не существует. «Welcome back + Continue with
  // Google» человеку с живой сессией — это предложение сделать то, что уже
  // сделано; он попадал сюда потому, что уводило отсюда только сохранённое
  // hg.authNext, а оно привязано к origin и после возврата на другой адрес
  // пустое. Теперь уводит само состояние.
  //
  // ТОЛЬКО signin, и это важно. Экраны email и code — середина входа: там
  // аккаунт появляется в состоянии РАНЬШЕ, чем меняется хеш (dispatch немедленно,
  // hashchange — следующим тиком), и эффект успевал перебить go('paywall') на
  // home. Онбординг из-за этого не доводил до пейволла.
  useEffect(() => {
    if (s.account && id === 'signin') go('home')
  }, [id, s.account, go])

  // Приветствие: один раз за визит. Визит — это вкладка, поэтому флаг в
  // sessionStorage, а не в состоянии: переходы внутри приложения и перерисовки
  // его не сбрасывают, а новая вкладка сбрасывает.
  const [greet, setGreet] = useState(false)
  useEffect(() => {
    if (!s.account || greet) return
    // В онбординге и на лендинге приветствовать нечего: человек в другом деле,
    // и попап туда влез бы поперёк шага. На /review — тоже: это стенд сверки, а
    // не приложение, и приветствие там сожгло бы флаг визита впустую.
    if (hash === 'review' || ROUTE(id)?.group === 'Онбординг') return
    try {
      if (sessionStorage.getItem(GREET_KEY)) return
      sessionStorage.setItem(GREET_KEY, '1')
    } catch { return }            // приватный режим: молча не показываем
    setGreet(true)
  }, [s.account, id, hash, greet])

  const goTracked = useCallback((next: string) => {
    // save ведёт в пейволл, но возвращаться из него надо на home, а не на save
    if (next === 'paywall') d({ t: 'pwFrom', v: id === 'save' ? 'home' : id })
    go(next)
  }, [go, d, id])

  // Вход через Google возвращает человека уже с сессией: подхватываем её и
  // уводим на экран, с которого начинали.
  useAuthSession(goTracked)
  useSync()

  if (hash === 'review') return <Review />

  const openSpecies = (sp: Species) => {
    d({ t: 'cropId', v: sp.id })
    goTracked('crop')
  }

  return (
    <main className="mob">
      {(ROUTE(id) || ROUTES[0]).render({ go: goTracked, openSpecies })}
      {greet && (
        <Welcome onClose={() => setGreet(false)}
                 onAccount={() => { setGreet(false); goTracked('account') }} />
      )}
      <Toast />
    </main>
  )
}
