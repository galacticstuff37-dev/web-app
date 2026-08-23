// Карточка растения. Второй виджет зависит от вида: комнатному — свет и
// влажность, съедобному — прогресс до сбора и «типичный диапазон».
// Если у вида нет настоящей фотографии, стоит плитка с иконкой, а не битая
// картинка: выдумывать ассеты нельзя.

import { Screen } from '../components/Chrome'
import { Arc, MetricRow, Note, PhotoTile } from '../components/bits'
import { useCamera } from '../components/parts'
import { IcPlus } from '../icons/Icon'
import { fmtPot, hPct, isEdible, pState, wDue, wPct, phUrl } from '../lib/plants'
import { useStore } from '../state/store'

export function PlantScreen({ go }: { go: (id: string) => void }) {
  const { s, d } = useStore()
  const p = s.plants[s.selected]
  const cam = useCamera(url => d({ t: 'addPhoto', v: { i: s.selected, url } }))

  if (!p) {
    return (
      <Screen id="plant" back={() => go('home')} nav={{ active: 'Week', go }} scrollKey="plant">
        <Note title="This plant is gone"
              cta={<div className="btn b-pri" role="button" tabIndex={0}
                        onClick={() => go('add-plant')}>Add a plant</div>}>
          You removed it. Nothing is lost — add it again whenever you like.
        </Note>
      </Screen>
    )
  }

  const st = pState(p)
  const due = wDue(p)
  const ready = isEdible(p) && hPct(p) >= 100

  return (
    <Screen id="plant" back={() => go('home')} nav={{ active: 'Week', go }}
            scrollKey={'plant' + s.selected}>
      <PhotoTile s={p.s} cls="det-ph" style={{ marginTop: 8 }} />

      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 16 }}>
        <div>
          <div style={{ fontSize: 'var(--t-24)', fontWeight: 600, letterSpacing: '-.02em' }}>
            {p.s.name}
          </div>
          {p.s.latin && (
            <div style={{ fontSize: 'var(--t-13)', color: 'var(--muted)', fontStyle: 'italic' }}>
              {p.s.latin}
            </div>
          )}
        </div>
        <div style={{ flex: 1 }} />
        <span className={'pill st-pill st-' + st[1]}>{st[0]}</span>
      </div>

      <div className="wgrid" style={{ marginTop: 12 }}>
        <div className="wg wg-dark">
          <div className="wg-top">
            <div className="num">{Math.max(0, due)}<span>d</span></div>
            <Arc pct={100 - wPct(p)} sz={44} dark />
          </div>
          <div className="lbl">{due <= 0 ? 'Water it today' : 'Until next water'}</div>
          <MetricRow items={[['Every', p.s.water + 'd'], ['Last', p.since + 'd ago']]} />
        </div>

        {isEdible(p)
          ? <div className="wg wg-lite">
              <div className="wg-top">
                <div className="num">{hPct(p)}<span>%</span></div>
                <Arc pct={hPct(p)} sz={44} />
              </div>
              <div className="lbl">{ready ? 'Ready to pick' : 'To first pick'}</div>
              <MetricRow items={[
                ['Pot', fmtPot(p.s.pot, s.units)],
                ['Typical', p.s.days + (p.s.daysMax !== p.s.days ? '–' + p.s.daysMax : '') + 'd'],
              ]} />
            </div>
          : <div className="wg wg-lite">
              <div className="wg-h"><b>Conditions</b></div>
              <MetricRow items={[['Light', p.s.light]]} />
              <MetricRow items={[['Humidity', p.s.hum]]} />
            </div>}
      </div>

      <div className="btn b-pri" role="button" tabIndex={0}
           onClick={() => d({ t: 'water', v: s.selected })}>Water it now</div>
      {ready && (
        <div className="btn b-ghost" role="button" tabIndex={0} onClick={() => go('harvest')}>
          Pick it — first harvest
        </div>
      )}

      <div className="sl">
        Journal{p.photos.length
          ? ` · ${p.photos.length} ${p.photos.length === 1 ? 'photo' : 'photos'}`
          : ''}
      </div>
      {p.photos.length > 0 && (
        <div className="jgrid">
          {p.photos.map((x, k) => (
            <figure className="jc" key={k}>
              <div className="jph" style={{ backgroundImage: `url(${phUrl(x)})` }} />
              <figcaption><b>{p.s.name}</b><s>Day {x.day} · {st[0]}</s></figcaption>
            </figure>
          ))}
        </div>
      )}
      <div className="btn-dash" role="button" tabIndex={0} onClick={cam.open}>
        <IcPlus /><span>{p.photos.length ? 'Add a photo' : 'Take the first photo'}</span>
      </div>
      {cam.input}

      <div className="btn b-ghost" role="button" tabIndex={0}
           onClick={() => { d({ t: 'remove', v: s.selected }); go('home') }}>
        Remove from my plants
      </div>
    </Screen>
  )
}
