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
