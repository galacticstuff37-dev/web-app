// Маршрут /review — замена review.html: те же экраны в рамке телефона, индекс
// перенесённых экранов, переключатели состояний данных и заметки к экрану.
//
// Зачем он: обойти экраны глазами и убедиться, что порт совпал с оригиналом.
// Рядом с рамкой стоит iframe со старым прототипом на тот же экран, поэтому
// расхождения видно сразу, а не по памяти.

import { useState } from 'react'
import { CalendarScreen } from '../screens/Calendar'
import { GrowthScreen } from '../screens/Growth'
import { HomeScreen } from '../screens/Home'
import { PlantScreen } from '../screens/Plant'
import { ASSET_ROOT } from '../lib/assets'
import {
  seedHouseDemo, seedMixed, seedPlants, useStore, type Track, type Units,
} from '../state/store'
import type { Species } from '../data/species'
import './review.css'

const SCREENS: Array<{ id: string; title: string; note: string }> = [
  { id: 'home', title: 'Home',
    note: 'Один экран, два состояния. Пусто — акцентный блок зовёт добавить растение. '
        + 'Есть растения — health score, виджеты и список. Задачи недели считаются из '
        + 'растений, а не захардкожены: полив по просрочке, сбор для созревших, протирка '
        + 'листьев для крупных.' },
  { id: 'growth', title: 'Growth',
    note: 'История ухода. Один дашборд и карточки растений, у каждой свои снимки. '
        + 'Тап ведёт в карточку. Виджет календаря — вход на Harvest calendar.' },
  { id: 'plant', title: 'Plant detail',
    note: 'Второй виджет зависит от вида: комнатному — свет и влажность, съедобному — '
        + 'прогресс до сбора и типичный диапазон. Без настоящей фотографии стоит плитка '
        + 'с иконкой, а не битая картинка.' },
  { id: 'calendar', title: 'Harvest calendar',
    note: 'Два вида под два вопроса. This month — рейка месяцев и плитки, отсортированные '
        + 'по скорости до урожая. Whole year — непрерывные полосы, по две дорожки на '
        + 'культуру, группы cool/warm-season, пунктир заморозков и оранжевая линия сегодня. '
        + 'Окна выводятся из даты заморозков ZIP, длины сезона и дней до сбора.' },
]

interface Preset { k: string; label: string; apply: () => void }

export function Review() {
  const { s, d } = useStore()
  const [id, setId] = useState('calendar')
  const [side, setSide] = useState(true)
  const cur = SCREENS.find(x => x.id === id)!

  const presets: Preset[] = [
    { k: 'plants', label: '4 овоща',
      apply: () => { d({ t: 'plants', v: seedPlants() }); d({ t: 'choices', v: { track: 'edible', outdoor: true } }) } },
    { k: 'house', label: '4 комнатных',
      apply: () => { d({ t: 'plants', v: seedHouseDemo() }); d({ t: 'choices', v: { track: 'house', outdoor: false } }) } },
    { k: 'mixed', label: 'Смешанный',
      apply: () => { d({ t: 'plants', v: seedMixed() }); d({ t: 'choices', v: { track: 'both', outdoor: true } }) } },
    { k: 'empty', label: 'Пусто',
      apply: () => { d({ t: 'plants', v: [] }) } },
    { k: 'sill', label: 'Подоконник',
      apply: () => { d({ t: 'plants', v: seedPlants() }); d({ t: 'choices', v: { track: 'edible', outdoor: false, space: 'windowsill' } }) } },
  ]

  const go = (next: string) => { if (SCREENS.some(x => x.id === next)) setId(next) }
  const openSpecies = (_sp: Species) => { /* библиотека не портирована */ }

  const body = () => {
    switch (id) {
      case 'home': return <HomeScreen go={go} />
      case 'growth': return <GrowthScreen go={go} />
      case 'plant': return <PlantScreen go={go} />
      default: return <CalendarScreen go={go} openSpecies={openSpecies} />
    }
  }

  return (
    <div className="rv">
      <aside className="rv-side">
        <div className="rv-wm">HOMEGROWN · REACT</div>
        <h1 className="rv-h">Порт на React</h1>
        <p className="rv-p">
          Перенесены четыре экрана из 29: шасси, дизайн-система, модель сезона и
          самые сложные экраны. Остальные живут в исходном прототипе.
        </p>

        <div className="rv-lb">Экраны</div>
        <div className="rv-chips">
          {SCREENS.map(x => (
            <button key={x.id} className={'rv-chip' + (x.id === id ? ' on' : '')}
                    onClick={() => setId(x.id)}>{x.title}</button>
          ))}
        </div>

        <div className="rv-lb">Состояние данных</div>
        <div className="rv-chips">
          {presets.map(p => (
            <button key={p.k} className="rv-chip" onClick={p.apply}>{p.label}</button>
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

        <div className="rv-lb">Прочее</div>
        <div className="rv-chips">
          <button className={'rv-chip' + (s.isPro ? ' on' : '')}
                  onClick={() => d({ t: 'pro', v: !s.isPro })}>Pro</button>
          <button className={'rv-chip' + (s.units === 'metric' ? ' on' : '')}
                  onClick={() => d({ t: 'units', v: (s.units === 'metric' ? 'imperial' : 'metric') as Units })}>
            Метрика
          </button>
          <button className={'rv-chip' + (side ? ' on' : '')}
                  onClick={() => setSide(v => !v)}>Прототип рядом</button>
        </div>

        <div className="rv-lb">Заметка к экрану</div>
        <p className="rv-note">{cur.note}</p>

        <div className="rv-lb">Трек</div>
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
      </aside>

      <div className="rv-stage">
        <div>
          <div className="rv-cap">React · {cur.title}</div>
          <div className="phone">{body()}</div>
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
