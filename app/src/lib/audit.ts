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
  calSort, entries, frostDates, inWin, isHousePool, monthMap, nowMonth, pctY, pickableIn,
  sowableIn, speciesPool, windows, zipInfo, type Ctx, type Range,
} from './season'

/** смещения весеннего окна — дублируются здесь намеренно: аудит должен
    проверять модель независимо, а не переиспользовать её же константу */
const SPRING: Record<string, [number, number]> = {
  hardy: [-4, -2], half: [0, 2], tender: [2, 4],
}
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
      if (w.any) { out.push(`NOTE no season: ${sp.id}`); continue }
      if (!entries(w).length) { bad(`${z.zip} ${sp.id} ни одного входа в грунт`); continue }

      // весеннее окно: смещение задано классом морозостойкости, а не булевым cool
      if (sp.direct) {
        if (!w.sow) bad(`${z.zip} ${sp.id} direct без окна посева`)
        else {
          const [ka, kb] = SPRING[sp.hardiness || 'tender']
          const wantA = new Date(f.last); wantA.setDate(wantA.getDate() + ka * 7)
          const wantB = new Date(f.last); wantB.setDate(wantB.getDate() + kb * 7)
          if (+w.sow[0] !== +wantA) bad(`${z.zip} ${sp.id} старт весеннего окна`)
          if (+w.sow[1] !== +wantB) bad(`${z.zip} ${sp.id} конец весеннего окна`)
        }
      } else if (w.sow) bad(`${z.zip} ${sp.id} прямого посева нет, а окно есть`)

      // рассада: высадка привязана к заморозкам, лоток — к высадке
      if (sp.transplant) {
        if (!w.plant || !w.indoors) bad(`${z.zip} ${sp.id} transplant без окон`)
        else {
          // Начало могло быть подрезано 1 января (холодный ZIP), поэтому
          // сверяем КОНЕЦ: он за indoorsWeeks[1] недель до высадки всегда.
          const back = Math.round((+w.plant[0] - +w.indoors[1]) / DAY / 7)
          if (back !== sp.indoorsWeeks![1]) bad(`${z.zip} ${sp.id} недель до высадки`)
          if (w.indoors[1] < w.indoors[0]) bad(`${z.zip} ${sp.id} окно рассады вывернуто`)
          if (+w.indoors[0] < +new Date(2026, 0, 1)) bad(`${z.zip} ${sp.id} рассада до 1 января`)
        }
      } else if (w.plant) bad(`${z.zip} ${sp.id} высадка без рассады`)

      // осеннее окно кончается за fallWeeks недель до ПЕРВЫХ заморозков
      if (sp.fallWeeks != null) {
        if (!w.fall) bad(`${z.zip} ${sp.id} нет осеннего окна`)
        else {
          const wantEnd = new Date(f.first)
          wantEnd.setDate(wantEnd.getDate() - sp.fallWeeks * 7)
          if (+w.fall[1] !== +wantEnd) bad(`${z.zip} ${sp.id} конец осеннего окна`)
          if (Math.round((+w.fall[1] - +w.fall[0]) / DAY) !== sp.fallSpan)
            bad(`${z.zip} ${sp.id} ширина осеннего окна`)
        }
      } else if (w.fall) bad(`${z.zip} ${sp.id} осеннее окно из ниоткуда`)

      // сбор считается от входа
      if (w.sow && w.pick && Math.round((+w.pick[0] - +w.sow[0]) / DAY) !== sp.days)
        bad(`${z.zip} ${sp.id} старт сбора`)
      for (const r of entries(w)) if (r[1] < r[0]) bad(`${z.zip} ${sp.id} окно вывернуто`)

      // между весной и осенью обязан быть разрыв: одно непрерывное окно —
      // это ровно тот баг, из-за которого салат «сеялся» девять месяцев
      if (w.sow && w.fall && +w.fall[0] <= +w.sow[1])
        bad(`${z.zip} ${sp.id} волны склеились в одно окно`)

      // monthMap согласован с окнами по каждому месяцу
      const mm = monthMap(sp, ctx)!
      const hit = (rs: (Range | undefined)[], a2: Date, b2: Date) =>
        rs.some(r => !!r && r[0] <= b2 && r[1] >= a2)
      for (let m = 0; m < 12; m++) {
        const a2 = new Date(2026, m, 1), b2 = new Date(2026, m + 1, 0)
        const sowHit = hit([w.indoors, w.plant, w.sow, w.fall], a2, b2)
        const pickHit = hit([w.pick, w.fallPick], a2, b2)
        const want = sowHit && pickHit ? 'both' : sowHit ? 'sow' : pickHit ? 'pick' : ''
        if (mm[m] !== want) bad(`${z.zip} ${sp.id} месяц ${m}: ${mm[m]} вместо ${want}`)
      }

      // полосы не выходят за ось года
      for (const r of entries(w)) {
        if (pctY(r[0]) < 0 || pctY(r[1]) > 100) bad(`${z.zip} ${sp.id} полоса за осью`)
      }

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
      const ea = entries(windows(srt[i - 1], ctx)), eb = entries(windows(srt[i], ctx))
      if (ea.length && eb.length
          && Math.min(...ea.map(r => +r[0])) > Math.min(...eb.map(r => +r[0])))
        bad(`${z.zip} порядок сортировки на ${i}`)
    }
    out.push(`${z.zip} ${zipInfo(z.zip).city.split(',')[0]} frost ${z.last}`
      + ` sowNow=${sowableIn(nowMonth(), pool, ctx).length}`
      + ` pickNow=${pickableIn(nowMonth(), pool, ctx).length}`)
  }

  // в помещении сезона нет ни у кого
  const ictx: Ctx = { zip: '78704', outdoor: false }
  const ip = speciesPool({ track: 'edible', outdoor: false })
  if (!ip.length) bad('пустой пул в помещении')
  for (const sp of ip) {
    if (!windows(sp, ictx)?.any) bad(`indoor ${sp.id} должен быть без сезона`)
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
  // join(',') а не join(''): пустые месяцы схлопывались, и две РАЗНЫЕ карты
  // (Остин sow в янв+апр, Чикаго в фев+мае) давали одну строку 'sowsowpickpick'
  const a = monthMap(SPECIES.find(x => x.id === 'pepper')!, { zip: '78704', outdoor: true })!.join(',')
  const b = monthMap(SPECIES.find(x => x.id === 'pepper')!, { zip: '60613', outdoor: true })!.join(',')
  if (a === b) bad(`кэш monthMap не инвалидируется при смене ZIP: ${a} == ${b}`)
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
