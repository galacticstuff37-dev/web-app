// Состояние приложения. В прототипе это были ~58 глобалов; здесь один контекст
// с той же семантикой, чтобы порт можно было сверять с оригиналом по числам.
//
// Специально НЕ разносим по мелким сторам: экраны читают почти всё вместе
// (календарь зависит от zip+outdoor+track, дашборд от MY_PLANTS+isPro), и
// дробление дало бы связность без выгоды.

import { createContext, useContext, useEffect, useMemo, useReducer, type ReactNode } from 'react'
import { mkPlant, type Plant, type Task, tkey } from '../lib/plants'
import { speciesPool, type Ctx, type Pool } from '../lib/season'
import type { Species } from '../data/species'

export type Track = 'house' | 'edible' | 'both'
export type Units = 'imperial' | 'metric'
export type CalView = 'month' | 'year'

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

export interface State {
  choices: Choices
  plants: Plant[]
  selected: number
  isPro: boolean
  units: Units
  /** отмеченные задачи недели, ключ = tkey(task) */
  done: Record<string, boolean>
  weekOpen: boolean
  calView: CalView
  /** выбранный месяц; null — текущий */
  calMonth: number | null
  /** id раскрытой строки годового вида */
  calOpen: string | null
  /** одноразовая передача вида из календаря в библиотеку */
  libSeek: string | null
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
  done: {},
  weekOpen: true,
  calView: 'month',
  calMonth: null,
  calOpen: null,
  libSeek: null,
}

export type Action =
  | { t: 'choices'; v: Partial<Choices> }
  | { t: 'plants'; v: Plant[] }
  | { t: 'select'; v: number }
  | { t: 'water'; v: number }
  | { t: 'remove'; v: number }
  | { t: 'pro'; v: boolean }
  | { t: 'units'; v: Units }
  | { t: 'toggleTask'; v: Task }
  | { t: 'weekOpen'; v: boolean }
  | { t: 'calView'; v: CalView }
  | { t: 'calMonth'; v: number | null }
  | { t: 'calOpen'; v: string | null }
  | { t: 'libSeek'; v: string | null }
  | { t: 'enterCalendar' }

function reducer(s: State, a: Action): State {
  switch (a.t) {
    case 'choices': return { ...s, choices: { ...s.choices, ...a.v } }
    case 'plants': return { ...s, plants: a.v, selected: 0 }
    case 'select': return { ...s, selected: a.v }
    case 'water': {
      const plants = s.plants.map((p, i) => (i === a.v ? { ...p, since: 0 } : p))
      return { ...s, plants }
    }
    case 'remove': {
      const plants = s.plants.filter((_, i) => i !== a.v)
      return { ...s, plants, selected: Math.min(s.selected, Math.max(0, plants.length - 1)) }
    }
    case 'pro': return { ...s, isPro: a.v }
    case 'units': return { ...s, units: a.v }
    case 'toggleTask': {
      const k = tkey(a.v)
      return { ...s, done: { ...s.done, [k]: !s.done[k] } }
    }
    case 'weekOpen': return { ...s, weekOpen: a.v }
    case 'calView': return { ...s, calView: a.v, calOpen: null }
    case 'calMonth': return { ...s, calMonth: a.v }
    case 'calOpen': return { ...s, calOpen: s.calOpen === a.v ? null : a.v }
    case 'libSeek': return { ...s, libSeek: a.v }
    // Вход на экран календаря всегда про «сейчас»: пролистанный месяц и
    // раскрытая строка не должны переживать уход с экрана. Вид вида — привычка
    // человека, его сохраняем.
    case 'enterCalendar': return { ...s, calMonth: null, calOpen: null }
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

export function StoreProvider({ children, initial }: { children: ReactNode; initial?: Partial<State> }) {
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
