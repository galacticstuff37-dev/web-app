// Growth. История ухода: один дашборд и карточки растений, у каждой свои
// снимки. Раньше здесь были две сущности про одно и то же — список и отдельная
// сетка фото, хотя каждое фото и так принадлежит растению.

import { Screen } from '../components/Chrome'
import { Note } from '../components/bits'
import { IcCam, IcChev, IcPlus } from '../icons/Icon'
import { img } from '../lib/assets'
import { careStats, pState, verdict, wDue, type Photo, type Plant } from '../lib/plants'
import { useStore } from '../state/store'
import { CalendarWidget } from './Calendar'

export const phUrl = (x: Photo) => x.u || img(x.f || '')

function PlantRow({ p, i, onOpen }: { p: Plant; i: number; onOpen: (i: number) => void }) {
  const st = pState(p)
  return (
    <div className="ccard">
      <div className="chead" role="button" tabIndex={0} onClick={() => onOpen(i)}
           onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpen(i) } }}>
        <div className="nm"><b>{p.s.name}</b><s className={'st-' + st[1]}>{st[0]}</s></div>
        <IcChev />
      </div>
      {p.photos.length
        ? <div className="cstrip">
            {p.photos.map((x, k) => (
              <div key={k} style={{ backgroundImage: `url(${phUrl(x)})` }} />
            ))}
          </div>
        : <div className="cempty" role="button" tabIndex={0}>
            <IcCam /><span>No photos yet — take one</span>
          </div>}
    </div>
  )
}

export function GrowthScreen({ go }: { go: (id: string) => void }) {
  const { s, d } = useStore()
  const st = careStats(s.plants)
  const open = (i: number) => { d({ t: 'select', v: i }); go('plant') }

  if (!s.plants.length) {
    return (
      <Screen id="growth" nav={{ active: 'Growth', go }}
              offer={{ txt: 'Keep every photo', onClick: () => go('paywall') }} scrollKey="growth">
        <div className="h1">Your plants</div>
        <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', marginTop: 4 }}>
          No plants yet
        </div>
        <Note title="Nothing to show yet"
              cta={<div className="btn b-pri" role="button" tabIndex={0}
                        onClick={() => go('add-plant')}>Add a plant</div>}>
          Add a plant and this page starts keeping its history — waterings, photos,
          how it changed.
        </Note>
      </Screen>
    )
  }

  const v = verdict(st.score, st.due)
  const thirsty: Array<[Plant, number]> = []
  const fine: Array<[Plant, number]> = []
  s.plants.forEach((p, i) => { (wDue(p) <= 2 ? thirsty : fine).push([p, i]) })

  return (
    <Screen id="growth" nav={{ active: 'Growth', go }}
            offer={{ txt: 'Keep every photo', onClick: () => go('paywall') }} scrollKey="growth">
      <div className="h1">Your plants</div>
      <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', marginTop: 4 }}>
        {st.plants} {st.plants === 1 ? 'plant in your care' : 'plants in your care'}
      </div>

      <div className="acc">
        <div className="row1"><span className="tag">Plant parent</span></div>
        <div className="lbl">Health score</div>
        <div className="scorehead">
          <div className="huge">{st.score}</div>
          <div className="huge-of">of 100</div>
        </div>
        <div className="pb-track accbar"><i style={{ width: st.score + '%' }} /></div>
        <div className="sub">
          {v[0]} — {v[1].toLowerCase()}. {st.photos} {st.photos === 1 ? 'photo' : 'photos'} in the journal.
        </div>
        <div className="duo">
          <div className="cell"><s>Thirsty</s><b>{st.due}</b></div>
          <div className="cell"><s>Soon</s><b>{st.soon}</b></div>
          <div className="cell"><s>Fine</s><b>{st.healthy}</b></div>
        </div>
      </div>

      <div className="wgrid"><CalendarWidget go={go} /></div>

      {thirsty.length > 0 && <>
        <div className="sl">Needs attention</div>
        {thirsty.map(([p, i]) => <PlantRow key={i} p={p} i={i} onOpen={open} />)}
      </>}
      {fine.length > 0 && <>
        <div className="sl">Doing fine</div>
        {fine.map(([p, i]) => <PlantRow key={i} p={p} i={i} onOpen={open} />)}
      </>}
      <div className="btn-dash" role="button" tabIndex={0}>
        <IcPlus /><span>Add a photo</span>
      </div>
    </Screen>
  )
}
