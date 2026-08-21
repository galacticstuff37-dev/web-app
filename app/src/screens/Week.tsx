// Состояния недели. Продукт НИКОГДА не показывает список из двадцати
// просроченных задач: пропуск сворачивается в две задачи из настоящих растений,
// остальное закрывается статусом expired без обвинения.

import { Screen } from '../components/Chrome'
import { Note, Ring } from '../components/bits'
import { Task } from '../components/parts'
import { Icon } from '../icons/Icon'
import { inDays } from '../lib/plan'
import {
  hEta, hPct, isEdible, lc, wDue, weekTasks, type Plant,
} from '../lib/plants'
import { MON, TODAY, dayOffset } from '../lib/season'
import { useStore } from '../state/store'

type Go = (id: string) => void

const WORDNUM = ['No', 'One', 'Two', 'Three', 'Four', 'Five', 'Six']
const pPct = (p: Plant) => (isEdible(p) ? hPct(p)
  : Math.max(0, Math.min(100, Math.round((p.since / p.s.water) * 100))))
const pSub = (p: Plant) => isEdible(p)
  ? `Day ${p.day} · ${hPct(p) >= 100 ? 'ready' : 'growing'}`
  : `${p.s.light} · every ${p.s.water}d`

// ─────────────────────────────────────────── Week · пусто
export function WeekEmptyScreen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const future = s.plants.filter(p => wDue(p) > 0).sort((a, b) => wDue(a) - wDue(b))
  const nextP = future[0]
  const open = (i: number) => { d({ t: 'select', v: i }); go('plant') }

  return (
    <Screen id="week-empty" nav={{ active: 'Week', go }}
            offer={{ onClick: () => go('paywall') }} scrollKey="week-empty">
      <div className="greet">Good morning · nothing due</div>
      <div className="h1">Nothing needed<br /><span className="m">this week.</span></div>
      {!s.plants.length
        ? <Note title="Nothing to do yet">Add a plant and the week fills itself in.</Note>
        : nextP
        ? <Note title="Just water and watch">
            Everything is on schedule. The next real job is{' '}
            {isEdible(nextP) && hPct(nextP) >= 100 ? 'picking the ' : 'watering the '}
            {lc(nextP.s.name)} {inDays(wDue(nextP))} — we’ll put it on that week’s card.
          </Note>
        : <Note title="Everything is thirsty at once">
            Water them today and the week clears itself. After that the schedule spreads
            them out again.
          </Note>}
      <div className="sl">Your plants</div>
      {s.plants.length > 0 && (
        <div className="plist">
          {s.plants.map((p, i) => (
            <div className="pl" key={i} role="button" tabIndex={0} onClick={() => open(i)}>
              <div className="rw">
                <Ring pct={pPct(p)} />
                <i><Icon name={p.s.icon} color="var(--primary)" size={15} sw={1.9} /></i>
              </div>
              <div className="nm"><b>{p.s.name}</b><s>{pSub(p)}</s></div>
              <div className="eta">
                {isEdible(p) ? hEta(p) : (wDue(p) <= 0 ? 'water' : `~${wDue(p)}d`)}
              </div>
            </div>
          ))}
        </div>
      )}
    </Screen>
  )
}

// ─────────────────────────────────────────── Week · возврат
export function WeekBackScreen({ go }: { go: Go }) {
  const { s } = useStore()
  const t = weekTasks(s.plants).slice(0, 2)
  return (
    <Screen id="week-back" nav={{ active: 'Week', badge: true, go }}
            offer={{ onClick: () => go('paywall') }} scrollKey="week-back">
      <div className="greet">You were away 2 weeks</div>
      <div className="h1">Welcome back.<br /><span className="m">Here’s what matters now.</span></div>
      <Note title="Most of it doesn’t matter now">
        Nine tasks stopped being useful and closed themselves. The ones below still pay off.
      </Note>
      <div className="sl">Still worth doing</div>
      {t.length
        ? t.map((x, i) => <Task key={i} t={[x[0], x[1], x[2]]} />)
        : <Note title="Nothing is waiting">Your plants held out fine.</Note>}
      <div className="btn b-pri" role="button" tabIndex={0} onClick={() => go('home')}>
        Continue with this week
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Week · долгий пропуск
export function WeekLongScreen({ go }: { go: Go }) {
  const { s } = useStore()
  // Нижняя строка называет растения, которые реально пересохли, а не выдуманный редис.
  const dry = s.plants.filter(p => wDue(p) <= 0).map(p => lc(p.s.name))
  return (
    <Screen id="week-long" nav={{ active: 'Week', go }}
            offer={{ onClick: () => go('paywall') }} scrollKey="week-long">
      <div className="greet">Last visit: 6 weeks ago</div>
      <div className="h1">It’s been a while.<br /><span className="m">Let’s restart from today.</span></div>
      <Note title="Your plan is out of date"
            cta={<>
              <div className="btn b-pri" role="button" tabIndex={0}
                   onClick={() => go('home')}>Rebuild my plan</div>
              <div className="btn b-ghost" role="button" tabIndex={0}
                   onClick={() => go('home')}>Keep the old one</div>
            </>}>
        Six weeks changed what needs doing. We’ll rebuild the schedule from today and keep
        everything you already did — every logged watering and photo stays.
      </Note>
      <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', lineHeight: 1.45,
                    marginTop: 16, padding: '0 4px' }}>
        {dry.length
          ? `The ${dry.join(' and ')} may have dropped a leaf while you were away. `
            + 'If it did, that’s normal — water deeply once and it comes back.'
          : 'Nothing dried out completely. Water once, and the schedule picks up from today.'}
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Soft-lock
export function WeekLockScreen({ go }: { go: Go }) {
  const { s } = useStore()
  // Окно «через две недели» считается от TODAY, а не от захардкоженных дат.
  const a = dayOffset(TODAY + 14), b = dayOffset(TODAY + 20)
  const when = `Two weeks from now · ${MON[a.getMonth()]} ${a.getDate()}–`
    + (a.getMonth() === b.getMonth() ? b.getDate() : `${MON[b.getMonth()]} ${b.getDate()}`)
  const tasks = weekTasks(s.plants)
  const cnt = Math.min(3, tasks.length)

  return (
    <Screen id="week-lock" back={() => go('home')} nav={{ active: 'Week', go }}
            scrollKey="week-lock">
      <div className="greet">{when}</div>
      <div className="h1">
        {WORDNUM[cnt] || cnt} {cnt === 1 ? 'task' : 'tasks'}
        <br /><span className="m">already planned.</span>
      </div>
      {!s.plants.length
        ? <Note title="Nothing is scheduled yet"
                cta={<div className="btn b-pri" role="button" tabIndex={0}
                          onClick={() => go('add-plant')}>Add a plant</div>}>
            Add a plant and the weeks ahead fill themselves in — that is what Pro keeps open.
          </Note>
        : s.isPro
        ? <>
            <div className="sl">What they are</div>
            {tasks.slice(0, 3).map((x, i) => <Task key={i} t={[x[0], x[1], x[2]]} />)}
            <Note title="You have the whole calendar">
              Every week ahead is planned. Nothing is hidden any more.
            </Note>
          </>
        : <>
            <div className="sl">What they are</div>
            {/* Даты и объём видны, скрыты только формулировки. Это не стена. */}
            <Task t={['', '4 min']} locked />
            <Task t={['', '3 min']} locked />
            <Task t={['', '10 min']} locked />
            <div className="acc" style={{ marginTop: 16 }}>
              <div className="row1"><span className="tag">Locked</span></div>
              <div className="big" style={{ fontSize: 'var(--t-24)', marginTop: 16 }}>
                Pro unlocks<br />the whole calendar
              </div>
              <div className="sub">
                The dates and the workload are real — only the wording is hidden.
              </div>
              <div className="btn b-lime" role="button" tabIndex={0}
                   onClick={() => go('paywall')}>Unlock the full plan</div>
            </div>
          </>}
    </Screen>
  )
}
