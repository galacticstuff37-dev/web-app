// Plan Preview и Save Plan. Момент ценности: план показывается ДО регистрации.
// План — предложение, а не решение: он реально применяется к MY_PLANTS, иначе
// после save→paywall на Home лежал бы демо-набор, а не то, что человек видел.

import { Providers } from './Auth'
import { Screen } from '../components/Chrome'
import { SpThumb } from '../components/bits'
import { Icon } from '../icons/Icon'
import { bg } from '../lib/assets'
import { QUOTE } from '../data/onboarding'
import { fmtPot, limit } from '../lib/plants'
import {
  anA, buildPlan, dateAfter, listNames, planWhy, seasonWeeks, spSub, type PlanCtx,
} from '../lib/plan'
import { lc } from '../lib/plants'
import { zipInfo } from '../lib/season'
import { useStore } from '../state/store'

type Go = (id: string) => void

export function usePlanCtx(): PlanCtx {
  const { s } = useStore()
  return { ...s.choices }
}

export function PreviewScreen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const c = usePlanCtx()
  const plan = buildPlan(c)
  const edible = plan.filter(x => x.kind === 'edible')

  const second = edible.length
    ? (c.outdoor ? 'First pick ' : 'First cut ')
      + dateAfter(Math.min(...edible.map(x => x.days))) + '.'
    : 'Care starts today.'
  const mins = c.effort === 3 ? 10 : c.effort === 4 ? 20 : 30
  const q = QUOTE[c.track === 'edible' ? 'edible' : 'house']
  const room = Math.min(plan.length, limit(s.isPro))

  const add = () => {
    const held = plan.slice(room)
    d({ t: 'applyPlan', v: plan, room })
    const names = held.map(x => lc(x.name))
    d({ t: 'toast', v: {
      html: held.length
        ? `<span>Added ${room}. Pro also keeps ${listNames(names)}</span>`
        : `<span>Added ${room} ${room === 1 ? 'plant' : 'plants'}</span>`,
      ms: 4500, at: Date.now() } })
    go('save')
  }

  return (
    <Screen id="preview" back={() => go('q5')}
            offer={{ txt: 'See the whole calendar', onClick: () => go('paywall') }}
            scrollKey="preview"
            foot={<>
              <div className="btn b-pri" role="button" tabIndex={0} onClick={add}>
                Add {room === plan.length ? `these ${room}` : `the first ${room}`}
                {room === 1 ? ' plant' : ' plants'}
              </div>
              <div className="tlink2" role="button" tabIndex={0} onClick={() => go('add-plant')}>
                I’ll pick my own
              </div>
            </>}>
      <div className="greet">Your plan is ready</div>
      <div className="cap-f" style={{ fontSize: 'var(--t-31)', lineHeight: 1.06, marginTop: 4 }}>
        {plan.length} {plan.length === 1 ? 'plant.' : 'plants.'}<br />{second}
      </div>
      <div style={{ fontSize: 'var(--t-13)', color: 'var(--muted)', marginTop: 8 }}>
        {(c.outdoor ? zipInfo(c.zip).city + ' · ' : '') + c.sun + ' · ' + anA(c.space)
         + ' · about ' + mins + ' min a week'}
      </div>

      {/* ⚠ Цитата — плейсхолдер: настоящий отзыв надо получить у реального
          человека с его согласия, выдумывать его нельзя. */}
      <div className="quote">
        <div className="qmark">“</div>
        <p>{q[0]}</p>
        <div className="qwho">
          <div className="qav">{c.track === 'edible' ? 'MG' : 'PS'}</div>
          <div><b>{q[1]}</b><s>{q[2]}</s></div>
        </div>
      </div>

      <div className="acc">
        <div className="row1"><span className="tag">Your plan</span></div>
        <div className="plants">
          {plan.map(sp => (
            <div className="prow" key={sp.id}>
              <SpThumb s={sp} />
              <div className="nm"><b>{sp.name}</b><s>{spSub(sp, s.units, fmtPot)}</s></div>
              <div className="rt">
                {sp.kind === 'edible' ? dateAfter(sp.days) : `every ${sp.water}d`}
              </div>
            </div>
          ))}
        </div>
        <div className="accwhy" dangerouslySetInnerHTML={{ __html: planWhy(plan, c) }} />
      </div>

    </Screen>
  )
}

export function SaveScreen({ go }: { go: Go }) {
  const { s } = useStore()
  const c = usePlanCtx()
  const plan = s.plants.length ? s.plants.map(p => p.s) : buildPlan(c)
  return (
    <div className="screen on" id="s-save">
      <div className="shot" style={{ backgroundImage: bg('hero-basket') }} />
      <div className="scrim" />
      <div className="overlay">
        <div className="sb"><span>9:41</span>
          <span style={{ letterSpacing: '.06em' }}>
            <Icon name="sun" color="#fff" size={15} sw={2} />
          </span></div>
        <div style={{ flex: 1 }} />
        <span className="pill b-lime" style={{ alignSelf: 'flex-start' }}>
          {plan.length} {plan.length === 1 ? 'PLANT' : 'PLANTS'} ·{' '}
          {c.outdoor ? `${seasonWeeks(c.zip)} WEEKS` : 'YEAR-ROUND'}
        </span>
        <div className="cap-f" style={{ fontSize: 'var(--t-40)', lineHeight: 1.03, marginTop: 16 }}>
          Save your plan<br /><span style={{ color: 'var(--lime)' }}>so we can remind you.</span>
        </div>
        <div style={{ fontSize: 'var(--t-16)', color: '#DCE7DE', lineHeight: 1.5, marginTop: 12 }}>
          Your plan is already built. This just saves it. We email you a few tasks a week —
          nothing else.
        </div>
        <div style={{ marginTop: 16 }}><Providers go={go} from="save" /></div>
      </div>
    </div>
  )
}
