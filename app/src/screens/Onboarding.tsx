// Онбординг. Развилка на входе: приложение — трекер ухода, а не только
// планировщик посадки, поэтому у «уже есть растения» и «хочу начать» разные
// вопросы и разные концы. Обе ветки сходятся на Home.

import { useState } from 'react'
import { Screen } from '../components/Chrome'
import { Opt, Pg } from '../components/parts'
import { Icon } from '../icons/Icon'
import { bg } from '../lib/assets'
import { isEdible } from '../lib/plants'
import {
  GOALS, Q4TITLE, SPACES, SUNLABEL, SUNRANK, TRACKOF, goalTag, isOutdoorSpace,
} from '../data/onboarding'
import { useStore, type Track } from '../state/store'
import { zipInfo } from '../lib/season'

type Go = (id: string) => void

// ─────────────────────────────────────────── Landing
export function LandingScreen({ go }: { go: Go }) {
  return (
    <div className="screen on" id="s-landing">
      <div className="sb"><span>9:41</span>
        <span style={{ letterSpacing: '.06em' }}>
          <Icon name="sun" color="var(--ink)" size={15} sw={2} />
        </span></div>
      <div className="shot" style={{ backgroundImage: bg('hero-basket'), top: 48 }} />
      <div className="scrim" style={{ top: 48 }} />
      <div className="overlay" style={{ top: 48 }}>
        <div className="wm" style={{ color: '#fff' }}>HOMEGROWN</div>
        <div style={{ flex: 1 }} />
        <div className="cap-f" style={{ fontSize: 'var(--t-40)', lineHeight: 1.02 }}>
          Green thumb<br /><span style={{ color: 'var(--lime)' }}>not required.</span>
        </div>
        <div style={{ fontSize: 'var(--t-16)', lineHeight: 1.5, marginTop: 16, color: '#DCE7DE' }}>
          Tell us what you have and how much light it gets. We’ll tell you what it needs
          this week.
        </div>
        <div className="btn b-lime" style={{ marginTop: 24 }} role="button" tabIndex={0}
             onClick={() => go('q0')}>Get started free</div>
        <div style={{ fontSize: 'var(--t-13)', color: '#C3D2C7', textAlign: 'center', marginTop: 12 }}>
          No card. Takes 90 seconds.
        </div>
      </div>
    </div>
  )
}

// ─────────────────────────────────────────── Q0: развилка
export function Q0Screen({ go }: { go: Go }) {
  const { d } = useStore()
  const pick = (own: boolean) => {
    d({ t: 'onbReset', v: own ? 'own' : 'plan' })
    go(own ? 'add-plant' : 'qwhat')
  }
  return (
    <Screen id="q0" back={() => go('landing')} scrollKey="q0">
      <div className="h1" style={{ marginTop: 16 }}>Where are you<br />starting from?</div>
      <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', marginTop: 4 }}>
        Two very different jobs, so we ask different things.
      </div>
      <Pg id="q0" />
      <div style={{ marginTop: 16 }}>
        <Opt label="I already have plants" sub="Get them on a care schedule"
             onPick={() => pick(true)} />
        <Opt label="I want to start growing" sub="Tell me what to plant and buy"
             onPick={() => pick(false)} />
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── QWhat: трек
export function QWhatScreen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const pick = (label: string) => {
    d({ t: 'choices', v: { track: TRACKOF[label] || 'edible', goals: [] } })
    go('q1')
  }
  return (
    <Screen id="qwhat" back={() => go('q0')} scrollKey="qwhat">
      <div className="h1" style={{ marginTop: 16 }}>What are you growing?</div>
      <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', marginTop: 4 }}>
        This decides the rest of the questions.
      </div>
      <Pg id="qwhat" />
      <div style={{ marginTop: 16 }}>
        <Opt label="Something to eat" sub="Radishes, greens, tomatoes in pots"
             on={s.choices.track === 'edible'} onPick={() => pick('Something to eat')} />
        <Opt label="Houseplants" sub="Monstera, pothos, snake plant"
             on={s.choices.track === 'house'} onPick={() => pick('Houseplants')} />
        <Opt label="Both" sub="Something edible, plants inside too"
             on={s.choices.track === 'both'} onPick={() => pick('Both')} />
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Q1: место
export function Q1Screen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const opts = SPACES[s.choices.track] || SPACES.both
  const pick = (label: string, next: string) => {
    d({ t: 'choices', v: {
      outdoor: isOutdoorSpace(label),
      space: label.indexOf('Windowsill') > -1 ? 'windowsill' : label.toLowerCase(),
    } })
    go(next)
  }
  return (
    <Screen id="q1" back={() => go('q0')} scrollKey="q1">
      <div className="h1" style={{ marginTop: 16 }}>
        {s.choices.track === 'edible' ? 'Where will you grow?' : 'Where will it live?'}
      </div>
      <Pg id="q1" />
      <div style={{ marginTop: 16 }}>
        {opts.map(([label, sub, next]) => (
          <Opt key={label} label={label} sub={sub} onPick={() => pick(label, next)} />
        ))}
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Q2: ZIP (только уличный трек)
export function Q2Screen({ go }: { go: Go }) {
  const { s, d } = useStore()
  // Пока не тапнули — плейсхолдер и погашенный Continue: состояние появляется
  // от действия, а не выставлено заранее.
  const [touched, setTouched] = useState(false)
  const z = zipInfo(s.choices.zip)
  return (
    <Screen id="q2" back={() => go('q1')} scrollKey="q2"
            foot={
              <div className={'btn b-pri' + (touched ? '' : ' off')} role="button" tabIndex={0}
                   onClick={() => touched && go('q3')}>Continue</div>
            }>
      <div className="h1" style={{ marginTop: 16 }}>What’s your ZIP?</div>
      <Pg id="q2" />
      <div style={{ marginTop: 16 }}>
        <div className={'zip' + (touched ? '' : ' ph')} role="button" tabIndex={0}
             aria-label="Enter your ZIP code"
             onClick={() => { setTouched(true)
                              d({ t: 'choices', v: { zip: s.choices.zip || '78704' } }) }}>
          {touched ? s.choices.zip : '— — — — —'}
        </div>
        <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', lineHeight: 1.5, marginTop: 16 }}>
          Frost dates decide what you can put outside right now. Tap to enter.
        </div>
        {touched && (
          <div className="acc" style={{ marginTop: 16 }}>
            <div className="row1"><span className="tag">Matched</span></div>
            <div className="lbl">Climate profile</div>
            <div className="big">{z.city}</div>
            <div className="duo">
              <div className="cell"><s>Last frost</s><b>{z.frost}</b></div>
              <div className="cell"><s>Season</s><b>{z.season} days</b></div>
            </div>
          </div>
        )}
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Q3 / Q2i: свет
const SUN_OUT: Array<[string, string]> = [
  ['3–5 hours', 'Mostly shade or morning sun'],
  ['6–8 hours', 'Good sun most of the day'],
  ['8+ hours', 'Full blazing sun'],
  ['Not sure yet', 'We’ll start you safe and check later'],
]
const SUN_IN: Array<[string, string]> = [
  ['South window', 'Brightest — aloe and basil work here'],
  ['East or West', 'Good for most houseplants and herbs'],
  ['North window', 'Low light — pothos, ZZ, snake plant'],
  ['Not sure', 'We’ll start you safe'],
]
/** Ключ ранга у внутренних вариантов короче подписи на экране. */
const IN_KEY: Record<string, string> = {
  'South window': 'South', 'East or West': 'East or West',
  'North window': 'North', 'Not sure': 'Not sure',
}

function sunPick(label: string, indoor: boolean) {
  const key = indoor ? (IN_KEY[label] || label) : label
  return { sun: SUNLABEL[key] || 'your light', sunRank: SUNRANK[key] || 1 }
}

/** Ветка «уже есть» заканчивается на Home, а не на плане: трек виден по растениям. */
function useSunNext(go: Go) {
  const { s, d } = useStore()
  return (label: string, indoor: boolean) => {
    d({ t: 'choices', v: sunPick(label, indoor) })
    if (s.onbMode === 'own') {
      const h = s.plants.some(p => p.s.kind === 'house')
      const e = s.plants.some(isEdible)
      const track: Track = h && e ? 'both' : e ? 'edible' : h ? 'house' : s.choices.track
      d({ t: 'choices', v: { track } })
      d({ t: 'onb', v: null })
      go('home')
      return
    }
    go('q4')
  }
}

export function Q3Screen({ go }: { go: Go }) {
  const next = useSunNext(go)
  return (
    <Screen id="q3" back={() => go('q2')} scrollKey="q3">
      <div className="h1" style={{ marginTop: 16 }}>How much direct sun<br />does that spot get?</div>
      <Pg id="q3" />
      <div style={{ marginTop: 16 }}>
        {SUN_OUT.map(([l, sub]) => (
          <Opt key={l} label={l} sub={sub} onPick={() => next(l, false)} />
        ))}
      </div>
    </Screen>
  )
}

export function Q2iScreen({ go }: { go: Go }) {
  const next = useSunNext(go)
  return (
    <Screen id="q2i" back={() => go('q1')} scrollKey="q2i">
      <div className="h1" style={{ marginTop: 16 }}>How bright is<br />that spot?</div>
      <Pg id="q2i" />
      <div style={{ marginTop: 16 }}>
        {SUN_IN.map(([l, sub]) => (
          <Opt key={l} label={l} sub={sub} onPick={() => next(l, true)} />
        ))}
      </div>
      <div className="card" style={{ marginTop: 12, display: 'flex', gap: 12, alignItems: 'center' }}>
        <Icon name="lightbulb" color="var(--primary)" size={24} />
        <div style={{ fontSize: 'var(--t-14)', color: 'var(--ink-2)', lineHeight: 1.4 }}>
          Got a grow light? <b style={{ color: 'var(--ink)' }}>Tell us</b> — it upgrades your options.
        </div>
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Q4: цели, лимит 3
const MAXG = 3
export function Q4Screen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const opts = GOALS[s.choices.track] || GOALS.both
  const picked = s.choices.goals
  const toggle = (label: string) => {
    const tag = goalTag(label)
    if (!tag) return
    const has = picked.indexOf(tag) > -1
    if (has) d({ t: 'choices', v: { goals: picked.filter(x => x !== tag) } })
    else if (picked.length < MAXG) d({ t: 'choices', v: { goals: [...picked, tag] } })
  }
  const full = picked.length >= MAXG
  return (
    <Screen id="q4" back={() => go(s.choices.outdoor ? 'q3' : 'q2i')} scrollKey="q4"
            foot={<>
              <div style={{ fontSize: 'var(--t-13)', color: 'var(--muted)', marginBottom: 8,
                            textAlign: 'center' }}>
                {picked.length ? `${picked.length} of 3 picked.` : 'Pick at least one.'}
              </div>
              <div className={'btn b-pri' + (picked.length ? '' : ' off')} role="button"
                   tabIndex={0} onClick={() => picked.length && go('q5')}>Continue</div>
            </>}>
      <div className="h1" style={{ marginTop: 16 }}>{Q4TITLE[s.choices.track] || Q4TITLE.both}</div>
      <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', marginTop: 4 }}>
        Up to 3 · {picked.length ? `${picked.length} selected` : 'nothing selected yet'}
      </div>
      <Pg id="q4" />
      <div style={{ marginTop: 16 }}>
        {opts.map(([label, tag]) => {
          const on = picked.indexOf(tag) > -1
          // лишние гаснут, а не исчезают
          return <Opt key={tag} label={label} multi on={on} dim={full && !on}
                      onPick={() => toggle(label)} />
        })}
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Q5: время в неделю
export function Q5Screen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const many = s.choices.track === 'edible' ? 'a real garden' : 'a real collection'
  const pick = (effort: number) => { d({ t: 'choices', v: { effort } }); go('preview') }
  return (
    <Screen id="q5" back={() => go('q4')} scrollKey="q5">
      <div className="h1" style={{ marginTop: 16 }}>How much time can<br />you give it?</div>
      <Pg id="q5" />
      <div style={{ marginTop: 16 }}>
        <Opt label="About 10 minutes" sub="Keep it very simple · 3 plants"
             on={s.choices.effort === 3} onPick={() => pick(3)} />
        <Opt label="About 20 minutes" sub="I can do a bit more · 4 plants"
             on={s.choices.effort === 4} onPick={() => pick(4)} />
        <Opt label="30+ minutes" sub={`I want ${many} · up to 6 plants`}
             on={s.choices.effort === 6} onPick={() => pick(6)} />
      </div>
    </Screen>
  )
}
