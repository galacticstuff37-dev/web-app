-- HOMEGROWN: схема бэкенда. Postgres (Supabase).
--
-- Принципы, из которых она выведена:
--   * Справочник видов остаётся В КОДЕ (app/src/data/species.ts) — он меняется
--     вместе с логикой окон посева, и дублировать его в базе значило бы иметь
--     две расходящиеся правды. В базе от вида хранится только id.
--   * Приложение остаётся local-first: localStorage — кеш и источник
--     мгновенности, база — синхронизация. Поэтому у каждой строки есть
--     updated_at, а удаление мягкое (deleted_at): иначе другое устройство
--     никогда не узнает, что растение убрали.
--   * Время напоминания хранится как время, а не как индекс массива из клиента,
--     и рядом лежит часовой пояс: планировщик обязан попасть в 18:00 по месту
--     человека, а не по UTC.
--   * RLS включён везде и без исключений: строку видит только её владелец.
--
-- Применение: SQL Editor проекта или `supabase db push`. Локальная проверка —
-- см. supabase/local-stub.sql (там заглушка схемы auth, которую даёт Supabase).

-- ───────────────────────────────────────────── общее

create extension if not exists pgcrypto;      -- gen_random_uuid()

-- Ставит updated_at на каждое изменение: по нему идёт синхронизация.
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end $$;

-- ───────────────────────────────────────────── профиль и настройки

-- Одна строка на человека: всё, что в клиенте лежит в choices/care/mail и
-- рядом. Отдельными колонками, а не одним jsonb: по zip и по времени
-- напоминания планировщик будет выбирать людей, а по jsonb это индексируется
-- плохо и ошибку в имени поля никто не поймает.
create table public.profiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  email         text,

  -- онбординг
  track         text not null default 'edible' check (track in ('edible','house','both')),
  space         text not null default 'patio',
  outdoor       boolean not null default true,
  sun           text not null default '6–8 hours of sun',
  sun_rank      smallint not null default 2 check (sun_rank between 1 and 3),
  goals         text[] not null default '{}',
  effort        smallint not null default 4 check (effort in (3,4,6)),
  zip           text check (zip ~ '^[0-9]{5}$'),

  -- настройки
  units         text not null default 'imperial' check (units in ('imperial','metric')),
  cal_view      text not null default 'month' check (cal_view in ('month','year')),
  remind_at     time not null default '18:00',
  tz            text not null default 'UTC',        -- IANA, для планировщика
  care_pick     boolean not null default true,
  care_leaf     boolean not null default true,
  care_rotate   boolean not null default true,
  care_feed     boolean not null default true,
  mail_weekly   boolean not null default true,
  mail_water    boolean not null default true,
  mail_news     boolean not null default false,

  -- деньги и возвраты
  is_pro        boolean not null default false,
  pro_until     timestamptz,
  trial_ends_at timestamptz,

  -- «когда заходил в последний раз»: без этого экраны возврата после пропуска
  -- (week-back, week-long, season-end) в продукте недостижимы
  last_seen_at  timestamptz,

  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create trigger profiles_touch before update on public.profiles
  for each row execute function public.touch_updated_at();

-- Профиль появляется вместе с аккаунтом: клиенту не нужно помнить, что его
-- надо создать, и «профиля нет» не становится состоянием, которое он чинит.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email) values (new.id, new.email)
  on conflict (id) do nothing;
  return new;
end $$;

create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- ───────────────────────────────────────────── растения

create table public.plants (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) on delete cascade,
  -- id вида из справочника в коде; текстом, потому что таблицы видов тут нет
  species_id  text not null,
  since       integer not null default 0 check (since >= 0),   -- дней с полива
  day         integer not null default 0 check (day >= 0),     -- возраст, дней
  sort        integer not null default 0,                      -- порядок в списке
  added_at    timestamptz not null default now(),
  deleted_at  timestamptz,                                     -- мягкое удаление
  updated_at  timestamptz not null default now()
);

create index plants_user_idx on public.plants (user_id) where deleted_at is null;
create trigger plants_touch before update on public.plants
  for each row execute function public.touch_updated_at();

-- ───────────────────────────────────────────── журнал снимков

-- Два вида кадров, как в клиенте: готовое фото вида из /img (stock, имя файла)
-- и снимок человека (upload, путь в Storage). Один из двух обязателен — иначе
-- в журнале появится карточка без картинки.
create table public.photos (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null references auth.users(id) on delete cascade,
  plant_id     uuid not null references public.plants(id) on delete cascade,
  kind         text not null check (kind in ('stock','upload')),
  stock_name   text,
  storage_path text,
  day          integer not null default 0 check (day >= 0),
  taken_at     timestamptz not null default now(),
  deleted_at   timestamptz,
  updated_at   timestamptz not null default now(),
  constraint photos_source check (
    (kind = 'stock'  and stock_name is not null and storage_path is null) or
    (kind = 'upload' and storage_path is not null and stock_name is null))
);

create index photos_plant_idx on public.photos (plant_id) where deleted_at is null;
create trigger photos_touch before update on public.photos
  for each row execute function public.touch_updated_at();

-- ───────────────────────────────────────────── отметки задач недели

-- Ключ задачи в клиенте привязан к позиции растения (water:0, pick:1) и живёт
-- одну неделю. Поэтому неделя — часть ключа: без неё прошлые отметки гасили бы
-- задачи следующей недели.
create table public.week_tasks (
  user_id    uuid not null references auth.users(id) on delete cascade,
  week_start date not null,
  task_key   text not null,
  done       boolean not null default true,
  updated_at timestamptz not null default now(),
  primary key (user_id, week_start, task_key)
);

create trigger week_tasks_touch before update on public.week_tasks
  for each row execute function public.touch_updated_at();

-- ───────────────────────────────────────────── подписки на пуш и лог отправок

create table public.push_subscriptions (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null references auth.users(id) on delete cascade,
  endpoint   text not null unique,
  p256dh     text not null,
  auth       text not null,
  user_agent text,
  created_at timestamptz not null default now(),
  failed_at  timestamptz          -- после 410 от сервиса пуша подписку гасим
);

create index push_user_idx on public.push_subscriptions (user_id) where failed_at is null;

-- Лог нужен не для истории, а для правил из каталога оповещений: не больше
-- одного пуша в день и одно событие не уходит в два канала в один день.
create table public.notification_log (
  id       uuid primary key default gen_random_uuid(),
  user_id  uuid not null references auth.users(id) on delete cascade,
  kind     text not null,         -- water_due, harvest_ready, frost_soon, …
  channel  text not null check (channel in ('push','email')),
  sent_on  date not null default current_date,
  sent_at  timestamptz not null default now(),
  unique (user_id, kind, channel, sent_on)
);

create index notif_user_day_idx on public.notification_log (user_id, sent_on);

-- ───────────────────────────────────────────── RLS

alter table public.profiles           enable row level security;
alter table public.plants             enable row level security;
alter table public.photos             enable row level security;
alter table public.week_tasks         enable row level security;
alter table public.push_subscriptions enable row level security;
alter table public.notification_log   enable row level security;

create policy profiles_self on public.profiles
  for all using (id = auth.uid()) with check (id = auth.uid());

create policy plants_self on public.plants
  for all using (user_id = auth.uid()) with check (user_id = auth.uid());

create policy photos_self on public.photos
  for all using (user_id = auth.uid()) with check (user_id = auth.uid());

create policy week_tasks_self on public.week_tasks
  for all using (user_id = auth.uid()) with check (user_id = auth.uid());

create policy push_self on public.push_subscriptions
  for all using (user_id = auth.uid()) with check (user_id = auth.uid());

-- Лог человек только читает: пишет в него планировщик своим ключом.
create policy notif_read_self on public.notification_log
  for select using (user_id = auth.uid());

-- ───────────────────────────────────────────── права
-- На Supabase роли anon/authenticated уже есть и default privileges обычно
-- выданы, но полагаться на настройку проекта нельзя: RLS без грантов молча
-- отдаёт «permission denied», а с лишними грантами и без RLS — чужие строки.
-- Поэтому гранты выданы явно и только там, где роли существуют.
do $$
begin
  if exists (select 1 from pg_roles where rolname = 'authenticated') then
    grant usage on schema public to authenticated;
    grant select, insert, update, delete on public.profiles, public.plants,
      public.photos, public.week_tasks, public.push_subscriptions to authenticated;
    grant select on public.notification_log to authenticated;
  end if;
  if exists (select 1 from pg_roles where rolname = 'anon') then
    grant usage on schema public to anon;   -- anon не читает данные: только вход
  end if;
end $$;
