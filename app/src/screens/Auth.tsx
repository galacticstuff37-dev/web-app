// Вход. Три способа: Google, Apple, почта с кодом.
//
// ВАЖНО, что здесь НЕ происходит: у прототипа нет бэкенда, поэтому письмо с
// кодом никто не отправляет и код не проверяется на сервере. Это написано на
// самом экране — притворяться авторизацией нельзя. Валидация адреса, состояния
// кнопок, таймер повторной отправки и ошибки — настоящие.
//
// Чтобы включить НАСТОЯЩИЙ Google:
//   1. Google Cloud Console → Credentials → OAuth client ID (Web application),
//      в Authorized JavaScript origins добавить https://<домен> (для Pages —
//      https://galacticstuff37-dev.github.io).
//   2. Подключить https://accounts.google.com/gsi/client и вызвать
//      google.accounts.id.initialize({ client_id, callback }).
//   3. В callback раскодировать credential (JWT) и взять из него email —
//      вместо demoSignIn ниже.
// Apple — через Sign in with Apple JS: Services ID, домен и return URL в
// Apple Developer, дальше AppleID.auth.init/signIn.
// Кода для этого здесь нет намеренно: непроверяемый код в прототипе хуже, чем
// его отсутствие.

import { useEffect, useRef, useState } from 'react'
import { Screen } from '../components/Chrome'
import { ASSET_ROOT, bg } from '../lib/assets'
import { Icon } from '../icons/Icon'
import { useStore, type AuthVia } from '../state/store'

type Go = (id: string) => void

/** Официальный логотип Google (img/google-g.png, см. img/CREDITS.txt). */
const GOOGLE_LOGO = ASSET_ROOT + 'img/google-g.png'

/** Знак Apple — глиф U+F8FF из системного SF Pro Text, снят из шрифта, а не
    нарисован от руки. Брендовые кнопки требуют родной формы знака. */
const APPLE_MARK = 'M859 248C907 190 941 111 941 31C941 20 940 9 938 0C860 3 766 52 710 118C666 168 625 248 625 328C625 340 627 352 628 356C633 357 641 358 649 358C719 358 807 311 859 248ZM914 375C797 375 748 431 667 431C584 431 511 379 404 379C299 379 187 443 116 553C16 708 33 1000 196 1250C254 1341 332 1443 434 1444C525 1445 551 1386 675 1385C800 1384 823 1444 914 1444C1016 1443 1098 1331 1156 1240C1198 1174 1214 1141 1246 1067C1013 978 976 646 1206 519C1136 431 1037 375 914 375Z'

/** Помеченный плейсхолдер: без client_id настоящего адреса взять негде. */
const DEMO_EMAIL = 'demo@homegrown.app'

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i
/** Код, которым в прототипе можно посмотреть состояние ошибки. */
const BAD_CODE = '000000'
// 60, а не 30: Supabase пускает новый код на один адрес раз в 60 секунд
// (docs → Auth → Rate limits). Таймер короче лимита обещал бы то, что сервер
// откажет, и «Resend code» отдавал бы ошибку.
const RESEND_S = 60

function AppleMark({ size = 17 }: { size?: number }) {
  return (
    <svg width={size * 0.813} height={size} viewBox="0 0 1261 1551" aria-hidden="true">
      <path d={APPLE_MARK} fill="currentColor" />
    </svg>
  )
}

/** Список способов входа. Один и тот же на экране онбординга и на возврате. */
export function Providers({ go, from }: { go: Go; from: string }) {
  const { d } = useStore()
  // Без client_id вход демонстрационный, и это видно: подпись в аккаунте
  // говорит прямо, что провайдер не подключён.
  const demoSignIn = (via: AuthVia) => {
    d({ t: 'authFrom', v: from })
    d({ t: 'signIn', v: { email: DEMO_EMAIL, via, demo: true } })
    d({ t: 'toast', v: { html: `<span>Demo sign-in — ${via === 'google' ? 'Google' : 'Apple'} `
      + 'is not wired to this build yet</span>', ms: 4000, at: Date.now() } })
    go(from === 'save' ? 'paywall' : 'home')
  }
  return (
    <>
      <div className="btn b-white prov" role="button" tabIndex={0}
           onClick={() => demoSignIn('google')}
           onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); demoSignIn('google') } }}>
        <img className="prov-ic" src={GOOGLE_LOGO} alt="" width={18} height={18} />
        <span>Continue with Google</span>
      </div>
      <div className="btn prov b-dark" role="button" tabIndex={0}
           onClick={() => demoSignIn('apple')}
           onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); demoSignIn('apple') } }}>
        <span className="prov-ic"><AppleMark /></span>
        <span>Continue with Apple</span>
      </div>
      <div className="btn b-ghost" role="button" tabIndex={0}
           onClick={() => { d({ t: 'authFrom', v: from }); go('email') }}
           onKeyDown={e => {
             if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); d({ t: 'authFrom', v: from }); go('email') }
           }}>Continue with email</div>
    </>
  )
}

// ─────────────────────────────────────────── Возврат: «уже есть аккаунт»
export function SignInScreen({ go }: { go: Go }) {
  return (
    <Screen id="signin" back={() => go('landing')} scrollKey="signin">
      <div className="h1" style={{ marginTop: 16 }}>Welcome back</div>
      <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', marginTop: 4 }}>
        Your plants and their schedule are waiting.
      </div>
      <div style={{ marginTop: 16 }}><Providers go={go} from="signin" /></div>
      <div className="tlink2" role="button" tabIndex={0} style={{ marginTop: 16 }}
           onClick={() => go('q0')}>New here? Start free</div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Почта
export function EmailScreen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const [val, setVal] = useState(s.authEmail)
  const [err, setErr] = useState('')
  const ok = EMAIL_RE.test(val.trim())

  const send = () => {
    if (!ok) { setErr('That address looks off — check it once more.'); return }
    d({ t: 'authEmail', v: val.trim().toLowerCase() })
    go('code')
  }

  return (
    <Screen id="email" back={() => go(s.authFrom === 'save' ? 'save' : 'signin')} scrollKey="email"
            foot={
              <div className={'btn b-pri' + (ok ? '' : ' off')} role="button" tabIndex={0}
                   onClick={send}
                   onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); send() } }}>
                Send me a code
              </div>
            }>
      <div className="h1" style={{ marginTop: 16 }}>What’s your email?</div>
      <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', marginTop: 4 }}>
        We send a 6-digit code. No password to remember.
      </div>

      <label className={'fld' + (err ? ' bad' : '')} style={{ marginTop: 16 }}>
        <span className="fld-l">Email</span>
        <input type="email" inputMode="email" autoComplete="email" autoCapitalize="off"
               autoCorrect="off" spellCheck={false} enterKeyHint="go" name="email"
               placeholder="you@email.com" value={val}
               onChange={e => { setVal(e.target.value); if (err) setErr('') }}
               onKeyDown={e => { if (e.key === 'Enter') send() }} />
      </label>
      {err && <div className="fld-err" role="alert">{err}</div>}

      <div className="note" style={{ marginTop: 16 }}>
        <b>This build does not send mail</b>
        <p>There is no server behind the prototype yet, so no code arrives. On the next
          screen any six digits sign you in — that is the demo, not the product.</p>
      </div>
    </Screen>
  )
}

// ─────────────────────────────────────────── Код
export function CodeScreen({ go }: { go: Go }) {
  const { s, d } = useStore()
  const [code, setCode] = useState('')
  const [err, setErr] = useState('')
  const [left, setLeft] = useState(RESEND_S)
  const box = useRef<HTMLInputElement>(null)

  // Таймер повторной отправки: секунду за секундой, без перерисовки экрана.
  useEffect(() => {
    if (left <= 0) return
    const t = window.setTimeout(() => setLeft(left - 1), 1000)
    return () => window.clearTimeout(t)
  }, [left])

  useEffect(() => { box.current?.focus() }, [])

  const full = code.length === 6
  const submit = (val = code) => {
    if (val.length !== 6) return
    if (val === BAD_CODE) {
      setErr('That code has expired. Ask for a new one.')
      setCode('')
      return
    }
    d({ t: 'signIn', v: { email: s.authEmail, via: 'email', demo: true } })
    go(s.authFrom === 'save' ? 'paywall' : 'home')
  }

  // Шестая цифра отправляет сама: на телефоне клавиатура накрывает подвал, и
  // кнопка под ней недосягаема, пока не свернёшь ввод. Кнопка остаётся для
  // повторной попытки и для тех, кто ходит с клавиатуры.
  const onDigits = (raw: string) => {
    const next = raw.replace(/\D/g, '').slice(0, 6)
    setCode(next)
    if (err) setErr('')
    if (next.length === 6) submit(next)
  }

  return (
    <Screen id="code" back={() => go('email')} scrollKey="code"
            foot={
              <div className={'btn b-pri' + (full ? '' : ' off')} role="button" tabIndex={0}
                   onClick={() => submit()}
                   onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); submit() } }}>
                Sign in
              </div>
            }>
      <div className="h1" style={{ marginTop: 16 }}>Enter the code</div>
      <div style={{ fontSize: 'var(--t-14)', color: 'var(--muted)', marginTop: 4 }}>
        {s.authEmail
          ? <>Sent to <b style={{ color: 'var(--ink)' }}>{s.authEmail}</b></>
          : 'Six digits from the email we just sent.'}
      </div>

      {/* Одно поле, а не шесть: шесть input-ов ломают вставку кода и автозаполнение
          из письма. Клетки — рисунок поверх, поле лежит прозрачным сверху. */}
      <label className={'otp' + (err ? ' bad' : '')} style={{ marginTop: 16 }}>
        <input ref={box} inputMode="numeric" autoComplete="one-time-code" name="one-time-code"
               pattern="[0-9]*" maxLength={6} enterKeyHint="go" aria-label="6-digit code"
               value={code}
               onChange={e => onDigits(e.target.value)}
               onKeyDown={e => { if (e.key === 'Enter') submit() }} />
        <span className="otp-cells" aria-hidden="true">
          {[0, 1, 2, 3, 4, 5].map(i => (
            <i key={i} className={code.length === i ? 'on' : undefined}>{code[i] || ''}</i>
          ))}
        </span>
      </label>
      {err && <div className="fld-err" role="alert">{err}</div>}

      <div className="otp-row">
        {left > 0
          ? <span className="otp-wait">Resend in {left}s</span>
          : <b role="button" tabIndex={0} onClick={() => { setLeft(RESEND_S); setCode(''); setErr('') }}>
              Resend code
            </b>}
        <span className="otp-sep">·</span>
        <b role="button" tabIndex={0} onClick={() => go('email')}>Use another email</b>
      </div>

      <div className="note" style={{ marginTop: 16 }}>
        <b>Demo: any six digits work</b>
        <p>No mail is sent — there is no server yet. Type <b>000000</b> to see what a
          rejected code looks like. With the backend on, a code lives 60 minutes
          and a new one can be asked once a minute.</p>
      </div>
    </Screen>
  )
}

/** Строка аккаунта в настройках: почта, способ входа и выход. */
export function AccountRow({ go }: { go: Go }) {
  const { s, d } = useStore()
  if (!s.account) {
    return (
      <div className="btn b-white" role="button" tabIndex={0} style={{ marginTop: 12 }}
           onClick={() => go('signin')}>Sign in</div>
    )
  }
  const via = s.account.via === 'google' ? 'Google'
            : s.account.via === 'apple' ? 'Apple' : 'Email code'
  return (
    <div className="acct">
      <div className="acc-who">
        <div className="acc-av" style={{ backgroundImage: bg('hero-plants') }} aria-hidden="true" />
        <div className="acc-tx">
          <b>{s.account.email}</b>
          <s>{via}{s.account.demo ? ' · demo sign-in, not wired yet' : ''}</s>
        </div>
        <span className="acc-go" role="button" tabIndex={0} aria-label="Sign out"
              onClick={() => { d({ t: 'signOut' }); go('signin') }}>
          <Icon name="x" color="#fff" size={17} sw={2.4} />
        </span>
      </div>
    </div>
  )
}
