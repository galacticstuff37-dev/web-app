// Синхронизация между устройствами. Postgres здесь НЕ источник правды для
// экранов: приложение остаётся local-first, все 32 экрана рисуются из
// localStorage мгновенно и без сети. База — вторая копия и способ довезти
// изменения до другого устройства. Поэтому здесь нет ни одного состояния
// «загружается» и ни одного «не удалось»: неудачная синхронизация ничего не
// показывает человеку, а просто повторится в следующий раз.
//
// Как решается, кто прав. У строк в базе есть updated_at, но у локальных
// растений его нет и заводить его в состоянии значило бы тащить служебное поле
// через весь продукт. Вместо этого рядом с состоянием лежит СНИМОК последней
// отправки: ключ строки → отпечаток её синхронизируемых полей. Отсюда всё:
//   * отпечаток не совпал или ключа в снимке нет → строку меняли здесь, она
//     «грязная», и на слиянии выигрывает локальная версия;
//   * ключ в снимке есть, а строки локально нет → её здесь удалили, значит в
//     базе ставим deleted_at;
//   * ключа нет ни там, ни там → строка чужая (её завели на другом
//     устройстве), молча берём версию из базы.
// Тот же снимок отвечает на вопрос «удалить в базе или это ещё не приехало»:
// без него полная отправка сносила бы всё, что успели добавить с телефона.
//
// Тянем ВСЁ и каждый раз, без водяного знака по updated_at. У человека десятки
// строк, это несколько килобайт, зато нет расхождения локальных и серверных
// часов — самого противного класса ошибок в синхронизации.

import type { SupabaseClient } from '@supabase/supabase-js'
import { REMIND_AT } from '../data/onboarding'
import { SP } from '../data/species'
import type { Track } from '../data/onboarding'
import { isDemoGarden } from '../state/store'
import type { CalView, Pulled, State, Units } from '../state/store'
import { mkPlant, type Photo, type Plant } from './plants'

// ───────────────────────────────────────────── снимок последней отправки

const SNAP_KEY = 'hg.sync'
const SNAP_VER = 1

export interface Snap {
  v: number
  uid: string
  rows: Record<string, string>
  /** когда проход в последний раз прошёл целиком, ISO. Экран аккаунта этим и
      отвечает на «когда синхронизировалось»; поле необязательное, потому что в
      снимках, записанных до него, его нет. */
  at?: string
}

/** Снимок чужого аккаунта не читаем: у него другие id строк. */
function readSnap(uid: string): Snap | null {
  try {
    const raw = localStorage.getItem(SNAP_KEY)
    if (!raw) return null
    const j = JSON.parse(raw) as Snap
    if (j.v !== SNAP_VER || j.uid !== uid) return null
    return { v: j.v, uid: j.uid, rows: j.rows || {}, at: j.at }
  } catch { return null }
}

function writeSnap(uid: string, rows: Record<string, string>, at: string): void {
  try {
    localStorage.setItem(SNAP_KEY, JSON.stringify({ v: SNAP_VER, uid, rows, at }))
  } catch { /* приватный режим: синхронизация станет отправлять лишнее, не более */ }
}

/** Выход из аккаунта. Снимок чужого человека на этом устройстве не нужен. */
export function forgetSnap(): void {
  try { localStorage.removeItem(SNAP_KEY) } catch { /* приватный режим */ }
}

// Ключи строк в снимке. Префикс, потому что карта одна на все таблицы.
const PK = (id: string) => 'p:' + id
// Порядок отдельным ключом, а не внутри отпечатка растения: сдвиг соседа не
// должен читаться как «растение меняли здесь» и выигрывать слияние.
const SK = (id: string) => 's:' + id
const FK = (id: string) => 'f:' + id
const TK = (week: string, key: string) => 't:' + week + '|' + key
const UK = 'u:'

const plantFp = (p: Plant) => `${p.s.id}|${p.since}|${p.day}`
const photoFp = (x: Photo, plant: string) => `${plant}|${x.f || ''}|${x.day}`

// ───────────────────────────────────────────── неделя

/**
 * Понедельник текущей недели, YYYY-MM-DD по МЕСТНОЙ дате. Неделя входит в
 * первичный ключ отметок: ключ задачи в клиенте (water:0) живёт одну неделю, и
 * без даты прошлые галочки гасили бы задачи следующей.
 */
export function weekStart(now = new Date()): string {
  const d = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7))     // 0=вс → 6, 1=пн → 0
  const p2 = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p2(d.getMonth() + 1)}-${p2(d.getDate())}`
}

// ───────────────────────────────────────────── строки базы

export interface ProfileRow {
  id: string
  track: Track; space: string; outdoor: boolean; sun: string; sun_rank: number
  goals: string[]; effort: number; zip: string | null
  units: Units; cal_view: CalView; remind_at: string; tz: string
  care_pick: boolean; care_leaf: boolean; care_rotate: boolean; care_feed: boolean
  mail_weekly: boolean; mail_water: boolean; mail_news: boolean
  is_pro: boolean
  /** Срок Pro. Колонка есть в живой базе (0001_init.sql:71, проверено запросом
      select=pro_until). Тарифа рядом НЕТ: profiles.pro_plan не существует,
      поэтому название тарифа остаётся локальным. */
  pro_until: string | null
}
export interface PlantRow {
  id: string; user_id: string; species_id: string
  since: number; day: number; sort: number; deleted_at?: string | null
}
export interface PhotoRow {
  id: string; user_id: string; plant_id: string; kind: 'stock' | 'upload'
  stock_name: string | null; storage_path?: string | null
  day: number; deleted_at?: string | null
}
export interface TaskRow { user_id: string; week_start: string; task_key: string; done: boolean }

export interface Cloud {
  profile: ProfileRow | null
  plants: PlantRow[]
  photos: PhotoRow[]
  tasks: TaskRow[]
}

/** Часовой пояс человека: планировщик обязан попасть в 18:00 по месту, не по UTC. */
const tz = () => {
  try { return Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC' } catch { return 'UTC' }
}

export function profileOf(s: State, uid: string): ProfileRow {
  const c = s.choices
  return {
    id: uid,
    track: c.track,
    space: c.space,
    outdoor: c.outdoor,
    sun: c.sun,
    sun_rank: c.sunRank,
    goals: c.goals,
    effort: c.effort,
    // В базе на zip стоит проверка ^[0-9]{5}$. Мусор лучше не отправить вовсе,
    // чем уронить 400-й всю отправку вместе с растениями.
    zip: /^[0-9]{5}$/.test(c.zip) ? c.zip : null,
    units: s.units,
    cal_view: s.calView,
    remind_at: REMIND_AT[s.remind] || REMIND_AT[3],
    tz: tz(),
    care_pick: s.care.pick,
    care_leaf: s.care.leaf,
    care_rotate: s.care.rotate,
    care_feed: s.care.feed,
    mail_weekly: s.mail.weekly,
    mail_water: s.mail.water,
    mail_news: s.mail.news,
    is_pro: s.isPro,
    pro_until: s.proUntil,
  }
}

/** Отпечаток профиля: одна строка, поэтому просто перечисление полей. */
const profileFp = (r: ProfileRow) =>
  [r.track, r.space, r.outdoor, r.sun, r.sun_rank, r.goals.join(','), r.effort, r.zip,
   r.units, r.cal_view, r.remind_at, r.tz, r.care_pick, r.care_leaf, r.care_rotate,
   r.care_feed, r.mail_weekly, r.mail_water, r.mail_news, r.is_pro,
   r.pro_until].join('|')

// ───────────────────────────────────────────── слияние

export interface SyncReport {
  ok: boolean
  /** Не отказ, а «ещё не время»: без сессии или проход ни разу не запускался.
      Экран аккаунта не должен показывать это как сбой. */
  skipped?: 'no-session' | 'never-run'
  uid?: string
  /** первая синхронизация на этом устройстве: снимка ещё не было */
  first?: boolean
  /** что приехало из базы и было применено */
  pulled?: { plants: number; photos: number; tasks: number; profile: boolean }
  /** что уехало в базу */
  pushed?: { plants: number; photos: number; tasks: number; profile: boolean; gone: number }
  error?: string
}

interface Merged {
  /** null — база не привезла ничего нового, состояние трогать не нужно */
  pulled: Pulled | null
  /** локальное состояние ПОСЛЕ слияния: из него считается отправка */
  next: State
  counts: { plants: number; photos: number; tasks: number; profile: boolean }
}

/**
 * База → локальное состояние. Чистая функция: сеть уже отработала, дальше
 * только арифметика, и её можно прогнать тестом без браузера и без аккаунта.
 */
export function merge(s: State, c: Cloud, snap: Snap | null, week: string,
                      uid: string): Merged {
  const rows = snap?.rows || {}
  const zero = { plants: 0, photos: 0, tasks: 0, profile: false }

  const live = c.plants.filter(r => !r.deleted_at && SP(r.species_id))

  // Первый проход на этом устройстве — особый случай. Разбирается он двумя
  // вопросами: есть ли в базе сад и лежит ли локально витрина.
  //
  //   в базе сад + локально витрина → человек зашёл с нового браузера. Берём
  //     базу целиком: иначе демо-редиска уехала бы к нему в настоящий огород.
  //   в базе пусто → аккаунт только что создан в конце онбординга. В базе есть
  //     ТОЛЬКО строка профиля от триггера, со значениями по умолчанию. Тянуть
  //     её нельзя — она затрёт ответы онбординга. Всё локальное уедет отправкой.
  //   в базе сад + локально занесённое руками → человек прошёл онбординг и
  //     вошёл в СТАРЫЙ аккаунт. Его растения не выбрасываем: они уедут
  //     отправкой и встанут рядом с накопленными, а сад из базы приедет
  //     следующим проходом (снимок к тому времени уже есть).
  const first = !snap
  const takeCloud = first && live.length > 0 && isDemoGarden(s.plants)
  if (first && !takeCloud) return { pulled: null, next: s, counts: zero }

  const cloudById = new Map(live.map(r => [r.id, r]))
  const dead = new Set(c.plants.filter(r => r.deleted_at).map(r => r.id))

  // Снимки. Из базы приезжают только готовые кадры из /img: кадры с камеры
  // (data-URL) в базе пока не живут, и до переезда в Storage «нет в базе» для
  // них НЕ значит «удалён» — они просто остаются локальными.
  const photosOf = (plantId: string, local: Photo[]): Photo[] => {
    const byId = new Map(local.map(x => [x.id, x]))
    const out: Photo[] = local.filter(x => x.u)
    const seen = new Set<string>()
    c.photos.filter(r => r.plant_id === plantId).forEach(r => {
      seen.add(r.id)
      if (r.deleted_at || r.kind !== 'stock' || !r.stock_name) return
      const mine = byId.get(r.id)
      const dirty = !!mine && rows[FK(r.id)] !== undefined
                          && rows[FK(r.id)] !== photoFp(mine, plantId)
      out.push(dirty && mine ? mine : { id: r.id, f: r.stock_name, day: r.day })
    })
    // Локальный готовый кадр, которого в базе нет: ещё не отправлен (в снимке
    // его нет) — оставляем; был отправлен (в снимке есть) — значит удалён на
    // другом устройстве.
    local.forEach(x => {
      if (x.u || seen.has(x.id) || rows[FK(x.id)] !== undefined) return
      out.push(x)
    })
    return out.sort((a, b) => b.day - a.day)
  }

  let plants: Plant[]
  if (takeCloud) {
    plants = live.map(r => mkPlant(r.species_id, r.since, r.day, photosOf(r.id, []), r.id))
  } else {
    const kept: Plant[] = []
    s.plants.forEach(p => {
      const r = cloudById.get(p.id)
      if (!r) {
        // Нет в базе. Удалили на другом устройстве, если мы её когда-то
        // отправляли или пришла явная строка с deleted_at.
        if (dead.has(p.id) || rows[PK(p.id)] !== undefined) return
        kept.push({ ...p, photos: photosOf(p.id, p.photos) })
        return
      }
      const dirty = rows[PK(p.id)] !== undefined && rows[PK(p.id)] !== plantFp(p)
      const src = dirty ? p : { ...p, since: r.since, day: r.day }
      kept.push({ ...src, photos: photosOf(p.id, p.photos) })
    })
    const mine = new Set(s.plants.map(p => p.id))
    live.filter(r => !mine.has(r.id))
      .forEach(r => kept.push(mkPlant(r.species_id, r.since, r.day, photosOf(r.id, []), r.id)))
    plants = kept
  }

  // Порядок входит в ключи задач недели (water:0), поэтому расходиться между
  // устройствами ему нельзя. Ведущий — sort из базы; занесённое здесь и ещё не
  // уехавшее встаёт в конец, при равных sort порядок решает id.
  plants.sort((a, b) => (cloudById.get(a.id)?.sort ?? 1e6) - (cloudById.get(b.id)?.sort ?? 1e6)
                     || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0))

  const pulled: Pulled = {}
  const counts = { ...zero }
  // Считаем разницу по факту, а не по ходу слияния: так не забыть ни одну
  // ветку, и «ничего не изменилось» становится честным ответом. Без него
  // применение вызывало бы новый проход, а тот — новое применение.
  const same = (a: Plant, b: Plant) =>
    a.id === b.id && a.s.id === b.s.id && a.since === b.since && a.day === b.day
    && a.photos.length === b.photos.length
    && a.photos.every((x, i) => x.id === b.photos[i].id && x.f === b.photos[i].f
                             && x.u === b.photos[i].u && x.day === b.photos[i].day)
  if (plants.length !== s.plants.length || plants.some((p, i) => !same(p, s.plants[i]))) {
    pulled.plants = plants
    counts.plants = Math.abs(plants.length - s.plants.length)
      + plants.filter((p, i) => s.plants[i] && !same(p, s.plants[i])).length
    counts.photos = plants.reduce((n, p) => n + p.photos.length, 0)
      - s.plants.reduce((n, p) => n + p.photos.length, 0)
  }

  // ── отметки задач недели
  const done: Record<string, boolean> = { ...s.done }
  c.tasks.filter(r => r.week_start === week).forEach(r => {
    const has = Object.prototype.hasOwnProperty.call(s.done, r.task_key)
    const k = TK(week, r.task_key)
    // Сравниваем локальное с ОТПРАВЛЕННЫМ, и «ничего не отправляли» — такое же
    // значение, как любое другое. Иначе поставленная здесь и ещё не уехавшая
    // галочка (в снимке ключа нет) затиралась бы старым значением из базы.
    const mine = has ? (s.done[r.task_key] ? '1' : '0') : undefined
    if (rows[k] !== mine) return
    if (!has || s.done[r.task_key] !== r.done) { done[r.task_key] = r.done; counts.tasks++ }
  })
  if (counts.tasks) pulled.done = done

  // ── профиль
  if (c.profile) {
    const mineFp = profileFp(profileOf(s, uid))
    const dirty = rows[UK] !== undefined && rows[UK] !== mineFp
    if (!dirty && profileFp(c.profile) !== mineFp) {
      const r = c.profile
      const ri = REMIND_AT.indexOf(String(r.remind_at).slice(0, 5))
      pulled.choices = {
        track: r.track, space: r.space, outdoor: r.outdoor, sun: r.sun,
        sunRank: r.sun_rank, goals: r.goals || [], effort: r.effort,
        zip: r.zip || s.choices.zip,
      }
      pulled.units = r.units
      pulled.calView = r.cal_view
      pulled.isPro = r.is_pro
      pulled.proUntil = r.pro_until
      if (ri > -1) pulled.remind = ri
      pulled.care = { pick: r.care_pick, leaf: r.care_leaf,
                      rotate: r.care_rotate, feed: r.care_feed }
      pulled.mail = { weekly: r.mail_weekly, water: r.mail_water, news: r.mail_news }
      counts.profile = true
    }
  }

  const any = Object.keys(pulled).length > 0
  return { pulled: any ? pulled : null, next: any ? applyTo(s, pulled) : s, counts }
}

/** То же, что делает case 'pulled' в редьюсере. Отправка считается из next. */
function applyTo(s: State, p: Pulled): State {
  const plants = p.plants ?? s.plants
  return {
    ...s, ...p, plants,
    choices: p.choices ? { ...s.choices, ...p.choices } : s.choices,
    selected: Math.min(s.selected, Math.max(0, plants.length - 1)),
  }
}

// ───────────────────────────────────────────── отправка

/** Отпечатки состояния: и для сравнения на слиянии, и для нового снимка. */
export function fingerprints(s: State, uid: string, week: string): Record<string, string> {
  const out: Record<string, string> = {}
  s.plants.forEach((p, i) => {
    out[PK(p.id)] = plantFp(p)
    out[SK(p.id)] = String(i)
    p.photos.forEach(x => { if (!x.u) out[FK(x.id)] = photoFp(x, p.id) })
  })
  Object.keys(s.done).forEach(k => { out[TK(week, k)] = s.done[k] ? '1' : '0' })
  out[UK] = profileFp(profileOf(s, uid))
  return out
}

// ───────────────────────────────────────────── один проход

/** Шаг отправки. Обёртка нужна только чтобы собрать шаги в список и не
    расписывать обработку ошибки у каждого. */
type Step = () => PromiseLike<{ error: { message: string } | null }>

async function firstError(steps: Step[]): Promise<string | null> {
  const rs = await Promise.all(steps.map(f => Promise.resolve(f())))
  for (const r of rs) if (r.error) return r.error.message
  return null
}

let busy = false
let again = false
let last: SyncReport = { ok: false, skipped: 'never-run', error: 'ещё не запускалась' }

export const lastReport = () => last

/**
 * Один проход: тянем всё → сливаем → отправляем изменённое → пишем снимок.
 * Сначала тянем и только потом отправляем: иначе отправка увезла бы в базу
 * устаревшую копию строки, которую только что поменяли с другого устройства.
 */
export async function syncNow(sb: SupabaseClient, s: State,
                              apply: (p: Pulled) => void): Promise<SyncReport> {
  const { data: sess } = await sb.auth.getSession()
  const uid = sess.session?.user.id
  if (!uid) return (last = { ok: false, skipped: 'no-session', error: 'нет сессии' })

  const week = weekStart()
  const snap = readSnap(uid)

  const [pr, pl, ph, tk] = await Promise.all([
    sb.from('profiles').select('*').eq('id', uid).maybeSingle(),
    sb.from('plants').select('*'),
    sb.from('photos').select('*'),
    sb.from('week_tasks').select('*').eq('week_start', week),
  ])
  const bad = pr.error || pl.error || ph.error || tk.error
  if (bad) return (last = { ok: false, uid, error: bad.message })

  const cloud: Cloud = {
    profile: (pr.data as ProfileRow | null) || null,
    plants: (pl.data as PlantRow[]) || [],
    photos: (ph.data as PhotoRow[]) || [],
    tasks: (tk.data as TaskRow[]) || [],
  }

  const m = merge(s, cloud, snap, week, uid)
  if (m.pulled) apply(m.pulled)

  // ── что отправляем: расхождение отпечатков со снимком
  const now = fingerprints(m.next, uid, week)
  const was = snap?.rows || {}

  const plantsUp: PlantRow[] = []
  const photosUp: PhotoRow[] = []
  m.next.plants.forEach((p, i) => {
    if (was[PK(p.id)] !== now[PK(p.id)] || was[SK(p.id)] !== now[SK(p.id)]) {
      plantsUp.push({ id: p.id, user_id: uid, species_id: p.s.id,
                      since: p.since, day: p.day, sort: i })
    }
    p.photos.forEach(x => {
      if (x.u || was[FK(x.id)] === now[FK(x.id)]) return
      photosUp.push({ id: x.id, user_id: uid, plant_id: p.id, kind: 'stock',
                      stock_name: x.f || '', day: x.day })
    })
  })

  const tasksUp: TaskRow[] = []
  Object.keys(m.next.done).forEach(k => {
    if (was[TK(week, k)] === now[TK(week, k)]) return
    tasksUp.push({ user_id: uid, week_start: week, task_key: k, done: m.next.done[k] })
  })

  const profileUp = was[UK] !== now[UK] ? profileOf(m.next, uid) : null

  // Пропало локально: ключ был в снимке, а теперь его нет. Отметки недели —
  // только текущей: снимок прошлых недель просто забываем, историю в базе
  // чистит prune_history, а не мы.
  const gonePlants: string[] = []
  const gonePhotos: string[] = []
  const goneTasks: string[] = []
  Object.keys(was).forEach(k => {
    if (now[k] !== undefined) return
    if (k.startsWith('s:')) return                       // ключ порядка, своей строки нет
    if (k.startsWith('p:')) gonePlants.push(k.slice(2))
    else if (k.startsWith('f:')) gonePhotos.push(k.slice(2))
    else if (k.startsWith('t:' + week + '|')) goneTasks.push(k.slice(('t:' + week + '|').length))
  })

  // Порядок важен: растение должно существовать до своего снимка (FK), а
  // профиль — до всего: без него у аккаунта нет ни ZIP, ни времени напоминания.
  const stamp = new Date().toISOString()
  const head: Step[] = []
  if (profileUp) head.push(() => sb.from('profiles').upsert(profileUp))
  if (plantsUp.length) head.push(() => sb.from('plants').upsert(plantsUp))
  const headErr = await firstError(head)
  if (headErr) return (last = { ok: false, uid, error: headErr })

  const tail: Step[] = []
  if (photosUp.length) tail.push(() => sb.from('photos').upsert(photosUp))
  if (tasksUp.length) tail.push(() => sb.from('week_tasks').upsert(tasksUp))
  if (gonePhotos.length) {
    tail.push(() => sb.from('photos').update({ deleted_at: stamp }).in('id', gonePhotos))
  }
  if (gonePlants.length) {
    tail.push(() => sb.from('plants').update({ deleted_at: stamp }).in('id', gonePlants))
  }
  // У отметок недели нет мягкого удаления: они и так живут до prune_history,
  // и «галочки нет» — это отсутствие строки, а не строка с датой.
  goneTasks.forEach(k => tail.push(() =>
    sb.from('week_tasks').delete().eq('week_start', week).eq('task_key', k)))
  const tailErr = await firstError(tail)
  if (tailErr) return (last = { ok: false, uid, error: tailErr })

  writeSnap(uid, now, stamp)
  return (last = {
    ok: true, uid, first: !snap,
    pulled: { ...m.counts },
    pushed: {
      plants: plantsUp.length, photos: photosUp.length, tasks: tasksUp.length,
      profile: !!profileUp, gone: gonePlants.length + gonePhotos.length + goneTasks.length,
    },
  })
}

/**
 * Delete account. Экран обещает «Your plants go with it», и без этой уборки
 * обещание было бы ложным: локальное стёрлось бы, а при следующем входе сад
 * приехал бы обратно из базы.
 *
 * Сам аккаунт входа остаётся: удалить пользователя из auth.users можно только
 * ключом service_role, а на статическом сайте его нет. Экран этого и не
 * обещает — он говорит про растения и настройки.
 *
 * Снимки уходят каскадом вместе с растениями (photos.plant_id on delete cascade).
 */
export async function wipeCloud(sb: SupabaseClient): Promise<string | null> {
  const { data: sess } = await sb.auth.getSession()
  const uid = sess.session?.user.id
  if (!uid) return 'нет сессии'
  const err = await firstError([
    () => sb.from('plants').delete().eq('user_id', uid),
    () => sb.from('week_tasks').delete().eq('user_id', uid),
    () => sb.from('profiles').delete().eq('id', uid),
  ])
  forgetSnap()
  return err
}

/**
 * Что показать на экране аккаунта. Считается из снимка последней отправки, а не
 * из запроса: снимок И ЕСТЬ ответ на «что из моего уже в базе», он лежит рядом
 * и читается мгновенно — экран не получает ни спиннера, ни отказа.
 */
export interface SyncFacts {
  /** когда проход в последний раз прошёл целиком, ISO; null — ни разу */
  at: string | null
  /** растений в базе */
  plants: number
  /** кадров журнала в базе */
  photos: number
  /** кадры с камеры: в базе их пока нет, им нужен Storage */
  localOnly: number
  /** причина последнего настоящего отказа; «ещё не время» сюда не попадает */
  error: string | null
}

export function syncFacts(s: State, uid: string | null): SyncFacts {
  const snap = uid ? readSnap(uid) : null
  const rows = snap?.rows || {}
  let plants = 0
  let photos = 0
  for (const k of Object.keys(rows)) {
    if (k.startsWith('p:')) plants++
    else if (k.startsWith('f:')) photos++
  }
  return {
    at: snap?.at || null,
    plants,
    photos,
    localOnly: s.plants.reduce((n, p) => n + p.photos.filter(x => x.u).length, 0),
    error: last.ok || last.skipped ? null : last.error || null,
  }
}

/** Проход с защитой от наложения: пока идёт один, второй только ставит флаг. */
export async function runSync(sb: SupabaseClient, get: () => State,
                              apply: (p: Pulled) => void): Promise<SyncReport> {
  if (busy) { again = true; return last }
  busy = true
  try {
    let r = await syncNow(sb, get(), apply)
    while (again) { again = false; r = await syncNow(sb, get(), apply) }
    return r
  } catch (e) {
    return (last = { ok: false, error: e instanceof Error ? e.message : String(e) })
  } finally { busy = false }
}
