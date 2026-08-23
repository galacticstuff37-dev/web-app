// Состояние приложения. В прототипе это были ~58 глобалов; здесь один контекст
// с той же семантикой, чтобы порт можно было сверять с оригиналом по числам.
//
// Специально НЕ разносим по мелким сторам: экраны читают почти всё вместе
// (календарь зависит от zip+outdoor+track, дашборд от MY_PLANTS+isPro), и
// дробление дало бы связность без выгоды.

import {
  createContext, useContext, useEffect, useMemo, useReducer, type ReactNode,
} from 'react'
import { mkPlant, tkey, type Plant, type Task } from '../lib/plants'
import { speciesPool, type Ctx, type Pool } from '../lib/season'
import type { Species } from '../data/species'
import type { Track } from '../data/onboarding'

export type { Track }
export type Units = 'imperial' | 'metric'
export type CalView = 'month' | 'year'
/** 'own' — у человека уже есть растения, 'plan' — начинает с нуля, null — не в онбординге */
export type OnbMode = 'own' | 'plan' | null

export interface Choices {
  track: Track
  space: string
  outdoor: boolean
  sun: string
  sunRank: number
  goals: string[]
  effort: number
  zip: string
}

/** какие типы задач попадают в недельную карточку. Полив не отключается — это ядро. */
export interface Care { pick: boolean; leaf: boolean; rotate: boolean; feed: boolean }
export interface Mail { weekly: boolean; water: boolean; news: boolean }

export interface ToastMsg { html: string; ms: number; at: number; undo?: boolean; unpro?: boolean }

export interface State {
  choices: Choices
  plants: Plant[]
  selected: number
  isPro: boolean
  units: Units
  /** индекс в REMIND_AT */
  remind: number
  care: Care
  mail: Mail
  /** отмеченные задачи недели, ключ = tkey(task) */
  done: Record<string, boolean>
  weekOpen: boolean
  calView: CalView
  calMonth: number | null
  calOpen: string | null
  /** id вида на странице культуры */
  cropId: string | null
  /** развёрнутые полки сезонов, ключ — id полки */
  shelves: Record<string, boolean>
  /** одноразовая передача вида из календаря в библиотеку */
  libSeek: string | null
  onbMode: OnbMode
  /** выбранное в библиотеке, но ещё не добавленное */
  pending: string[]
  /** снимок из камеры: показывается на экране скана */
  scanUrl: string | null
  /** снимок, ждущий, пока человек выберет вид в библиотеке */
  scanKeep: string | null
  /** какая настройка открыта на экране выбора */
  pickKey: string
  /** откуда пришли в пейволл — туда и вернёмся */
  pwFrom: string
  /** удалённое растение для Undo */
  undo: { p: Plant; i: number } | null
  toast: ToastMsg | null
  /** поисковый запрос библиотеки */
  query: string
}

// Съедобное — основной трек продукта. Комнатные остаются полноценной ветвью.
const CHOICES0: Choices = {
  track: 'edible', space: 'patio', outdoor: true,
  sun: '6–8 hours of sun', sunRank: 2, goals: [], effort: 4, zip: '78704',
}

export const seedPlants = (): Plant[] => [
  mkPlant('radish', 0, 27, [{ f: 'radish', day: 24 }, { f: 'leaves1', day: 11 }]),
  mkPlant('lettuce', 1, 24, [{ f: 'leaves3', day: 18 }]),
  mkPlant('basil', 3, 34, [{ f: 'basil', day: 21 }]),
  mkPlant('cherrytomato', 1, 12, []),
]
export const seedHouseDemo = (): Plant[] => [
  mkPlant('monstera', 4, 210, [{ f: 'leaves3', day: 18 }]),
  mkPlant('snakeplant', 20, 430, []),
  mkPlant('pothos', 9, 96, [{ f: 'leaves1', day: 11 }]),
  mkPlant('peacelily', 2, 64, [{ f: 'flowers', day: 21 }]),
]
export const seedMixed = (): Plant[] => [
  mkPlant('monstera', 4, 210, [{ f: 'leaves3', day: 18 }]),
  mkPlant('pothos', 9, 96, []),
  mkPlant('basil', 1, 34, [{ f: 'basil', day: 21 }]),
  mkPlant('radish', 0, 27, [{ f: 'radish', day: 24 }]),
]

const INIT: State = {
  choices: CHOICES0,
  plants: seedPlants(),
  selected: 0,
  isPro: false,
  units: 'imperial',
  remind: 3,
  care: { pick: true, leaf: true, rotate: true, feed: true },
  mail: { weekly: true, water: true, news: false },
  done: {},
  weekOpen: true,
  calView: 'month',
  calMonth: null,
  calOpen: null,
  cropId: null,
  shelves: {},
  libSeek: null,
  onbMode: null,
  pending: [],
  scanUrl: null,
  scanKeep: null,
  pickKey: 'space',
  pwFrom: 'home',
  undo: null,
  toast: null,
  query: '',
}

export type Action =
  | { t: 'choices'; v: Partial<Choices> }
  | { t: 'plants'; v: Plant[] }
  | { t: 'select'; v: number }
  | { t: 'water'; v: number }
  | { t: 'remove'; v: number }
  | { t: 'undo' }
  | { t: 'pro'; v: boolean }
  | { t: 'units'; v: Units }
  | { t: 'remind'; v: number }
  | { t: 'care'; v: keyof Care }
  | { t: 'mail'; v: keyof Mail }
  | { t: 'toggleTask'; v: Task }
  | { t: 'weekOpen'; v: boolean }
  | { t: 'calView'; v: CalView }
  | { t: 'calMonth'; v: number | null }
  | { t: 'calOpen'; v: string | null }
  | { t: 'cropId'; v: string | null }
  | { t: 'shelf'; v: string }
  | { t: 'shelvesInit'; v: Record<string, boolean> }
  | { t: 'libSeek'; v: string | null }
  | { t: 'onb'; v: OnbMode }
  | { t: 'onbReset'; v: OnbMode }
  | { t: 'wipe' }
  | { t: 'pendingToggle'; v: string; limit: number }
  | { t: 'pending'; v: string[] }
  | { t: 'addPending' }
  | { t: 'applyPlan'; v: Species[]; room: number }
  | { t: 'scanUrl'; v: string | null }
  | { t: 'scanKeep'; v: string | null }
  | { t: 'pickKey'; v: string }
  | { t: 'pwFrom'; v: string }
  | { t: 'toast'; v: ToastMsg | null }
  | { t: 'query'; v: string }
  | { t: 'addPhoto'; v: { i: number; url: string } }
  | { t: 'enterCalendar' }
  | { t: 'enterLibrary'; seek: string | null }

function reducer(s: State, a: Action): State {
  switch (a.t) {
    case 'choices': return { ...s, choices: { ...s.choices, ...a.v } }
    case 'plants': return { ...s, plants: a.v, selected: 0 }
    case 'select': return { ...s, selected: a.v }
    case 'water': return { ...s, plants: s.plants.map((p, i) => (i === a.v ? { ...p, since: 0 } : p)) }
    case 'remove': {
      const p = s.plants[a.v]
      if (!p) return s
      const plants = s.plants.filter((_, i) => i !== a.v)
      return { ...s, plants, undo: { p, i: a.v },
               selected: Math.min(s.selected, Math.max(0, plants.length - 1)) }
    }
    case 'undo': {
      if (!s.undo) return s
      const plants = s.plants.slice()
      plants.splice(s.undo.i, 0, s.undo.p)
      return { ...s, plants, undo: null, toast: null }
    }
    case 'pro': return { ...s, isPro: a.v }
    case 'units': return { ...s, units: a.v }
    case 'remind': return { ...s, remind: a.v }
    // Смена состава задач обнуляет отметки: ключи привязаны к позиции растения,
    // и старая галочка после фильтра означала бы уже другую задачу.
    case 'care': return { ...s, care: { ...s.care, [a.v]: !s.care[a.v] }, done: {} }
    case 'mail': return { ...s, mail: { ...s.mail, [a.v]: !s.mail[a.v] }, done: {} }
    case 'toggleTask': {
      const k = tkey(a.v)
      return { ...s, done: { ...s.done, [k]: !s.done[k] } }
    }
    case 'weekOpen': return { ...s, weekOpen: a.v }
    case 'calView': return { ...s, calView: a.v, calOpen: null }
    case 'calMonth': return { ...s, calMonth: a.v }
    case 'calOpen': return { ...s, calOpen: s.calOpen === a.v ? null : a.v }
    case 'cropId': return { ...s, cropId: a.v }
    case 'shelf': return { ...s, shelves: { ...s.shelves, [a.v]: !s.shelves[a.v] } }
    case 'shelvesInit': return { ...s, shelves: a.v }
    case 'libSeek': return { ...s, libSeek: a.v }
    case 'onb': return { ...s, onbMode: a.v }
    // Онбординг начинается с чистого листа: демо-набор не должен притворяться
    // растениями, которые человек занёс сам.
    case 'onbReset': return { ...s, onbMode: a.v, plants: [], pending: [], selected: 0,
                              done: {}, scanKeep: null }
    // Delete account: назад к состоянию до первого запуска. Не onbReset —
    // тот чистит только растения, а тут уходят и выбор места, и ZIP, и Pro.
    // Демо-набор не возвращаем: человек попадает в онбординг с пустыми руками.
    case 'wipe': return { ...INIT, plants: [] }
    case 'pendingToggle': {
      const k = s.pending.indexOf(a.v)
      if (k > -1) return { ...s, pending: s.pending.filter(x => x !== a.v) }
      if (s.plants.length + s.pending.length >= a.limit) return s
      return { ...s, pending: [...s.pending, a.v] }
    }
    case 'pending': return { ...s, pending: a.v }
    case 'addPending': {
      const add = s.pending.map(id => mkPlant(id, 0, 0,
        s.scanKeep ? [{ u: s.scanKeep, day: 0 }] : []))
      return { ...s, plants: [...s.plants, ...add], pending: [], scanKeep: null,
               onbMode: null, selected: s.plants.length }
    }
    // План — предложение. Раньше он строился, показывался и молча выбрасывался:
    // после save→paywall на Home лежал демо-набор, а не то, что человек видел.
    case 'applyPlan': return { ...s, onbMode: null,
      plants: a.v.slice(0, a.room).map(sp => mkPlant(sp.id, 0, 0, [])) }
    case 'scanUrl': return { ...s, scanUrl: a.v }
    case 'scanKeep': return { ...s, scanKeep: a.v }
    case 'pickKey': return { ...s, pickKey: a.v }
    case 'pwFrom': return { ...s, pwFrom: a.v }
    case 'toast': return { ...s, toast: a.v }
    case 'query': return { ...s, query: a.v }
    case 'addPhoto': return { ...s, plants: s.plants.map((p, i) =>
      i === a.v.i ? { ...p, photos: [{ u: a.v.url, day: p.day }, ...p.photos] } : p) }
    // Вход на календарь всегда про «сейчас»: пролистанный месяц и раскрытая
    // строка не переживают уход с экрана. Вид — привычка человека, его храним.
    case 'enterCalendar': return { ...s, calMonth: null, calOpen: null }
    // Роутер прототипа на входе в библиотеку чистил и поиск, и выбор; передача
    // вида из календаря — единственное, что переживает вход.
    case 'enterLibrary': {
      const sk = a.seek
      const own = sk ? s.plants.some(p => p.s.id === sk) : false
      return { ...s, libSeek: null, query: '', pending: sk && !own ? [sk] : [] }
    }
  }
}

interface Store {
  s: State
  d: (a: Action) => void
  /** контекст сезона: от него зависят все окна */
  ctx: Ctx
  /** виды, уместные при текущем треке и месте */
  pool: Species[]
}

const Ctx0 = createContext<Store | null>(null)

export function StoreProvider({ children, initial }:
    { children: ReactNode; initial?: Partial<State> }) {
  const [s, d] = useReducer(reducer, { ...INIT, ...initial })
  const value = useMemo<Store>(() => {
    const ctx: Ctx = { zip: s.choices.zip, outdoor: s.choices.outdoor }
    const p: Pool = { track: s.choices.track, outdoor: s.choices.outdoor }
    return { s, d, ctx, pool: speciesPool(p) }
  }, [s])
  // для сверки с прототипом из консоли: __state().plants
  useEffect(() => {
    ;(window as unknown as { __state?: () => State }).__state = () => s
  }, [s])
  return <Ctx0.Provider value={value}>{children}</Ctx0.Provider>
}

export function useStore(): Store {
  const v = useContext(Ctx0)
  if (!v) throw new Error('useStore вне StoreProvider')
  return v
}
