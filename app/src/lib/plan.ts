// Мини-движок плана. Порядок правил важен и повторяет proto.py:
// сначала отбор по свету и скоринг, потом три обязательства — трек both даёт
// и то и другое, съедобный трек даёт хотя бы одну быструю культуру, каждая
// заявленная цель представлена. Иначе человек просит томаты, получает пять
// салатов и не понимает почему.

import { GOALWORD, SUNNEED, type Track } from '../data/onboarding'
import type { Species } from '../data/species'
import { lc } from './plants'
import { speciesPool, zipInfo } from './season'

export interface PlanCtx {
  track: Track
  outdoor: boolean
  sunRank: number
  sun: string
  space: string
  goals: string[]
  effort: number
  zip: string
}

export const fitsLight = (s: Species, sunRank: number) => s.sun <= sunRank
export const pool = (c: PlanCtx) => speciesPool({ track: c.track, outdoor: c.outdoor })
export const anA = (w: string) => (/^[aeiou]/i.test(w) ? 'an ' : 'a ') + w
export const inOn = (outdoor: boolean) => (outdoor ? 'on your ' : 'in your ')
export const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1)
export const inDays = (n: number) => (n <= 0 ? 'today' : n === 1 ? 'tomorrow' : `in ${n} days`)
export const seasonWeeks = (zip: string) => Math.round(zipInfo(zip).season / 7)

const MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export function dateAfter(days: number) {
  const d = new Date(2026, 2, 14)
  d.setDate(d.getDate() + days)
  return `${MONTH[d.getMonth()]} ${d.getDate()}`
}

export function buildPlan(c: PlanCtx): Species[] {
  const g = c.goals
  const n = c.effort
  let p = pool(c).filter(s => fitsLight(s, c.sunRank))
  if (!p.length) p = pool(c)
  const score = (s: Species) =>
    s.tags.filter(t => g.indexOf(t) > -1).length * 40
    + (s.kind === 'edible' && s.days <= 35 ? 20 : 0)
    + (s.kind === 'house' ? (s.water >= 12 ? 14 : 6) : 0)
    + (s.kind === 'edible' ? (120 - s.daysMax) / 12 : 0)
  p = p.slice().sort((a, b) => score(b) - score(a))

  const out: Species[] = []
  for (let i = 0; i < p.length && out.length < n; i++) {
    const s = p[i]
    // не даём плану превратиться в три долгих культуры
    if (s.kind === 'edible' && s.days > 70 && out.filter(x => x.days > 70).length >= 2) continue
    out.push(s)
  }
  // трек both обязан дать и то, и другое
  if (c.track === 'both') {
    (['house', 'edible'] as const)
      .filter(k => !out.some(s => s.kind === k))
      .forEach(k => {
        const add = p.find(s => s.kind === k)
        if (add) { out.pop(); out.unshift(add) }
      })
  }
  // съедобный трек обязан дать хотя бы одну быструю культуру
  if (c.track === 'edible' && !out.some(s => s.days <= 35)) {
    const f = p.find(s => s.days <= 35)
    if (f) { out.pop(); out.unshift(f) }
  }
  // каждая заявленная цель обязана быть представлена, если по свету это возможно
  g.forEach(tag => {
    if (out.some(s => s.tags.indexOf(tag) > -1)) return
    const cand = p.find(s => s.tags.indexOf(tag) > -1)
    if (!cand) return
    let victim = -1
    for (let i = out.length - 1; i >= 0; i--) {
      const covers = out[i].tags.filter(t => g.indexOf(t) > -1)
      const spare = covers.every(t => out.some((x, k) => k !== i && x.tags.indexOf(t) > -1))
      if (spare) { victim = i; break }
    }
    if (victim < 0 && out.length >= n) victim = out.length - 1
    if (victim >= 0) out.splice(victim, 1)
    out.push(cand)
  })
  return out
}

const listWords = (a: string[]) =>
  a.map(x => GOALWORD[x] || x)
   .reduce((s, x, i, arr) => s + (i === 0 ? '' : i === arr.length - 1 ? ' and ' : ', ') + x, '')

/**
 * Блок «Why these» под планом. Он обязан объяснять и отказы: если цель не
 * попала, честно говорим почему — не хватает света, такого мы не выращиваем
 * или не влезло в размер плана.
 */
export function planWhy(plan: Species[], c: PlanCtx): string {
  const got: Record<string, 1> = {}
  plan.forEach(s => s.tags.forEach(t => { got[t] = 1 }))
  const asked = c.goals.length ? c.goals : (c.track === 'edible' ? ['fast'] : ['hardy'])
  const missed = asked.filter(t => !got[t])
  const edible = plan.filter(s => s.kind === 'edible')

  let t = `<b>Why these:</b> you asked for ${listWords(asked)}, and ${c.sun}`
        + ' is what decides the rest. '
  const fast = edible.length ? edible.reduce((a, b) => (b.days < a.days ? b : a)) : null
  const tough = plan.filter(s => s.kind === 'house').sort((a, b) => b.water - a.water)[0]
  t += fast ? `${fast.name} is your fast win — ready in ${fast.days} days.`
            : tough ? `${tough.name} is the forgiving one — it only needs water every `
                      + `${tough.water} days.` : ''

  if (missed.length) {
    const all = pool(c)
    const exists = (tag: string) => all.some(s => s.tags.indexOf(tag) > -1)
    const lit = (tag: string) => all.some(s => s.tags.indexOf(tag) > -1 && fitsLight(s, c.sunRank))
    const dark = missed.filter(tag => exists(tag) && !lit(tag))
    const absent = missed.filter(tag => !exists(tag))
    const tight = missed.filter(tag => dark.indexOf(tag) < 0 && absent.indexOf(tag) < 0)
    let w = ''
    if (dark.length) {
      const need = dark.map(m => SUNNEED[m]).filter(Boolean)[0]
      w += cap(listWords(dark))
         + (need ? ` need ${need} of direct sun. At your light they rarely finish, so we left `
                 : ' need more light than you have, so we left ')
         + (dark.length > 1 ? 'them' : 'it') + ' out. '
    }
    if (absent.length) {
      w += cap(listWords(absent)) + (absent.length > 1 ? ' are' : ' is')
         + ' not something we grow ' + (c.outdoor ? 'in containers' : 'indoors') + ' yet. '
    }
    if (tight.length) {
      w += cap(listWords(tight)) + ` didn’t fit in ${plan.length} plants — ask for more `
         + 'time a week and ' + (tight.length > 1 ? 'they' : 'it') + ' come'
         + (tight.length > 1 ? '' : 's') + ' in. '
    }
    w += `You can add ${missed.length > 1 ? 'them' : 'it'} by hand any time.`
    t += `<span class="warn">${w}</span>`
  }
  return t
}

/** Подпись строки вида в библиотеке и плане. */
export const spSub = (s: Species, units: 'imperial' | 'metric',
                      fmtPot: (v: string, u: 'imperial' | 'metric') => string) =>
  s.kind === 'edible'
    ? `${s.days}${s.daysMax !== s.days ? '–' + s.daysMax : ''} days · ${fmtPot(s.pot, units)}`
    : `Water every ${s.water}d · ${s.light}`

export const listNames = (names: string[]) =>
  names.length > 1
    ? `${names.slice(0, -1).join(', ')} and ${names[names.length - 1]}`
    : names[0] || ''

export const lcName = lc
