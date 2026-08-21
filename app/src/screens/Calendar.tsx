// Harvest calendar. Два вида под два разных вопроса:
//   This month — «что сажать сейчас»: рейка двенадцати месяцев и плитки с
//     настоящими снимками, отсортированные по скорости до урожая;
//   Whole year — «как устроен мой сезон»: таблица НЕПРЕРЫВНЫХ полос, по две
//     дорожки на культуру (посев и сбор). Клетка с зазором читалась как
//     шахматка, полоса читается как отрезок времени; две дорожки убирают
//     нужду в третьем цвете под пересечение и показывают сам сдвиг.
//
// Пунктиром — обе даты заморозков, оранжевой линией — сегодня: именно от них
// считаются все окна, поэтому они и объясняют форму диаграммы.

import { Fragment } from 'react'
import { Screen } from '../components/Chrome'
import { Icon } from '../icons/Icon'
import { bg } from '../lib/assets'
import type { Species as Sp } from '../data/species'
import {
  MON1, MONF, addD, byDays, calSort, dayOffset, fmtMD, frostDates, isHousePool,
  monthMap, nowMonth, pctY, pickableIn, sowableIn, spDays as days, TODAY, windows,
  zipInfo, type Ctx,
} from '../lib/season'
import { useStore } from '../state/store'

/** Одна строка человеческим языком — она же aria-label, она же раскрытая деталь. */
function say(sp: Sp, ctx: Ctx): { plain: string; rich: JSX.Element } {
  const w = windows(sp, ctx)
  if (!w) {
    const t = sp.kind === 'house'
      ? 'no season — open all year'
      : `sow any month · ready ${days(sp)} days after sowing`
    return { plain: t, rich: <>{t}</> }
  }
  if (w.tight) {
    const t = 'the season here is too short for it — no window this year'
    return { plain: t, rich: <>{t}</> }
  }
  const a = `${fmtMD(w.sow[0])} – ${fmtMD(w.sow[1])}`
  const b = `${fmtMD(w.pick[0])} – ${fmtMD(w.pick[1])}`
  return {
    plain: `sow ${a} · pick ${b} · ${days(sp)} days to harvest`,
    rich: <>sow <b>{a}</b> · pick <b>{b}</b> · {days(sp)} days to harvest</>,
  }
}

function Row({ sp, ctx, open, onToggle }:
             { sp: Sp; ctx: Ctx; open: boolean; onToggle: () => void }) {
  const w = windows(sp, ctx)
  const s = say(sp, ctx)
  const seg = (a: Date, b: Date, cls: string) => {
    const l = pctY(a), r = pctY(b)
    return <i className={'calbar ' + cls}
              style={{ left: l.toFixed(1) + '%', width: Math.max(1.8, r - l).toFixed(1) + '%' }} />
  }
  return (
    <>
      <div className={'calrow' + (open ? ' open' : '')} role="button" tabIndex={0}
           aria-expanded={open} aria-label={`${sp.name} — ${s.plain}`}
           onClick={onToggle}
           onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onToggle() } }}>
        <b className="calname">{sp.name}</b>
        <div className="caltrack">
          {w
            ? <>{seg(w.sow[0], w.sow[1], 's-sow')}{seg(w.pick[0], w.pick[1], 's-pick')}</>
            : <i className="calbar s-any" style={{ left: 0, width: '100%' }} />}
        </div>
      </div>
      {open && <div className="caldet">{s.rich}</div>}
    </>
  )
}

const Axis = () => (
  <div className="calaxis" aria-hidden="true">
    <b />
    <div>{MON1.map((m, i) => <i key={i} className={i === nowMonth() ? 'on' : undefined}>{m}</i>)}</div>
  </div>
)

/** Заморозки и «сегодня» — один слой на всю таблицу, а не по метке в строке. */
function Overlay({ ctx }: { ctx: Ctx }) {
  if (!ctx.outdoor) return null
  const f = frostDates(ctx.zip)
  return (
    <div className="calov" aria-hidden="true">
      <i className="calfrost" style={{ left: pctY(f.last).toFixed(1) + '%' }} />
      <i className="calfrost" style={{ left: pctY(f.first).toFixed(1) + '%' }} />
      <i className="caltoday" style={{ left: pctY(dayOffset(TODAY)).toFixed(1) + '%' }} />
    </div>
  )
}

interface Group { t: string; s: string; rows: Sp[] }

function Table({ rows, groups, ctx, open, setOpen }:
    { rows?: Sp[]; groups?: Group[]; ctx: Ctx; open: string | null; setOpen: (id: string) => void }) {
  const row = (sp: Sp) => (
    <Row key={sp.id} sp={sp} ctx={ctx} open={open === sp.id} onToggle={() => setOpen(sp.id)} />
  )
  return (
    <div className="calbox">
      <Axis />
      <div className="caltl">
        <Overlay ctx={ctx} />
        {groups
          ? groups.map(g => (
              <Fragment key={g.t}>
                <div className="calgrp">{g.t}{g.s && <s> · {g.s}</s>}</div>
                {g.rows.map(row)}
              </Fragment>
            ))
          : rows!.map(row)}
      </div>
    </div>
  )
}

function YearView() {
  const { s, d, ctx, pool } = useStore()
  const house = isHousePool(pool)
  const noSeason = !ctx.outdoor
  const seen: Record<string, 1> = {}
  const mine = s.plants.map(p => p.s).filter(x => (seen[x.id] ? false : (seen[x.id] = 1, true)))
  const rest = pool.filter(x => !seen[x.id])
  const f = frostDates(ctx.zip)

  const groups: Group[] = []
  if (noSeason) {
    groups.push({ t: 'ANY MONTH', s: 'no frost indoors, so nothing waits', rows: calSort(rest, ctx) })
  } else {
    const cool = rest.filter(x => x.kind === 'edible' && x.cool)
    const warm = rest.filter(x => x.kind === 'edible' && !x.cool)
    const hou = rest.filter(x => x.kind === 'house')
    if (cool.length) groups.push({
      t: 'COOL-SEASON', s: 'in the ground from ' + fmtMD(addD(f.last, -28)), rows: calSort(cool, ctx),
    })
    if (warm.length) groups.push({
      t: 'WARM-SEASON', s: 'waits until ' + fmtMD(f.last), rows: calSort(warm, ctx),
    })
    if (hou.length) groups.push({
      t: 'NO SEASON', s: 'houseplants, open all year', rows: calSort(hou, ctx),
    })
  }
  const setOpen = (id: string) => d({ t: 'calOpen', v: id })

  return (
    <>
      {mine.length > 0 && <>
        <div className="sl">Yours</div>
        <Table rows={calSort(mine, ctx)} ctx={ctx} open={s.calOpen} setOpen={setOpen} />
      </>}
      {groups.length > 0 && <>
        <div className="sl">{mine.length ? 'Could also go in' : 'What can go in'}</div>
        <Table groups={groups} ctx={ctx} open={s.calOpen} setOpen={setOpen} />
      </>}
      {/* Легенда обязана описывать то, что нарисовано: без сезона полос посева
          и сбора на экране нет вообще, обещать их нельзя. */}
      <div className="callg">
        {noSeason || house
          ? <span><i className="s-any" />open all year</span>
          : <>
              <span><i className="s-sow" />sow</span>
              <span><i className="s-pick" />pick</span>
              <span><i className="l-frost" />frost dates</span>
              <span><i className="l-today" />today</span>
            </>}
      </div>
    </>
  )
}

function Card({ sp, note, onOpen }: { sp: Sp; note: string; onOpen: () => void }) {
  return (
    <div className="calcard" role="button" tabIndex={0} aria-label={`${sp.name} — ${note}`}
         onClick={onOpen}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpen() } }}>
      {sp.img
        ? <div className="calph" style={{ backgroundImage: bg(sp.img) }} />
        : <div className="calph"><Icon name={sp.icon} color="#8CA093" size={22} /></div>}
      <b>{sp.name}</b>
      <s>{note}</s>
    </div>
  )
}

function Rail() {
  const { s, d, ctx, pool } = useStore()
  const m = s.calMonth ?? nowMonth()
  return (
    <div className="calrail" role="radiogroup" aria-label="Month">
      {MON1.map((lbl, i) => {
        const sow = sowableIn(i, pool, ctx).length
        const pick = pickableIn(i, pool, ctx).length
        const k = sow && pick ? 'c-both' : pick ? 'c-pick' : sow ? 'c-sow' : ''
        // Вслух клетка должна называть не только месяц, но и что в нём есть.
        const say2 = `${MONF[i]}${i === nowMonth() ? ' (this month)' : ''} — `
          + (sow ? `${sow} to sow` : 'nothing to sow') + ', '
          + (pick ? `${pick} in a harvest window` : 'no harvest window')
        const cls = [k, i === m ? 'on' : '', i === nowMonth() ? 'cnow' : ''].filter(Boolean).join(' ')
        return (
          <i key={i} className={cls} role="radio" tabIndex={0} aria-checked={i === m}
             aria-label={say2}
             onClick={() => d({ t: 'calMonth', v: i })}
             onKeyDown={e => {
               if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); d({ t: 'calMonth', v: i }) }
             }}>{lbl}</i>
        )
      })}
    </div>
  )
}

function MonthView({ openSpecies }: { openSpecies: (sp: Sp) => void }) {
  const { s, d, ctx, pool } = useStore()
  if (!pool.length) return <div className="setnote">Nothing on the list yet.</div>

  // Комнатные: месяц ничего не решает, решает свет. Рейку месяцев тут
  // показывать нельзя — двенадцать одинаковых клеток обещают выбор, которого нет.
  if (isHousePool(pool)) {
    return (
      <>
        <div className="sl">Any month works · {pool.length}</div>
        <div className="calgrid">
          {pool.map(sp => <Card key={sp.id} sp={sp} note={sp.light} onOpen={() => openSpecies(sp)} />)}
        </div>
      </>
    )
  }

  const m = s.calMonth ?? nowMonth()
  const noSeason = !ctx.outdoor
  const sow = byDays(sowableIn(m, pool, ctx))
  const pick = byDays(pickableIn(m, pool, ctx))
  const step = (n: number) => d({ t: 'calMonth', v: (m + n + 12) % 12 })
  const opens = pool.map(sp => windows(sp, ctx)).filter(Boolean)
    .map(w => w!.sow[0]).sort((a, b) => +a - +b)[0]

  return (
    <>
      <div className="calmh">
        <b>{MONF[m]}</b>
        {/* Двенадцать клеток по 44px в 358px не влезают физически, поэтому
            рейка — ускоритель, а обязательная тап-зона живёт здесь. */}
        <div className="calnav">
          <i className="prev" role="button" tabIndex={0} aria-label="Previous month"
             onClick={() => step(-1)}
             onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); step(-1) } }}>
            <Icon name="caret-right" color="var(--primary)" size={20} sw={2.6} />
          </i>
          <i role="button" tabIndex={0} aria-label="Next month"
             onClick={() => step(1)}
             onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); step(1) } }}>
            <Icon name="caret-right" color="var(--primary)" size={20} sw={2.6} />
          </i>
        </div>
      </div>
      <Rail />

      <div className="sl">
        {sow.length
          ? (noSeason ? `Can go in any month · ${sow.length}` : `Sow in ${MONF[m]} · ${sow.length}`)
          : `Nothing to sow in ${MONF[m]}`}
      </div>
      {sow.length
        ? <div className="calgrid">
            {sow.map(sp => {
              const w = windows(sp, ctx)
              // Окно закрывается в этом же месяце — это и есть срочность, её и пишем.
              const last = w && !w.tight && w.sow[1].getMonth() === m
              return <Card key={sp.id} sp={sp} onOpen={() => openSpecies(sp)}
                           note={last ? 'sow by ' + fmtMD(w!.sow[1]) : `${days(sp)} days`} />
            })}
          </div>
        : <div className="setnote">
            Too cold to start anything outside.{' '}
            {opens ? <>The first window opens around <b>{fmtMD(opens)}</b>.</>
                   : 'Nothing on this list has an outdoor window here.'}
          </div>}

      {!noSeason && <>
        <div className="sl">
          {pick.length ? `Harvest window in ${MONF[m]} · ${pick.length}`
                       : `No harvest window in ${MONF[m]}`}
        </div>
        {pick.length
          ? <>
              <div className="calgrid">
                {pick.map(sp => (
                  <Card key={sp.id} sp={sp} note={`${days(sp)} days`} onOpen={() => openSpecies(sp)} />
                ))}
              </div>
              <div className="setnote">
                A window, not a promise: it opens this early only if the seed went in
                on the first possible day.
              </div>
            </>
          : <div className="setnote">Nothing sown here has had time to come in yet.</div>}
      </>}
    </>
  )
}

/**
 * Шапка экрана всегда описывает ТЕКУЩИЙ месяц: это сводка, а не то, что
 * человек листает рейкой.
 */
function Hero() {
  const { ctx, pool } = useStore()
  const z = zipInfo(ctx.zip)
  const f = frostDates(ctx.zip)
  const n = nowMonth()
  const house = isHousePool(pool)
  const noSeason = !ctx.outdoor
  const sow = sowableIn(n, pool, ctx).length
  const pick = pickableIn(n, pool, ctx).length

  let big: JSX.Element, sub: string
  if (house) {
    big = <>Houseplants keep<br />no season</>
    sub = 'Nothing here waits for a date — they go by light, not by month.'
  } else if (noSeason) {
    big = <>{sow} {sow === 1 ? 'crop can go in' : 'crops can go in'}</>
    sub = 'Indoors there is no frost to work around, so any month works. '
        + 'What matters is days from sowing to the first cut.'
  } else {
    big = <>{sow} {sow === 1 ? 'crop can go in' : 'crops can go in'}</>
    sub = (pick ? `${pick} ${pick === 1 ? 'is' : 'are'} inside a harvest window.`
                : 'No harvest window is open yet.') + ' Both come from your frost dates.'
  }

  return (
    <div className="acc">
      <div className="acc-photo"
           style={{ backgroundImage: bg(house ? 'hero-plants' : 'hero-calendar') }} />
      <div className="row1" style={{ marginTop: 16 }}>
        <span className="tag">
          {ctx.outdoor ? `SEASON 2026 · ${z.city.toUpperCase()}` : 'INDOORS · ALL YEAR'}
        </span>
      </div>
      <div className="lbl">{house ? 'All twelve months' : MONF[n]}</div>
      <div className="big">{big}</div>
      <div className="sub">{sub}</div>
      {!house && !noSeason && (
        <div className="duo">
          <div className="cell"><s>Last frost</s><b>{z.frost}</b></div>
          <div className="cell"><s>First frost</s><b>{fmtMD(f.first)}</b></div>
          <div className="cell"><s>Season</s><b>{z.season}d</b></div>
        </div>
      )}
    </div>
  )
}

export function CalendarScreen({ go, openSpecies }:
                               { go: (id: string) => void; openSpecies: (sp: Sp) => void }) {
  const { s, d, ctx, pool } = useStore()
  const house = isHousePool(pool)
  // У комнатных года нет: восемь строк по двенадцать одинаковых полос ничего не
  // сообщают. На этом треке переключателя вида нет вовсе — заодно нижняя
  // оговорка про карточки перестаёт врать, карточки теперь единственный вид.
  const view = house ? 'month' : s.calView
  const y = view === 'year'

  return (
    <Screen id="calendar" back={() => go('growth')}
            nav={{ active: 'Growth', go }} scrollKey="calendar">
      <div className="h1" style={{ marginTop: 16 }}>Harvest calendar</div>
      <Hero />
      {!house && (
        <div className="calseg" role="radiogroup" aria-label="Calendar view">
          <div className={y ? undefined : 'on'} role="radio" aria-checked={!y} tabIndex={0}
               onClick={() => d({ t: 'calView', v: 'month' })}
               onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); d({ t: 'calView', v: 'month' }) } }}>
            This month
          </div>
          <div className={y ? 'on' : undefined} role="radio" aria-checked={y} tabIndex={0}
               onClick={() => d({ t: 'calView', v: 'year' })}
               onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); d({ t: 'calView', v: 'year' }) } }}>
            Whole year
          </div>
        </div>
      )}
      {y ? <YearView /> : <MonthView openSpecies={openSpecies} />}
      <div className="setnote">
        {house
          ? 'A harvest calendar has nothing to plan for a houseplant: there is no sowing '
            + 'window and no crop to bring in. What decides whether one of these works is '
            + 'the light in the room, so that is what each card shows.'
          : !ctx.outdoor
          ? 'Indoors there is no frost, so no month is closed. The number that matters is '
            + 'days from sowing to the first cut.'
          : <>
              Windows come from your last frost date and how long each crop needs.
              Houseplants have no season, so their row stays open all year.
              <br /><br />
              One honest gap: this works off frost, not summer heat. In a hot region the
              cool-season crops — lettuce, radish, cilantro — will bolt in midsummer even
              though the row here stays open. Sow those in spring and again in late summer.
            </>}
      </div>
    </Screen>
  )
}

/** Виджет-вход с Growth: предпросмотр года, сложенный по растениям человека. */
export function CalendarWidget({ go }: { go: (id: string) => void }) {
  const { s, ctx, pool } = useStore()
  const mine = s.plants.map(p => p.s)
  const now = nowMonth()
  const noSeason = !ctx.outdoor
  const free = noSeason && mine.some(x => x.kind === 'edible')
  const have: Record<string, 1> = {}
  mine.forEach(sp => { have[sp.id] = 1 })
  // Полоса показывает год ЕГО растений, значит и счётчик должен считать
  // остальное: одна и та же цифра про «всё вообще» рядом с личной полосой
  // читалась как её подпись.
  const can = sowableIn(now, pool, ctx).filter(sp => !have[sp.id])
  const word = (mine.length ? ' more crop' : ' crop') + (can.length === 1 ? '' : 's')

  return (
    <div className="wg wg-lite span2" role="button" tabIndex={0}
         onClick={() => go('calendar')}
         onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go('calendar') } }}>
      <div className="wg-h"><b>Harvest calendar</b><s>{MONF[now].slice(0, 3)}</s></div>
      <div className="calyear">
        {MON1.map((lbl, m) => {
          let sow = 0, pick = 0
          mine.forEach(sp => {
            const mm = monthMap(sp, ctx)
            if (!mm) return
            if (mm[m] === 'sow' || mm[m] === 'both') sow++
            if (mm[m] === 'pick' || mm[m] === 'both') pick++
          })
          // Без сезона строка открыта весь год — красим ровно, а не пусто.
          const k = free ? 'c-sow' : (pick && sow ? 'c-both' : pick ? 'c-pick' : sow ? 'c-sow' : '')
          return <i key={m} className={[k, m === now ? 'cnow' : ''].filter(Boolean).join(' ')}>{lbl}</i>
        })}
      </div>
      <div className="calcta">
        {noSeason
          ? 'No season indoors — any month works'
          : can.length ? `${can.length}${word} can go in this month`
                       : 'Nothing new should go in this month'}
        {' · see the whole year'}
      </div>
    </div>
  )
}
