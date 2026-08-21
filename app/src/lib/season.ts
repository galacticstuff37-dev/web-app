// Модель сезона: окна ВЫВОДЯТСЯ из дат заморозков, а не выдуманы.
//
// Что изменилось против первой версии и почему.
//
// 1. Было ОДНО непрерывное окно от заморозков до заморозков минус срок
//    созревания. В опубликованных календарях у холодостойкой культуры их ДВА —
//    весной и в конце лета — с провалом на жару между ними. Салат в Остине:
//    раньше выходило Feb 3 – Oct 10 (249 дней), реально Feb 17 – Mar 3 и
//    Sep 15 – 29 (30 дней двумя окнами). Окна были шире реальных в 8–16 раз.
//
// 2. Было ОДНО действие «посев». Календарь оперирует тремя: рассада дома →
//    высадка → прямой посев. У томата, перца и баклажана прямого посева нет
//    вовсе, а приложение предлагало сеять их в грунт.
//
// 3. Весеннее смещение считалось булевым cool (−28 дней или 0). Теперь класс
//    морозостойкости: hardy −4…−2 недели, half 0…+2, tender +2…+4. Правило
//    сверено с опубликованными датами для Остина и Чикаго — совпало день в день.
//
// 4. Осеннее окно раньше не существовало. Оно кончается за fallWeeks недель до
//    ПЕРВЫХ заморозков. Проверка: смещение, снятое с Остина, предсказало Чикаго
//    по 11 культурам без единого расхождения — значит окно зависит только от
//    даты заморозков и константы культуры.
//
// Известное ограничение, оно проговорено на экране: модель работает от
// заморозков, а не от летней жары. Крайний срок весеннего посева у
// холодостойких задан классом, а не выведен из температуры, поэтому в жарком
// регионе край окна поплывёт. Температурную модель выдумывать нельзя.

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
export const today = () => dayOffset(TODAY)

export const zipInfo = (zip: string): Zip => ZIPS.find(z => z.zip === zip) || ZIPS[0]

const parseMD = (s: string) => {
  const [m, d] = s.split(' ')
  return new Date(2026, MON.indexOf(m), +d)
}

export interface Frost { last: Date; first: Date }
export function frostDates(zip: string): Frost {
  const z = zipInfo(zip)
  return { last: parseMD(z.last), first: parseMD(z.first) }
}
/** Длина безморозного сезона считается из двух дат, а не хранится числом. */
export const seasonDays = (zip: string) => {
  const f = frostDates(zip)
  return Math.round((+f.first - +f.last) / 86400000)
}

export interface Ctx {
  zip: string
  /** false = в помещении: заморозков нет, значит нет и календарного окна. */
  outdoor: boolean
}

export type Range = [Date, Date]
export interface Window {
  /** рассада дома */
  indoors?: Range
  /** высадка рассады в грунт */
  plant?: Range
  /** прямой посев весной */
  sow?: Range
  /** прямой посев второй волной, в конце лета */
  fall?: Range
  /** сбор от весеннего входа и от осеннего */
  pick?: Range
  fallPick?: Range
  /** сезона нет вовсе: лоток на подоконнике, годится любой месяц */
  any?: boolean
}

/** смещения от последних заморозков, в неделях */
const SPRING: Record<string, [number, number]> = {
  hardy: [-4, -2], half: [0, 2], tender: [2, 4],
}
const PLANT: Record<string, [number, number]> = {
  hardy: [-4, -3], half: [0, 1], tender: [2, 3],
}

const addD = (d: Date, n: number) => { const x = new Date(d); x.setDate(x.getDate() + n); return x }
const wk = (d: Date, n: number) => addD(d, n * 7)

// Прототип живёт внутри одного календарного года. У холодного ZIP окно рассады
// уезжает за 1 января: в Портленде салат, капуста и перец начинаются 26 декабря
// ПРОШЛОГО года, и диапазон получается вывернутым — конец раньше начала.
// Подрезаем по границам года: пара дней точности против невозможной полосы.
const Y0 = new Date(2026, 0, 1), Y1 = new Date(2026, 11, 31)
const clip = (r: Range): Range | undefined => {
  const a = r[0] < Y0 ? Y0 : r[0] > Y1 ? Y1 : r[0]
  const b = r[1] > Y1 ? Y1 : r[1] < Y0 ? Y0 : r[1]
  return b < a ? undefined : [a, b]
}

export function windows(sp: Species, ctx: Ctx): Window | null {
  if (sp.kind === 'house') return null
  // В помещении заморозков нет — годится любой месяц. Раньше окна всё равно
  // считались от заморозков, и экран спорил сам с собой.
  if (!ctx.outdoor || sp.anyMonth) return { any: true }
  const h = sp.hardiness || 'tender'
  const f = frostDates(ctx.zip)
  const out: Window = {}

  if (sp.direct) {
    const [a, b] = SPRING[h]
    out.sow = [wk(f.last, a), wk(f.last, b)]
    out.pick = [addD(out.sow[0], sp.days), addD(out.sow[1], sp.daysMax)]
  }
  if (sp.transplant && sp.indoorsWeeks) {
    const [a, b] = PLANT[h]
    out.plant = [wk(f.last, a), wk(f.last, b)]
    out.indoors = clip([addD(out.plant[0], -sp.indoorsWeeks[0] * 7),
                        addD(out.plant[0], -sp.indoorsWeeks[1] * 7)])
    const p: Range = [addD(out.plant[0], sp.days), addD(out.plant[1], sp.daysMax)]
    out.pick = out.pick
      ? [new Date(Math.min(+out.pick[0], +p[0])), new Date(Math.max(+out.pick[1], +p[1]))]
      : p
  }
  if (sp.fallWeeks != null) {
    const end = addD(f.first, -sp.fallWeeks * 7)
    out.fall = [addD(end, -sp.fallSpan), end]
    out.fallPick = [addD(out.fall[0], sp.days), addD(out.fall[1], sp.daysMax)]
  }
  return Object.keys(out).length ? out : null
}

/** Все входы в грунт и в лоток — одним списком, для «что делать в этом месяце». */
export const entries = (w: Window | null): Range[] =>
  !w || w.any ? [] : [w.indoors, w.plant, w.sow, w.fall].filter(Boolean) as Range[]

export const live = (r: Range | undefined, now: Date) => !!r && now >= r[0] && now <= r[1]
export const ahead = (r: Range | undefined, now: Date) => !!r && now < r[0]

/** Ближайшее окно в будущем — им сортируется лента и им подписывается напоминание. */
export function nextWin(w: Window | null, now: Date): Range | undefined {
  if (!w) return undefined
  return entries(w).filter(r => r[0] > now).sort((a, b) => +a[0] - +b[0])[0]
}

const monthsOf = (a: Date, b: Date) => {
  const out: Record<number, 1> = {}
  const d = new Date(a.getFullYear(), a.getMonth(), 1)
  while (d <= b) { out[d.getMonth()] = 1; d.setMonth(d.getMonth() + 1) }
  return out
}

export type MonthKind = 'sow' | 'pick' | 'both' | ''

// Кэш: пикер месяцев спрашивает monthMap 12x29 раз за перерисовку, а ответ
// меняется только от ZIP и от «на улице или нет».
let CACHE: Record<string, MonthKind[] | null> = {}
let CACHE_KEY = ''

export function monthMap(sp: Species, ctx: Ctx): MonthKind[] | null {
  const key = `${ctx.zip}|${ctx.outdoor ? 1 : 0}`
  if (key !== CACHE_KEY) { CACHE_KEY = key; CACHE = {} }
  if (sp.id in CACHE) return CACHE[sp.id]
  const w = windows(sp, ctx)
  let out: MonthKind[] | null = null
  if (w && !w.any) {
    // именно entries(): рассада на подоконнике — тоже действие этого месяца.
    // Без неё у перца Остин и Чикаго давали одинаковую карту, потому что
    // различались они только месяцем лотка.
    const sowR = entries(w)
    const pickR = [w.pick, w.fallPick].filter(Boolean) as Range[]
    const sow: Record<number, 1> = {}
    const pick: Record<number, 1> = {}
    sowR.forEach(r => Object.assign(sow, monthsOf(r[0], r[1])))
    pickR.forEach(r => Object.assign(pick, monthsOf(r[0], r[1])))
    out = MON1.map((_, m) => {
      if (sow[m] && pick[m]) return 'both'   // и сажать можно, и что-то снимаешь
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
  // Съедобное без сезона (подоконник, микрозелень) сажается в любой месяц, а
  // «снимать в таком-то месяце» без сезона не определено — счёт идёт от посева.
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

/** Порядок — по первому входу в грунт: строки складываются в каскад. */
export function calSort(list: Species[], ctx: Ctx): Species[] {
  const first = (sp: Species) => {
    const e = entries(windows(sp, ctx))
    return e.length ? Math.min(...e.map(r => +r[0])) : Infinity
  }
  return list.slice().sort((a, b) => (first(a) - first(b)) || a.name.localeCompare(b.name))
}

// В месячном виде полезен другой порядок: не каскад окон, а «что даст урожай
// раньше» — число дней стоит на самой плитке.
export const byDays = (list: Species[]) =>
  list.slice().sort((a, b) =>
    (a.days - b.days) || (a.daysMax - b.daysMax) || a.name.localeCompare(b.name))

export const fmtMD = (d: Date) => `${MON[d.getMonth()]} ${d.getDate()}`
/** Диапазон без повтора месяца: «Feb 18–Mar 4», но «Apr 1–15». */
export const fmtRange = (r: Range | undefined) =>
  !r ? null
    : r[0].getMonth() === r[1].getMonth()
      ? `${MON[r[0].getMonth()]} ${r[0].getDate()}–${r[1].getDate()}`
      : `${fmtMD(r[0])}–${fmtMD(r[1])}`
export const spDays = (sp: Species) =>
  sp.days + (sp.daysMax !== sp.days ? `–${sp.daysMax}` : '')
export { addD }
export const daysBetween = (a: Date, b: Date) => Math.round((+b - +a) / 86400000)

/** Позиция даты на оси года в процентах — из этого считаются длины полос. */
export const pctY = (d: Date) =>
  Math.max(0, Math.min(100, (+d - +new Date(2026, 0, 1)) / 86400000 / 365 * 100))
