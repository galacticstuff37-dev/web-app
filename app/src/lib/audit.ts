// Аудит модели сезона. Тот же набор проверок, что гонялся на прототипе, но
// против портированного кода: если порт разошёлся с моделью, это видно числом,
// а не на глаз.
//
// Вызывается из консоли: window.__audit(). Держим в бандле намеренно — это
// страховка порта, а не отладочный мусор: 29 видов x 4 региона x 12 месяцев
// руками не проверить.

import { SPECIES } from '../data/species'
import { ZIPS } from '../data/zips'
import {
  calSort, frostDates, inWin, isHousePool, monthMap, nowMonth, pctY, pickableIn,
  sowableIn, speciesPool, windows, zipInfo, type Ctx,
} from './season'
import {
  careStats as careStatsRef, verdict as verdictRef, weekTasks as weekTasksRef,
} from './plants'

const DAY = 86400000

export function audit(): string {
  const out: string[] = []
  let fail = 0
  const bad = (m: string) => { fail++; out.push('FAIL ' + m) }

  for (const z of ZIPS) {
    const ctx: Ctx = { zip: z.zip, outdoor: true }
    const f = frostDates(z.zip)
    const pool = speciesPool({ track: 'edible', outdoor: true })
    if (!pool.length) bad(z.zip + ' пустой пул')

    for (const sp of pool) {
      const w = windows(sp, ctx)
      if (!w) { bad(`${z.zip} ${sp.id} нет окна на улице`); continue }
      if (w.tight) { out.push(`NOTE tight: ${z.zip} ${sp.id}`); continue }

      // старт окна посева: холодостойкие за 28 дней до заморозков
      const wantStart = new Date(f.last)
      if (sp.cool) wantStart.setDate(wantStart.getDate() - 28)
      if (+w.sow[0] !== +wantStart) bad(`${z.zip} ${sp.id} старт посева`)

      // крайний срок: успеть отдать урожай до осенних заморозков
      const wantEnd = new Date(f.first)
      wantEnd.setDate(wantEnd.getDate() - sp.daysMax - 14)
      if (+w.sow[1] !== +wantEnd) bad(`${z.zip} ${sp.id} крайний срок посева`)

      // окно сбора = посев + дни до урожая
      if (Math.round((+w.pick[0] - +w.sow[0]) / DAY) !== sp.days) bad(`${z.zip} ${sp.id} старт сбора`)
      if (Math.round((+w.pick[1] - +w.sow[1]) / DAY) !== sp.daysMax) bad(`${z.zip} ${sp.id} конец сбора`)
      if (w.sow[1] < w.sow[0]) bad(`${z.zip} ${sp.id} окно посева вывернуто`)
      if (w.pick[1] < w.pick[0]) bad(`${z.zip} ${sp.id} окно сбора вывернуто`)

      // monthMap согласован с windows по каждому месяцу
      const mm = monthMap(sp, ctx)!
      for (let m = 0; m < 12; m++) {
        const a = new Date(2026, m, 1), b = new Date(2026, m + 1, 0)
        const sowHit = w.sow[0] <= b && w.sow[1] >= a
        const pickHit = w.pick[0] <= b && w.pick[1] >= a
        const want = sowHit && pickHit ? 'both' : sowHit ? 'sow' : pickHit ? 'pick' : ''
        if (mm[m] !== want) bad(`${z.zip} ${sp.id} месяц ${m}: ${mm[m]} вместо ${want}`)
      }

      // полосы не выходят за ось года
      const l = pctY(w.sow[0]), r = pctY(w.pick[1])
      if (l < 0 || l > 100 || r < 0 || r > 100) bad(`${z.zip} ${sp.id} полоса за осью`)
      if (pctY(w.sow[1]) < l) bad(`${z.zip} ${sp.id} полоса вывернута`)

      // sowableIn / pickableIn согласованы с monthMap
      for (let m = 0; m < 12; m++) {
        const inSow = sowableIn(m, pool, ctx).indexOf(sp) > -1
        if (inSow !== (mm[m] === 'sow' || mm[m] === 'both')) bad(`${z.zip} ${sp.id} sowableIn ${m}`)
        const inPick = pickableIn(m, pool, ctx).indexOf(sp) > -1
        if (inPick !== (mm[m] === 'pick' || mm[m] === 'both')) bad(`${z.zip} ${sp.id} pickableIn ${m}`)
      }
    }

    // сортировка не убывает по старту окна
    const srt = calSort(pool, ctx)
    for (let i = 1; i < srt.length; i++) {
      const a = windows(srt[i - 1], ctx), b = windows(srt[i], ctx)
      if (a && b && +a.sow[0] > +b.sow[0]) bad(`${z.zip} порядок сортировки на ${i}`)
    }
    out.push(`${z.zip} ${zipInfo(z.zip).city.split(',')[0]} frost ${z.frost}`
      + ` sowNow=${sowableIn(nowMonth(), pool, ctx).length}`
      + ` pickNow=${pickableIn(nowMonth(), pool, ctx).length}`)
  }

  // в помещении сезона нет ни у кого
  const ictx: Ctx = { zip: '78704', outdoor: false }
  const ip = speciesPool({ track: 'edible', outdoor: false })
  if (!ip.length) bad('пустой пул в помещении')
  for (const sp of ip) {
    if (windows(sp, ictx) !== null) bad(`indoor ${sp.id} имеет окно`)
    if (monthMap(sp, ictx) !== null) bad(`indoor ${sp.id} имеет monthMap`)
  }
  for (let m = 0; m < 12; m++) {
    if (sowableIn(m, ip, ictx).length !== ip.length) bad(`indoor sowableIn ${m}`)
    if (pickableIn(m, ip, ictx).length !== 0) bad(`indoor pickableIn ${m}`)
  }
  if (isHousePool(ip)) bad('съедобное в помещении помечено как комнатное')
  out.push(`indoor pool=${ip.length} allMonthsSowable=yes`)

  // трек комнатных
  const hp = speciesPool({ track: 'house', outdoor: false })
  if (!isHousePool(hp)) bad('трек комнатных не распознан')
  for (const sp of hp) if (monthMap(sp, ictx) !== null) bad(`house ${sp.id} monthMap`)
  if (sowableIn(3, hp, ictx).length !== 0) bad('house sowableIn не пуст')
  out.push(`house pool=${hp.length} calHouse=yes`)

  // кэш инвалидируется по ZIP
  const a = monthMap(SPECIES.find(x => x.id === 'pepper')!, { zip: '78704', outdoor: true })!.join('')
  const b = monthMap(SPECIES.find(x => x.id === 'pepper')!, { zip: '60613', outdoor: true })!.join('')
  if (a === b) bad('кэш monthMap не инвалидируется при смене ZIP')
  out.push('cache invalidates on zip: yes')

  // inWin для комнатного не должен считаться посевом
  const mon = SPECIES.find(x => x.id === 'monstera')!
  if (inWin(mon, 3, 'sow', ictx)) bad('комнатное попало в sowable')

  return (fail ? `FAILURES=${fail} :: ` : 'ALL LOGIC CHECKS PASS :: ') + out.join(' | ')
}

declare global {
  interface Window { __audit?: () => string }
}
if (typeof window !== 'undefined') window.__audit = audit

// Слепок чисел ухода: сверяется напрямую с careStats()/weekTasks() прототипа.
// Держим рядом с аудитом сезона — это та же страховка, только про растения.
export function stats(plants: import('./plants').Plant[]) {
  const cs = careStatsRef(plants)
  return JSON.stringify({
    ...cs,
    verdict: verdictRef(cs.score, cs.due),
    tasks: weekTasksRef(plants).map(t => t[0]),
  })
}
declare global {
  interface Window { __stats?: (p: import('./plants').Plant[]) => string }
}
