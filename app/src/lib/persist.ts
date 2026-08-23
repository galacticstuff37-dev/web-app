// Сессия переживает перезагрузку. Раньше состояние жило только в памяти:
// обновление страницы возвращало демо-набор, а внесённые растения, поливы,
// отметки задач, ZIP и Pro исчезали.
//
// Храним только внесённое человеком. Экранное — тост, раскрытая строка
// календаря, поиск, снимок в процессе выбора вида — остаётся однодневным:
// его и так сбрасывает вход на экран.
//
// Растения пишем как id вида, а не целиком. Справочник видов живёт в коде и
// меняется; восстановленное растение должно брать свежие числа полива и сроков,
// а не те, что были в момент сохранения.

import { SP } from '../data/species'
import { mkPlant, type Photo } from './plants'
import type {
  Account, CalView, Care, Choices, Mail, OnbMode, State, Units,
} from '../state/store'

const KEY = 'hg.state'
/** версия схемы: несовпадение = начинаем заново, а не читаем чужие поля */
const VER = 1

interface SavedPlant { id: string; since: number; day: number; photos: Photo[] }
interface Saved {
  v: number
  choices: Choices
  plants: SavedPlant[]
  selected: number
  isPro: boolean
  units: Units
  remind: number
  care: Care
  mail: Mail
  done: Record<string, boolean>
  calView: CalView
  onbMode: OnbMode
  account: Account | null
}

/** Ключа нет — человек здесь впервые: отдаём демо-набор из INIT.
    Ключ есть, но растений в нём нет — это Delete account, демо не возвращаем. */
export function load(init: State): State {
  let j: Partial<Saved> | null = null
  try {
    const raw = localStorage.getItem(KEY)
    j = raw ? (JSON.parse(raw) as Saved) : null
  } catch { j = null }
  if (!j || j.v !== VER) return init

  const saved = Array.isArray(j.plants) ? j.plants : []
  // вид мог исчезнуть из справочника — такое растение просто не возвращаем
  const plants = saved
    .filter(p => p && SP(p.id))
    .map(p => mkPlant(p.id, p.since, p.day, Array.isArray(p.photos) ? p.photos : []))
  return {
    ...init,
    choices: { ...init.choices, ...j.choices },
    plants,
    selected: Math.min(Math.max(0, j.selected ?? 0), Math.max(0, plants.length - 1)),
    isPro: j.isPro ?? init.isPro,
    units: j.units ?? init.units,
    remind: j.remind ?? init.remind,
    care: { ...init.care, ...j.care },
    mail: { ...init.mail, ...j.mail },
    done: j.done ?? init.done,
    calView: j.calView ?? init.calView,
    onbMode: j.onbMode ?? init.onbMode,
    // Поле добавлено позже: в блобе без него аккаунта просто нет. Версию из-за
    // нового необязательного поля не поднимаем — старые данные читаются верно.
    account: j.account ?? init.account,
  }
}

export function save(s: State): void {
  const body: Saved = {
    v: VER,
    choices: s.choices,
    plants: s.plants.map(p => ({ id: p.s.id, since: p.since, day: p.day, photos: p.photos })),
    selected: s.selected,
    isPro: s.isPro,
    units: s.units,
    remind: s.remind,
    care: s.care,
    mail: s.mail,
    done: s.done,
    calView: s.calView,
    onbMode: s.onbMode,
    account: s.account,
  }
  try {
    localStorage.setItem(KEY, JSON.stringify(body))
  } catch {
    // Квоту (≈5 МБ) выбирают снимки с камеры. Сад без снимков лучше, чем
    // молча не сохранённый сад.
    try {
      localStorage.setItem(KEY, JSON.stringify({
        ...body,
        plants: body.plants.map(p => ({ ...p, photos: p.photos.filter(x => !x.u) })),
      }))
    } catch { /* приватный режим или квота: остаёмся в памяти */ }
  }
}
