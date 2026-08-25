// Проверка слияния. Тот же приём, что и с моделью сезона в audit.ts: проверки
// живут в бандле и гоняются в настоящем Safari — window.__syncAudit().
//
// Почему так, а не тестовым бегунком: слияние надо проверять там же, где оно
// работает, и БЕЗ аккаунта. merge() — чистая функция, сеть к этому моменту уже
// отработала, поэтому весь набор сценариев (полив на двух устройствах,
// удаление, порядок, кадры с камеры) разыгрывается без единого запроса.
//
// Главная из проверок — сходимость: применили привезённое, прогнали ещё раз с
// тем же облаком и получили «ничего нового». Без неё применение вызывало бы
// новый проход, тот — новое применение, и приложение ушло бы в бесконечный
// круг запросов.
//
// Когда нужна быстрая обратная связь без симулятора, тот же набор гоняется и в
// node — сборка одним файлом, никакого бегунка тестов:
//
//   echo "import{syncAudit}from'./app/src/lib/sync-audit';console.log(syncAudit())" > /tmp/r.ts
//   ./app/node_modules/.bin/esbuild /tmp/r.ts --bundle --platform=node --format=esm \
//     --define:import.meta.env='{"BASE_URL":"/web-app/react/"}' --outfile=/tmp/r.mjs
//   node /tmp/r.mjs

import { INIT, type Pulled, type State } from '../state/store'
import { mkPlant, type Plant } from './plants'
import {
  fingerprints, merge, profileOf, weekStart,
  type Cloud, type PlantRow, type ProfileRow, type Snap,
} from './sync'

const UID = '11111111-1111-4111-8111-111111111111'
const WEEK = '2026-08-24'                  // понедельник

const st = (over: Partial<State>): State => ({ ...INIT, ...over })
const snapOf = (s: State): Snap => ({ v: 1, uid: UID, rows: fingerprints(s, UID, WEEK) })
const empty: Cloud = { profile: null, plants: [], photos: [], tasks: [] }

/** Растение состояния → строка базы, как её вернул бы PostgREST. */
const rowOf = (p: Plant, sort: number): PlantRow =>
  ({ id: p.id, user_id: UID, species_id: p.s.id, since: p.since, day: p.day, sort })

const cloudOf = (s: State, over: Partial<Cloud> = {}): Cloud => ({
  profile: { ...profileOf(s, UID) },
  plants: s.plants.map(rowOf),
  photos: s.plants.flatMap(p => p.photos.filter(x => !x.u).map(x => ({
    id: x.id, user_id: UID, plant_id: p.id, kind: 'stock' as const,
    stock_name: x.f || '', day: x.day,
  }))),
  tasks: Object.keys(s.done).map(k => ({
    user_id: UID, week_start: WEEK, task_key: k, done: s.done[k],
  })),
  ...over,
})

const apply = (s: State, p: Pulled | null): State => {
  if (!p) return s
  const plants = p.plants ?? s.plants
  return { ...s, ...p, plants,
           choices: p.choices ? { ...s.choices, ...p.choices } : s.choices }
}

export function syncAudit(): string {
  const out: string[] = []
  let fail = 0
  const bad = (m: string) => { fail++; out.push('FAIL ' + m) }
  const eq = (name: string, got: unknown, want: unknown) => {
    if (got === want) out.push(`${name}=${String(got)}`)
    else bad(`${name}: получено ${String(got)}, ожидалось ${String(want)}`)
  }

  // ── 1. Первый проход, база пуста: не тянем ничего.
  // Это защита ответов онбординга: строку профиля завёл триггер, и в ней
  // значения по умолчанию — приехав, они затёрли бы ZIP, свет и время.
  {
    const local = st({ choices: { ...INIT.choices, zip: '60613', effort: 6 } })
    const cloud: Cloud = { ...empty, profile: { ...profileOf(st({}), UID),
                                                zip: null, effort: 4 } }
    const m = merge(local, cloud, null, WEEK, UID)
    eq('первый/пусто: ничего не тянем', m.pulled, null)
    eq('первый/пусто: zip цел', m.next.choices.zip, '60613')
    eq('первый/пусто: effort цел', m.next.choices.effort, 6)
  }

  // ── 2. Первый проход, в базе есть сад: он и выигрывает.
  // Локально в этот момент лежит демо-набор из INIT — уехать он не должен.
  {
    const local = st({})                                    // демо: редиска и т.д.
    const theirs = st({ plants: [mkPlant('pepper', 2, 40, []), mkPlant('kale', 0, 8, [])] })
    const m = merge(local, cloudOf(theirs), null, WEEK, UID)
    eq('первый/есть сад: растений', m.next.plants.length, 2)
    eq('первый/есть сад: демо не выжило',
       m.next.plants.some(p => p.s.id === 'radish'), false)
    eq('первый/есть сад: виды', m.next.plants.map(p => p.s.id).join(','), 'pepper,kale')
  }

  // ── 2b. Первый проход, в базе сад, а локально — ЗАНЕСЁННОЕ РУКАМИ.
  // Прошёл онбординг и вошёл в старый аккаунт: свои растения не исчезают.
  {
    const local = st({ plants: [mkPlant('kale', 0, 0, [])] })       // не витрина
    const theirs = st({ plants: [mkPlant('pepper', 2, 40, [])] })
    const m = merge(local, cloudOf(theirs), null, WEEK, UID)
    eq('первый/своё занесённое: не выброшено', m.next.plants.map(p => p.s.id).join(','), 'kale')
    eq('первый/своё занесённое: база не подмешана сразу', m.pulled, null)
    // Следующий проход: kale к этому моменту УЖЕ уехал отправкой, поэтому в базе
    // оба. Снимок и база обязаны быть согласованы — иначе «в снимке есть, в базе
    // нет» законно читается как «удалили на другом устройстве».
    const snap = { v: 1, uid: UID, rows: fingerprints(local, UID, WEEK) }
    const after = st({ plants: [...local.plants, ...theirs.plants] })
    const both = merge(local, cloudOf(after), snap, WEEK, UID)
    eq('второй проход: сад из базы приехал рядом',
       both.next.plants.map(p => p.s.id).sort().join(','), 'kale,pepper')
  }

  // ── 3. Полив на другом устройстве приезжает.
  {
    const base = st({ plants: [mkPlant('basil', 5, 30, [])] })
    const snap = snapOf(base)
    const cloud = cloudOf(base)
    cloud.plants[0].since = 0                                // там полили
    const m = merge(base, cloud, snap, WEEK, UID)
    eq('чужой полив приехал', m.next.plants[0].since, 0)
  }

  // ── 4. Полив здесь: локальное побеждает, значение не откатывается.
  {
    const was = st({ plants: [mkPlant('basil', 5, 30, [])] })
    const snap = snapOf(was)                                 // снимок со since=5
    const here = st({ plants: [{ ...was.plants[0], since: 0 }] })
    const m = merge(here, cloudOf(was), snap, WEEK, UID)     // в базе всё ещё 5
    eq('свой полив не откатился', m.next.plants[0].since, 0)
    eq('свой полив: тянуть нечего', m.pulled, null)
  }

  // ── 5. Удалили на другом устройстве: строка была в снимке, в базе её нет.
  {
    const base = st({ plants: [mkPlant('basil', 1, 30, []), mkPlant('kale', 1, 9, [])] })
    const snap = snapOf(base)
    const cloud = cloudOf(base)
    cloud.plants = cloud.plants.slice(1)                     // базилик убрали
    const m = merge(base, cloud, snap, WEEK, UID)
    eq('чужое удаление применилось', m.next.plants.map(p => p.s.id).join(','), 'kale')
  }

  // ── 6. Добавили здесь: строки нет ни в базе, ни в снимке — не трогаем.
  {
    const was = st({ plants: [mkPlant('basil', 1, 30, [])] })
    const snap = snapOf(was)
    const here = st({ plants: [...was.plants, mkPlant('kale', 0, 0, [])] })
    const m = merge(here, cloudOf(was), snap, WEEK, UID)
    eq('своё новое цело', m.next.plants.map(p => p.s.id).join(','), 'basil,kale')
    eq('своё новое: тянуть нечего', m.pulled, null)
  }

  // ── 7. Добавили на другом устройстве: приезжает и встаёт по sort.
  {
    const base = st({ plants: [mkPlant('basil', 1, 30, [])] })
    const snap = snapOf(base)
    const cloud = cloudOf(base)
    const extra = mkPlant('pepper', 0, 4, [])
    cloud.plants = [{ ...rowOf(extra, 0), }, { ...cloud.plants[0], sort: 1 }]
    const m = merge(base, cloud, snap, WEEK, UID)
    eq('чужое новое приехало', m.next.plants.map(p => p.s.id).join(','), 'pepper,basil')
  }

  // ── 8. Кадр с камеры не теряется и не читается как удалённый.
  // В базе его нет вовсе: data-URL уедет только после переезда в Storage.
  {
    const p = mkPlant('basil', 1, 30, [{ f: 'basil', day: 21 }])
    const withShot: Plant = { ...p, photos: [{ id: 'cam-1', u: 'data:image/png;base64,AA', day: 30 },
                                             ...p.photos] }
    const base = st({ plants: [withShot] })
    const snap = snapOf(base)
    const m = merge(base, cloudOf(base), snap, WEEK, UID)
    eq('кадр с камеры цел', m.next.plants[0].photos.some(x => x.id === 'cam-1'), true)
    eq('кадр из /img цел', m.next.plants[0].photos.some(x => x.f === 'basil'), true)
    eq('снимки: тянуть нечего', m.pulled, null)
  }

  // ── 9. Отметка задачи с другого устройства приезжает; своя не откатывается.
  {
    const base = st({ plants: [mkPlant('basil', 9, 30, [])], done: {} })
    const snap = snapOf(base)
    const cloud = cloudOf(base)
    cloud.tasks = [{ user_id: UID, week_start: WEEK, task_key: 'water:0', done: true }]
    const m = merge(base, cloud, snap, WEEK, UID)
    eq('чужая галочка приехала', m.next.done['water:0'], true)

    // Поставили здесь и ещё не отправили: в снимке ключа нет, в базе лежит
    // старое значение. Локальное обязано выжить.
    const here = st({ ...base, done: { 'water:0': true } })
    const cloud2 = cloudOf(base)                             // снимок и база без галочки
    cloud2.tasks = [{ user_id: UID, week_start: WEEK, task_key: 'water:0', done: false }]
    const m2 = merge(here, cloud2, snapOf(base), WEEK, UID)
    eq('своя неотправленная галочка выжила', m2.next.done['water:0'], true)

    // Отправили true, а на другом устройстве СНЯЛИ: там новее, снятие приезжает.
    const pushed = st({ ...base, done: { 'water:0': true } })
    const cloud3 = cloudOf(pushed)
    cloud3.tasks = [{ user_id: UID, week_start: WEEK, task_key: 'water:0', done: false }]
    const m3 = merge(pushed, cloud3, snapOf(pushed), WEEK, UID)
    eq('чужое снятие приехало', m3.next.done['water:0'], false)

    // Сняли здесь тумблером care (done чистится целиком) — база не возвращает.
    const cleared = st({ ...base, done: {} })
    const cloud4 = cloudOf(pushed)
    cloud4.tasks = [{ user_id: UID, week_start: WEEK, task_key: 'water:0', done: true }]
    const m4 = merge(cleared, cloud4, snapOf(pushed), WEEK, UID)
    eq('своя очистка не отменилась',
       Object.prototype.hasOwnProperty.call(m4.next.done, 'water:0'), false)
  }

  // ── 10. Отметки чужой недели не влияют на текущую.
  {
    const base = st({ plants: [mkPlant('basil', 9, 30, [])], done: {} })
    const cloud = cloudOf(base)
    cloud.tasks = [{ user_id: UID, week_start: '2026-08-17', task_key: 'water:0', done: true }]
    const m = merge(base, cloud, snapOf(base), WEEK, UID)
    eq('прошлая неделя не влияет', m.pulled, null)
  }

  // ── 11. Профиль: чужая правка приезжает, своя не откатывается.
  {
    const base = st({})
    const snap = snapOf(base)
    const theirs: ProfileRow = { ...profileOf(base, UID), zip: '97214', effort: 6 }
    const m = merge(base, { ...cloudOf(base), profile: theirs }, snap, WEEK, UID)
    eq('чужой профиль приехал', m.next.choices.zip, '97214')
    eq('чужой effort приехал', m.next.choices.effort, 6)

    const here = st({ choices: { ...INIT.choices, zip: '10025' } })
    const m2 = merge(here, cloudOf(base), snap, WEEK, UID)   // в базе старый zip
    eq('свой профиль не откатился', m2.next.choices.zip, '10025')
  }

  // ── 12. Сходимость. Применили привезённое — второй проход обязан сказать
  // «ничего нового», иначе приложение уйдёт в круг запросов.
  {
    const local = st({})
    const theirs = st({ plants: [mkPlant('pepper', 2, 40, [{ f: 'basil', day: 12 }]),
                                 mkPlant('kale', 0, 8, [])],
                        done: { 'water:0': true } })
    const cloud = cloudOf(theirs)
    const one = merge(local, cloud, null, WEEK, UID)
    const after = apply(local, one.pulled)
    const snap: Snap = { v: 1, uid: UID, rows: fingerprints(after, UID, WEEK) }
    const two = merge(after, cloud, snap, WEEK, UID)
    eq('сходимость: второй проход пуст', two.pulled, null)
    const three = merge(after, cloud, snap, WEEK, UID)
    eq('сходимость: третий проход пуст', three.pulled, null)
  }

  // ── 13. Отпечаток растения не зависит от порядка соседей: иначе добавление
  // первого растения делало бы «грязными» все остальные и они бы выигрывали
  // слияние у более свежих значений из базы.
  {
    const a = mkPlant('basil', 1, 30, [])
    const b = mkPlant('kale', 0, 9, [])
    const one = fingerprints(st({ plants: [a, b] }), UID, WEEK)
    const two = fingerprints(st({ plants: [b, a] }), UID, WEEK)
    eq('отпечаток не зависит от порядка', one['p:' + a.id] === two['p:' + a.id], true)
    eq('порядок отдельным ключом', one['s:' + a.id] !== two['s:' + a.id], true)
  }

  // ── 14. Понедельник недели: воскресенье относится к НАЧАВШЕЙСЯ неделе, а не
  // к следующей. Иначе галочки воскресенья уезжали бы в чужую строку.
  {
    eq('вс 2026-08-30 → пн', weekStart(new Date(2026, 7, 30)), '2026-08-24')
    eq('пн 2026-08-24 → он же', weekStart(new Date(2026, 7, 24)), '2026-08-24')
    eq('сб 2026-08-29 → пн', weekStart(new Date(2026, 7, 29)), '2026-08-24')
  }

  return (fail ? `FAILURES=${fail} :: ` : 'ALL SYNC CHECKS PASS :: ') + out.join(' | ')
}

declare global {
  interface Window { __syncAudit?: () => string }
}
if (typeof window !== 'undefined') window.__syncAudit = syncAudit
