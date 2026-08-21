// Модель сезона: окна посева и сбора ВЫВОДЯТСЯ, а не выдуманы.
//
// Считаются из даты последних заморозков выбранного ZIP, длины сезона и числа
// дней до сбора каждой культуры. Холодостойкие (cool) уходят в грунт за месяц
// до последних заморозков, теплолюбивые — только после. Крайний срок посева
// такой, чтобы культура успела отдать урожай до первых осенних заморозков.
//
// Известное ограничение, оно проговорено на экране: модель работает от
// заморозков, а не от летней жары, поэтому в жарком регионе салат, редис и
// кинза уйдут в стрелку в середине лета, хотя строка остаётся открытой.
// Температурную модель выдумывать нельзя.

import { SPECIES, type Species } from '../data/species'
import { ZIPS, type Zip } from '../data/zips'

export const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export const MON1 = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
export const MONF = ['January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']

/** Условный «сегодня» прототипа: START + TODAY = 10 апреля 2026. */
export const START = new Date(2026, 2, 14)
export const TODAY = 27
export const dayOffset = (d: number) => {
  const x = new Date(START)
  x.setDate(x.getDate() + d)
  return x
}
export const nowMonth = () => dayOffset(TODAY).getMonth()

export const zipInfo = (zip: string): Zip => ZIPS.find(z => z.zip === zip) || ZIPS[0]

export interface Frost { last: Date; first: Date }
export function frostDates(zip: string): Frost {
  const z = zipInfo(zip)
  const parts = z.frost.split(' ')
  const last = new Date(2026, MON.indexOf(parts[0]), +parts[1])
  const first = new Date(last)
  first.setDate(first.getDate() + z.season)
  return { last, first }
}

export interface Ctx {
  zip: string
  /** false = в помещении: заморозков нет, значит нет и календарного окна. */
  outdoor: boolean
}

export interface Window {
  sow: [Date, Date]
  pick: [Date, Date]
  /** сезон слишком короткий: окна нет вовсе */
  tight: boolean
}

export function windows(sp: Species, ctx: Ctx): Window | null {
  // В помещении заморозков нет — годится любой месяц. Раньше окна всё равно
  // считались от заморозков, и экран спорил сам с собой: подзаголовок обещал
  // «any month works», а строки показывали весну.
  if (sp.kind === 'house' || !ctx.outdoor) return null
  const f = frostDates(ctx.zip)
  const from = new Date(f.last)
  if (sp.cool) from.setDate(from.getDate() - 28)
  const to = new Date(f.first)
  to.setDate(to.getDate() - sp.daysMax - 14)
  if (to < from) return { sow: [from, from], pick: [from, from], tight: true }
  const pickFrom = new Date(from); pickFrom.setDate(pickFrom.getDate() + sp.days)
  const pickTo = new Date(to); pickTo.setDate(pickTo.getDate() + sp.daysMax)
  return { sow: [from, to], pick: [pickFrom, pickTo], tight: false }
}

const monthsOf = (a: Date, b: Date) => {
  const out: Record<number, 1> = {}
  const d = new Date(a.getFullYear(), a.getMonth(), 1)
  while (d <= b) { out[d.getMonth()] = 1; d.setMonth(d.getMonth() + 1) }
  return out
}

export type MonthKind = 'sow' | 'pick' | 'both' | ''

// Кэш: рейка месяцев спрашивает monthMap 12x29 раз за перерисовку, а ответ
// меняется только от ZIP и от «на улице или нет».
let CACHE: Record<string, MonthKind[] | null> = {}
let CACHE_KEY = ''

export function monthMap(sp: Species, ctx: Ctx): MonthKind[] | null {
  const key = `${ctx.zip}|${ctx.outdoor ? 1 : 0}`
  if (key !== CACHE_KEY) { CACHE_KEY = key; CACHE = {} }
  if (sp.id in CACHE) return CACHE[sp.id]
  const w = windows(sp, ctx)
  let out: MonthKind[] | null = null
  if (w) {
    const sow = monthsOf(w.sow[0], w.sow[1])
    const pick = monthsOf(w.pick[0], w.pick[1])
    out = MON1.map((_, m) => {
      if (sow[m] && pick[m]) return 'both'   // и сеять можно, и что-то снимаешь
      if (sow[m]) return 'sow'
      if (pick[m]) return 'pick'
      return ''
    })
  }
  CACHE[sp.id] = out
  return out
}

/** Какие виды вообще уместны при выбранном треке и месте. */
export interface Pool { track: 'house' | 'edible' | 'both'; outdoor: boolean }
export function speciesPool(p: Pool): Species[] {
  return SPECIES.filter(s => {
    if (p.track === 'house' && s.kind !== 'house') return false
    if (p.track === 'edible' && s.kind !== 'edible') return false
    if (s.kind === 'edible' && !p.outdoor && !s.sill) return false
    return true
  })
}

export function inWin(sp: Species, m: number, kind: 'sow' | 'pick', ctx: Ctx): boolean {
  const mm = monthMap(sp, ctx)
  // Съедобное без сезона (подоконник) сеется в любой месяц, а «снимать в таком-то
  // месяце» без сезона не определено — там счёт идёт от даты посева.
  if (!mm) return sp.kind === 'edible' && kind === 'sow'
  const k = mm[m]
  return kind === 'sow' ? (k === 'sow' || k === 'both') : (k === 'pick' || k === 'both')
}

export const sowableIn = (m: number, pool: Species[], ctx: Ctx) =>
  pool.filter(sp => inWin(sp, m, 'sow', ctx))
export const pickableIn = (m: number, pool: Species[], ctx: Ctx) =>
  pool.filter(sp => inWin(sp, m, 'pick', ctx))

/** Трек комнатных: у календаря урожая для него нет ни окон, ни сбора. */
export const isHousePool = (pool: Species[]) => !pool.some(s => s.kind === 'edible')

// Порядок строк годового вида — по дате открытия окна посева, потом по крайнему
// сроку: при одинаковом старте первой идёт культура, у которой меньше времени.
// Так строки складываются в каскад вместо ровной зелёной плиты.
export function calSort(list: Species[], ctx: Ctx): Species[] {
  return list.slice().sort((a, b) => {
    const wa = windows(a, ctx), wb = windows(b, ctx)
    if (!wa || !wb) return !wa && !wb ? a.name.localeCompare(b.name) : (wa ? -1 : 1)
    return (+wa.sow[0] - +wb.sow[0]) || (+wa.sow[1] - +wb.sow[1]) || a.name.localeCompare(b.name)
  })
}

// В месячном виде полезен другой порядок: не каскад окон, а «что даст урожай
// раньше» — число дней стоит на самой плитке.
export const byDays = (list: Species[]) =>
  list.slice().sort((a, b) =>
    (a.days - b.days) || (a.daysMax - b.daysMax) || a.name.localeCompare(b.name))

export const fmtMD = (d: Date) => `${MON[d.getMonth()]} ${d.getDate()}`
export const spDays = (sp: Species) =>
  sp.days + (sp.daysMax !== sp.days ? `–${sp.daysMax}` : '')
export const addD = (d: Date, n: number) => {
  const x = new Date(d); x.setDate(x.getDate() + n); return x
}

/** Позиция даты на оси года в процентах — из этого считаются длины полос. */
export const pctY = (d: Date) =>
  Math.max(0, Math.min(100, (+d - +new Date(2026, 0, 1)) / 86400000 / 365 * 100))
