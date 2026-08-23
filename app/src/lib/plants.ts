// Состояние растения. ОДНА форма на весь продукт: { s, since, day, photos }.
//   s      — вид из справочника
//   since  — дней с последнего полива
//   day    — возраст растения в днях
//   photos — журнал: {f} для готового снимка из img/, {u} для data-URL с камеры

import { SP, SPECIES, type Species } from '../data/species'
import { img } from './assets'

export interface Photo { f?: string; u?: string; day: number }

/** URL снимка журнала: загруженный кадр или фото из /img. Жил копией в двух
    экранах сразу, поэтому переехал к типу. */
export const phUrl = (x: Photo) => x.u || img(x.f || '')
export interface Plant { s: Species; since: number; day: number; photos: Photo[] }

export const FREE_LIMIT = 3
export const limit = (isPro: boolean) => (isPro ? 99 : FREE_LIMIT)

export function mkPlant(id: string, since = 0, day = 0, photos: Photo[] = []): Plant {
  return { s: SP(id) || SPECIES[0], since, day, photos }
}

export const isEdible = (p: Plant) => p.s.kind === 'edible'

// Компактная подпись света для узкой колонки виджета: раньше строка резалась по
// первому слову и «Low to bright» превращалось в «Low».
const LIGHTSHORT: Record<string, string> = {
  'Low to bright': 'Any', 'Bright indirect': 'Indirect',
  'Medium indirect': 'Indirect', 'Bright direct': 'Direct', 'Low light': 'Low',
}
export const lightShort = (s: Species) =>
  LIGHTSHORT[s.light] || s.light.replace(/ (h )?sun$/, 'h')

export const lc = (s: string) => s.charAt(0).toLowerCase() + s.slice(1)

/** дней до полива: отрицательное — просрочено */
export const wDue = (p: Plant) => p.s.water - p.since
export const wPct = (p: Plant) =>
  Math.max(0, Math.min(100, Math.round((p.since / p.s.water) * 100)))
export const hPct = (p: Plant) =>
  !isEdible(p) ? 0 : Math.min(100, Math.round((p.day / p.s.days) * 100))
export const hEta = (p: Plant) => {
  const d = p.s.days - p.day
  return d <= 0 ? 'ready' : `~${d}d`
}
export const hStage = (p: Plant) => {
  const r = p.day / p.s.days
  return r < 0.1 ? 'seed' : r < 0.35 ? 'seedling' : r < 0.7 ? 'growing'
       : r < 1 ? 'nearly ready' : 'ready'
}

export type StateTone = 'ok' | 'warn' | 'bad'
export function pState(p: Plant): [string, StateTone] {
  const d = wDue(p)
  if (d <= 0) return ['Needs water', 'bad']
  if (d <= 2) return ['Water soon', 'warn']
  if (isEdible(p) && hPct(p) >= 100) return ['Ready to pick', 'ok']
  return ['Healthy', 'ok']
}

export interface JournalShot { f?: string; u?: string; n: string; day: number; st: string }
export const allPhotos = (plants: Plant[]): JournalShot[] =>
  plants.flatMap(p => p.photos.map(x => ({
    f: x.f, u: x.u, n: p.s.name, day: x.day, st: pState(p)[0],
  }))).sort((a, b) => b.day - a.day)

export function healthScore(plants: Plant[]): number {
  if (!plants.length) return 0
  const sum = plants.reduce((a, p) => {
    const d = wDue(p)
    const pen = d > 0 ? 0                                  // ещё не пора — полный вклад
              : d === 0 ? 0.12                             // ровно сегодня — небольшой штраф
              : Math.min(1, (-d / p.s.water) * 1.6)        // просрочено — по мере просрочки
    return a + Math.max(0, 1 - pen)
  }, 0)
  return Math.round((sum / plants.length) * 100)
}

export function verdict(sc: number, due = 0): [string, string] {
  if (due >= 3) return ['Struggling', `${due} plants are waiting for water`]
  if (due === 2) return ['Needs care', 'Two are waiting for water']
  if (due === 1) return ['Good', 'One needs a drink today']
  if (sc >= 92) return ['Great', 'Your plants are doing amazing']
  if (sc >= 75) return ['Good', 'Everything is on schedule']
  return ['Needs care', 'Some plants are drifting off schedule']
}

export interface CareStats {
  plants: number; due: number; photos: number; score: number; waterings: number
  soon: number; edible: number; ready: number; oldest: number; healthy: number
}
export function careStats(plants: Plant[]): CareStats {
  let waterings = 0
  plants.forEach(p => { waterings += Math.floor((p.day - p.since) / p.s.water) + 1 })
  return {
    plants: plants.length,
    due: plants.filter(p => wDue(p) <= 0).length,
    photos: allPhotos(plants).length,
    score: healthScore(plants),
    waterings: Math.max(0, waterings),
    soon: plants.filter(p => { const d = wDue(p); return d > 0 && d <= 2 }).length,
    edible: plants.filter(isEdible).length,
    ready: plants.filter(p => isEdible(p) && hPct(p) >= 100).length,
    oldest: plants.reduce((a, p) => Math.max(a, p.day), 0),
    healthy: plants.filter(p => wDue(p) > 2).length,
  }
}

// Задачи недели СЧИТАЮТСЯ из растений, а не захардкожены.
// Задача = [заголовок, время, пояснение, КЛЮЧ]. Ключ привязан к растению:
// по тексту два одинаковых заголовка делили одну галочку.
export type Task = [string, string, string, string]
/** состав задач по умолчанию: всё включено, как в прототипе до правок настроек */
export const CARE = { pick: true, leaf: true, rotate: true, feed: true }

// care приходит из состояния: тумблеры Settings обещают фильтровать эту карточку,
// а функция читала свою константу — обещание не выполнялось ни разу.
export function weekTasks(plants: Plant[], care = CARE): Task[] {
  if (!plants.length) return []
  const out: Task[] = []
  plants.forEach((p, i) => {
    if (wDue(p) <= 0) out.push([
      `Water the ${lc(p.s.name)}`, '1 min',
      `${p.since} days since the last drink — it wants one every ${p.s.water}.`,
      `water:${i}`,
    ])
  })
  if (care.pick) plants.forEach((p, i) => {
    if (isEdible(p) && hPct(p) >= 100) out.push([
      `Pick from the ${lc(p.s.name)}`, '4 min',
      'It is ready. Picking keeps it producing.', `pick:${i}`,
    ])
  })
  const si = plants.findIndex(p => p.s.tags.indexOf('statement') > -1)
  if (care.leaf && si > -1) out.push([
    `Wipe the ${lc(plants[si].s.name)} leaves`, '3 min',
    'Dust cuts the light it gets.', `wipe:${si}`,
  ])
  plants.forEach((p, i) => {
    const d = wDue(p)
    if (d > 0 && d <= 2) out.push([
      `Check the ${lc(p.s.name)} — top soil dry?`, '1 min', '', `check:${i}`,
    ])
  })
  const ti = plants.findIndex(p => p.s.sun >= 2)
  if (care.rotate && ti > -1) out.push([
    `Rotate the ${lc(plants[ti].s.name)} a quarter turn`, '1 min',
    'Keeps it growing even on all sides.', `rotate:${ti}`,
  ])
  if (care.feed) out.push([
    plants.some(isEdible) ? 'Feed the edible pots once this month'
                          : 'Feed everything once this month', '4 min',
    'Container soil runs out faster than a bed.', 'feed',
  ])
  return out.slice(0, 6)
}
export const tkey = (t: Task) => t[3] || t[0]

const POT_METRIC: Record<string, string> = {
  '1 pint': '0.5 L', '0.5 gal': '2 L', '1 gal': '4 L', '2 gal': '7.5 L',
  '3 gal': '11 L', '5 gal': '19 L', '1 quart': '1 L', 'tray': 'tray',
  '6 inch': '15 cm', '8 inch': '20 cm', '10 inch': '25 cm', '12 inch': '30 cm',
}
export const fmtPot = (v: string, units: 'imperial' | 'metric') =>
  units === 'metric' ? (POT_METRIC[v] || v) : v
