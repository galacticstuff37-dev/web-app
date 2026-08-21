// Маршрут /review — замена review.html: все экраны в рамке телефона, индекс по
// группам, переключатели состояний данных и заметки к экрану.
//
// Рядом с рамкой стоит iframe со старым прототипом на тот же экран, поэтому
// расхождения видно сразу, а не по памяти.

import { useState } from 'react'
import { ASSET_ROOT } from '../lib/assets'
import { GROUPS, ROUTE, ROUTES } from '../routes'
import {
  seedHouseDemo, seedMixed, seedPlants, useStore, type Track, type Units,
} from '../state/store'
import { Toast } from '../components/parts'
import type { Species } from '../data/species'
import './review.css'

export function Review() {
  const { s, d } = useStore()
  const [id, setId] = useState('calendar')
  const [side, setSide] = useState(true)
  const cur = ROUTE(id) || ROUTES[0]

  const presets: Array<[string, () => void]> = [
    ['4 овоща', () => { d({ t: 'plants', v: seedPlants() })
                        d({ t: 'choices', v: { track: 'edible', outdoor: true } }) }],
    ['4 комнатных', () => { d({ t: 'plants', v: seedHouseDemo() })
                            d({ t: 'choices', v: { track: 'house', outdoor: false } }) }],
    ['Смешанный', () => { d({ t: 'plants', v: seedMixed() })
                          d({ t: 'choices', v: { track: 'both', outdoor: true } }) }],
    ['Пусто', () => d({ t: 'plants', v: [] })],
    ['Подоконник', () => { d({ t: 'plants', v: seedPlants() })
                           d({ t: 'choices', v: { track: 'edible', outdoor: false,
                                                  space: 'windowsill' } }) }],
  ]

  const go = (next: string) => { if (ROUTE(next)) setId(next) }
  const openSpecies = (_sp: Species) => setId('add-plant')

  return (
    <div className="rv">
      <aside className="rv-side">
        <div className="rv-wm">HOMEGROWN · REACT</div>
        <h1 className="rv-h">Порт на React</h1>
        <p className="rv-p">
          Все {ROUTES.length} экранов прототипа. Дизайн-система, иконки и справочник
          перенесены дословно; модель сезона и ухода — вручную и сверены числами.
        </p>

        {Object.entries(GROUPS).map(([group, list]) => (
          <div key={group}>
            <div className="rv-lb">{group}</div>
            <div className="rv-chips">
              {list.map(r => (
                <button key={r.id} className={'rv-chip' + (r.id === id ? ' on' : '')}
                        onClick={() => setId(r.id)}>{r.title}</button>
              ))}
            </div>
          </div>
        ))}

        <div className="rv-lb">Состояние данных</div>
        <div className="rv-chips">
          {presets.map(([label, apply]) => (
            <button key={label} className="rv-chip" onClick={apply}>{label}</button>
          ))}
        </div>

        <div className="rv-lb">Регион (от него считаются окна)</div>
        <div className="rv-chips">
          {[['78704', 'Austin'], ['97214', 'Portland'], ['10025', 'New York'], ['60613', 'Chicago']]
            .map(([z, city]) => (
              <button key={z} className={'rv-chip' + (s.choices.zip === z ? ' on' : '')}
                      onClick={() => d({ t: 'choices', v: { zip: z } })}>{city}</button>
            ))}
        </div>

        <div className="rv-lb">Трек и место</div>
        <div className="rv-chips">
          {(['edible', 'house', 'both'] as Track[]).map(t => (
            <button key={t} className={'rv-chip' + (s.choices.track === t ? ' on' : '')}
                    onClick={() => d({ t: 'choices', v: { track: t } })}>{t}</button>
          ))}
          <button className={'rv-chip' + (s.choices.outdoor ? ' on' : '')}
                  onClick={() => d({ t: 'choices', v: { outdoor: !s.choices.outdoor } })}>
            {s.choices.outdoor ? 'на улице' : 'в помещении'}
          </button>
        </div>

        <div className="rv-lb">Прочее</div>
        <div className="rv-chips">
          <button className={'rv-chip' + (s.isPro ? ' on' : '')}
                  onClick={() => d({ t: 'pro', v: !s.isPro })}>Pro</button>
          <button className={'rv-chip' + (s.units === 'metric' ? ' on' : '')}
                  onClick={() => d({ t: 'units',
                                     v: (s.units === 'metric' ? 'imperial' : 'metric') as Units })}>
            Метрика
          </button>
          <button className={'rv-chip' + (s.onbMode === 'own' ? ' on' : '')}
                  onClick={() => d({ t: 'onb', v: s.onbMode === 'own' ? null : 'own' })}>
            Ветка «уже есть»
          </button>
          <button className={'rv-chip' + (side ? ' on' : '')}
                  onClick={() => setSide(v => !v)}>Прототип рядом</button>
        </div>

        <div className="rv-lb">Заметка к экрану</div>
        <p className="rv-note">{cur.note}</p>
      </aside>

      <div className="rv-stage">
        <div>
          <div className="rv-cap">React · {cur.title}</div>
          <div className="phone">
            {cur.render({ go, openSpecies })}
            <Toast />
          </div>
        </div>
        {side && (
          <div>
            <div className="rv-cap">Прототип · тот же экран</div>
            <iframe className="rv-frame" title="прототип"
                    src={`${ASSET_ROOT}index.html#${id}`} />
          </div>
        )}
      </div>
    </div>
  )
}
