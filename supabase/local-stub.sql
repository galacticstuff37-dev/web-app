-- Заглушка того, что на Supabase даёт платформа: схема auth с таблицей
-- пользователей и функцией auth.uid(). Нужна ТОЛЬКО для локальной проверки
-- миграции — на Supabase этот файл применять нельзя, там всё это уже есть.
create schema if not exists auth;

create table if not exists auth.users (
  id    uuid primary key default gen_random_uuid(),
  email text
);

create or replace function auth.uid() returns uuid
  language sql stable as $$ select current_setting('request.jwt.claim.sub', true)::uuid $$;

-- На Supabase роли имеют доступ к схеме auth; в заглушке это надо выдать, иначе
-- запрос вида `where user_id = (select auth.uid())` падает на permission denied,
-- хотя внутри политики та же функция работает.
do $$ begin
  if exists (select 1 from pg_roles where rolname = 'authenticated') then
    grant usage on schema auth to authenticated;
  end if;
  if exists (select 1 from pg_roles where rolname = 'anon') then
    grant usage on schema auth to anon;
  end if;
end $$;
