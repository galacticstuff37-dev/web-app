# Бэкенд HOMEGROWN: Postgres на Supabase

Сайт живёт на classic GitHub Pages из ветки `main` — это статика, серверного
кода там быть не может, а браузер не умеет говорить с Postgres напрямую (у него
TCP-протокол). Поэтому база берётся хостингом, который отдаёт её по HTTP:
Supabase = Postgres + PostgREST + Auth + Storage + Cron в одном проекте.

Приложение остаётся **local-first**: `localStorage` — кеш и источник
мгновенности (все 32 экрана продолжают открываться без сети), Postgres —
синхронизация между устройствами и то, из чего планировщик считает напоминания.

## Что в этой папке

| Файл | Что это |
|---|---|
| `migrations/0001_init.sql` | Схема: профиль, растения, журнал снимков, отметки задач недели, подписки на пуш, лог отправок. RLS на всех таблицах |
| `local-stub.sql` | Заглушка схемы `auth` для локальной проверки. **На Supabase не применять** — там она есть |

Миграция проверена на живом Postgres 17: ограничения отбивают мусор (`zip 123`,
`effort 5`, снимок сразу и из `/img`, и из Storage), профиль создаётся триггером
вместе с аккаунтом, `updated_at` растёт при изменении, мягкое удаление оставляет
строку для синхронизации, удаление аккаунта уносит растения и снимки каскадом,
а RLS не отдаёт чужие строки и не даёт записать растение на чужой `user_id`.

## Что нужно сделать тебе (аккаунты я не создаю)

1. **Проект.** supabase.com → New project. Регион — US East или US West: рынок
   американский, и планировщик будет считать заморозки по ZIP.
2. **Схема.** SQL Editor → вставить `migrations/0001_init.sql` → Run.
3. **Вход по коду.** Authentication → Providers → Email: включить, **Confirm
   email** оставить включённым.
   Затем Authentication → Emails → шаблон **Magic Link**: заменить ссылку на
   `{{ .Token }}`. Без этой правки Supabase присылает ссылку, а у нас экран на
   шесть цифр — придёт письмо не про то, что показано.
   Там же Advanced: OTP length = 6, OTP expiry = 600 (10 минут; на экране
   таймер повторной отправки 30 с).
4. **Google.** Authentication → Providers → Google: включить и вставить Client
   ID и Client Secret из Google Cloud Console. В самой Console, в OAuth-клиенте:
   - Authorized JavaScript origins: `https://galacticstuff37-dev.github.io`
   - Authorized redirect URIs: `https://<project-ref>.supabase.co/auth/v1/callback`
5. **Apple.** Authentication → Providers → Apple: Services ID, Team ID, Key ID и
   `.p8`-ключ из Apple Developer. Return URL там же — тот же
   `https://<project-ref>.supabase.co/auth/v1/callback`.
6. **URL приложения.** Authentication → URL Configuration:
   - Site URL: `https://galacticstuff37-dev.github.io/web-app/react/`
   - Redirect URLs: добавить и её, и `http://localhost:5173/**` для разработки.
7. **Снимки.** Storage → New bucket `photos`, **приватный**. Политики: путь
   начинается с `auth.uid()`, то есть человек пишет и читает только свою папку.
8. **Отдать мне два значения** (оба публичные, лежат в репозитории спокойно):
   - Project URL: `https://<project-ref>.supabase.co`
   - `anon` public key

**Ключ `service_role` в репозиторий не попадает никогда.** Он нужен только
планировщику напоминаний (Edge Function) и живёт в секретах проекта: у него
права в обход RLS, и на статическом сайте он означал бы «любой читает всё».

## Что я делаю дальше, получив URL и anon key

1. Подключаю `@supabase/supabase-js`, заменяю демонстрационный вход настоящим:
   `signInWithOtp({ email })` → `verifyOtp({ email, token })` для почты и
   `signInWithOAuth({ provider })` для Google и Apple. Экраны не меняются —
   они с самого начала собраны под этот флоу, и уйдут только оговорки «письмо
   не отправляется» и «demo sign-in».
2. Слой синхронизации поверх `localStorage`: при входе — тянем и сливаем по
   `updated_at`, при изменении — пишем в базу. Экраны остаются мгновенными и
   работают без сети.
3. Снимки с камеры уезжают в bucket `photos` вместо data-URL в `localStorage`
   (сейчас квота ≈5 МБ, около 30 кадров).
4. `last_seen_at` оживляет три уже нарисованных экрана возврата (`week-back`,
   `week-long`, `season-end`) — сейчас в продукте они недостижимы.
5. Только после этого — напоминания: Edge Function по расписанию считает
   `wDue` по растениям, берёт `remind_at` и `tz`, проверяет `notification_log`
   (не больше одного пуша в день на событие) и отправляет веб-пуш по
   `push_subscriptions`. Для пуша в порт добавляется service worker с
   обработчиками `push`/`notificationclick` — сейчас его там нет.

## Чего этот переезд стоит

Наивный переезд «всё через сеть» испортил бы то, что уже проверено: каждый
экран получил бы загрузку и ошибку, а `#review` и свипы перестали бы
открываться без входа. Поэтому local-first, а не замена хранилища.
