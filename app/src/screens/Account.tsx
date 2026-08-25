// Экран аккаунта. Отвечает на три вопроса, которые до него задать было некому:
// в какой я аккаунт вошёл, как именно я в него попал и что из моего уже лежит на
// сервере, а что пока только здесь.
//
// Цифры берутся из снимка последней отправки (lib/sync.ts), а не запросом: снимок
// И ЕСТЬ ответ на «что уже в базе», он лежит рядом с состоянием и читается
// мгновенно. Поэтому у экрана нет ни спиннера, ни состояния «не удалось».
//
// Sign out и Delete account переехали сюда с экрана настроек: там они висели
// среди тумблеров, а это не настройка, а действие над аккаунтом.

import { useEffect, useState } from 'react'
import { Screen } from '../components/Chrome'
import { Confirm } from '../components/Confirm'
import { bg } from '../lib/assets'
import { allPhotos } from '../lib/plants'
import { MON } from '../lib/season'
import { supa } from '../lib/supabase'
import { forgetSnap, syncFacts, wipeCloud } from '../lib/sync'
import { useStore } from '../state/store'

type Go = (id: string) => void

/**
 * «Когда» человеческим языком. Точное время тут никому не нужно: вопрос звучит
 * как «свежее ли это», а не «во сколько именно».
 */
function ago(iso: string): string {
  const m = Math.round((Date.now() - new Date(iso).getTime()) / 60000)
  if (m < 1) return 'just now'
  if (m < 60) return `${m} ${m === 1 ? 'minute' : 'minutes'} ago`
  const h = Math.round(m / 60)
  if (h < 24) return `${h} ${h === 1 ? 'hour' : 'hours'} ago`
  const d = Math.round(h / 24)
  if (d === 1) return 'yesterday'
  if (d < 7) return `${d} days ago`
  const t = new Date(iso)
  return `${MON[t.getMonth()]} ${t.getDate()}`
}

const plural = (n: number, one: string) => `${n} ${n === 1 ? one : one + 's'}`

/** Строка-факт: та же строка списка, но она никуда не ведёт и не притворяется. */
function FactRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="pl flat">
      <div className="nm"><b>{label}</b></div>
      <span className="setval">{value}</span>
    </div>
  )
}

export function AccountScreen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const [ask, setAsk] = useState(false)
  const acc = s.account

  // Без аккаунта экрана нет: в настройках на его месте кнопка Sign in. Если
  // сюда пришли ссылкой — уводим, а не показываем пустую страницу.
  //
  // Проверка ОДИН РАЗ на входе, а не слежка за acc. Слежка перебивала переходы
  // самих действий: выход и удаление обнуляют аккаунт и сами уводят куда надо
  // (home и landing), а эффект успевал в том же коммите отправить в settings —
  // человек стирал всё и попадал в настройки вместо начала.
  useEffect(() => {
    if (!acc) go('settings')
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
  if (!acc) return null

  const f = syncFacts(s, acc.uid || null)
  const via = acc.via === 'google' ? 'Google'
            : acc.via === 'apple' ? 'Apple' : 'Email code'

  const signOut = async () => {
    // У демонстрационного входа сессии на сервере нет — закрывать нечего.
    if (!acc.demo) await (await supa()).auth.signOut()
    // Снимок отправки привязан к аккаунту: оставить его — значит дать
    // следующему человеку на этом устройстве чужие id строк.
    forgetSnap()
    d({ t: 'signOut' })
    go('home')
  }

  // Delete account убирает и копию в базе: без этого «Your plants go with it» —
  // ложь, при следующем входе сад приехал бы обратно.
  const wipe = () => {
    void supa().then(async sb => { await wipeCloud(sb); await sb.auth.signOut() })
      .catch(() => { /* без сети уборка не состоялась: сад вернётся при входе */ })
    d({ t: 'wipe' })
    go('landing')
  }

  const photos = allPhotos(s.plants).length
  const cloud = f.plants || f.photos
    ? [plural(f.plants, 'plant'), f.photos ? plural(f.photos, 'photo') : '']
        .filter(Boolean).join(' · ')
    : acc.demo ? 'Nothing' : 'Nothing yet'

  return (
    <Screen id="account" back={() => go('settings')} nav={{ active: 'Settings', go }}
            scrollKey="account"
            overlay={ask ? (
              <Confirm title="Delete everything?"
                       body={`${plural(s.plants.length, 'plant')}`
                           + (photos ? ` and ${plural(photos, 'photo')}` : '')
                           + ', your ZIP, your light and every reminder go with it — here and'
                           + ' on the server. This cannot be undone.'}
                       yes="Delete it all" no="Keep my plants"
                       onYes={wipe} onNo={() => setAsk(false)} />
            ) : undefined}>
      <div className="h1" style={{ marginTop: 16 }}>Account</div>

      <div className="acct">
        <div className="acc-who">
          <div className="acc-av" style={{ backgroundImage: bg('hero-plants') }} aria-hidden="true" />
          <div className="acc-tx">
            <b>{acc.email}</b>
            <s>Signed in with {via}{acc.demo ? ' · demo, not wired yet' : ''}</s>
          </div>
        </div>
      </div>

      <div className="sl">Your data</div>
      <div className="plist">
        <FactRow label="On the server" value={cloud} />
        <FactRow label="Last synced"
                 value={f.at ? ago(f.at) : acc.demo ? 'Never' : 'Not yet'} />
        {f.localOnly > 0 && (
          <FactRow label="Only on this phone" value={plural(f.localOnly, 'photo')} />
        )}
      </div>

      {acc.demo ? (
        <div className="note">
          <b>This sign-in is a demo</b>
          <p>The screens are real, the account is not: no code was sent and no server
            knows about it. Nothing syncs until you sign in with Google.</p>
        </div>
      ) : f.error ? (
        <div className="note">
          <b>Last sync did not go through</b>
          <p>{f.error}. Your plants are safe on this phone — the next change tries
            again on its own.</p>
        </div>
      ) : !f.at ? (
        <div className="note">
          <b>Nothing has gone up yet</b>
          <p>It happens by itself the moment you change something — water a plant,
            tick a task, edit a setting. There is no button to press.</p>
        </div>
      ) : f.localOnly > 0 ? (
        <div className="note">
          <b>Camera photos stay here for now</b>
          <p>They need file storage, which comes next. Plants, tasks and settings are
            already on the server and will follow you to another phone.</p>
        </div>
      ) : (
        <div className="note">
          <b>Open it anywhere</b>
          <p>Sign in with the same Google account on another phone or laptop and this
            garden is there — same plants, same schedule, same settings.</p>
        </div>
      )}

      <div className="btn b-ghost" role="button" tabIndex={0} style={{ marginTop: 16 }}
           onClick={signOut}
           onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); void signOut() } }}>
        Sign out
      </div>
      <div className="dangernote" style={{ marginTop: 8 }}>
        Signing out leaves your plants on this phone.
      </div>

      <div className="danger" role="button" tabIndex={0}
           onClick={() => setAsk(true)}
           onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setAsk(true) } }}>
        Delete account
      </div>
      <div className="dangernote">Wipes your plants and settings here and on the
        server, and takes you back to the start.</div>
    </Screen>
  )
}
