-- Гигиена RLS под рост до тысяч аккаунтов. Три правки, каждая из документации
-- Supabase (Troubleshooting → RLS performance), а не из общих соображений.
--
-- 1. auth.uid() в подзапросе. Без обёртки функция вызывается НА КАЖДУЮ строку;
--    в подзапросе планировщик считает её один раз (initPlan). В замерах
--    Supabase это 179 мс → 9 мс на простом сравнении.
-- 2. TO authenticated. Политика без роли проверяется и для анонимных запросов —
--    отсекаем их до обращения к данным.
-- 3. Индексы на колонки, по которым фильтрует политика. У photos фильтр идёт по
--    user_id, а индекс был только по plant_id: на сканировании всей таблицы
--    политика и работала. У push_subscriptions индекс был частичный
--    (where failed_at is null), под фильтр политики он не подходит.

drop policy if exists profiles_self   on public.profiles;
drop policy if exists plants_self     on public.plants;
drop policy if exists photos_self     on public.photos;
drop policy if exists week_tasks_self on public.week_tasks;
drop policy if exists push_self       on public.push_subscriptions;
drop policy if exists notif_read_self on public.notification_log;

create policy profiles_self on public.profiles
  for all to authenticated
  using (id = (select auth.uid())) with check (id = (select auth.uid()));

create policy plants_self on public.plants
  for all to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

create policy photos_self on public.photos
  for all to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

create policy week_tasks_self on public.week_tasks
  for all to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

create policy push_self on public.push_subscriptions
  for all to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));

create policy notif_read_self on public.notification_log
  for select to authenticated
  using (user_id = (select auth.uid()));

-- Индексы под фильтр политик (partial-индексы из 0001 остаются: они под выборки
-- живых строк, а эти — под RLS).
create index if not exists photos_user_idx on public.photos (user_id);
create index if not exists push_user_all_idx on public.push_subscriptions (user_id);

-- Две таблицы растут линейно по времени, а не по числу людей: 1000 человек ×
-- 6 задач × 52 недели ≈ 300 тыс. строк в год плюс столько же в логе отправок.
-- Держать это вечно незачем — недельные отметки не нужны через квартал, а лог
-- нужен только чтобы не отправить два одинаковых пуша в один день.
create or replace function public.prune_history(keep_days integer default 90)
returns integer language plpgsql security definer set search_path = public as $$
declare
  gone integer := 0;
  n    integer;
begin
  delete from public.week_tasks where week_start < current_date - keep_days;
  get diagnostics n = row_count;  gone := gone + n;
  delete from public.notification_log where sent_on < current_date - keep_days;
  get diagnostics n = row_count;  gone := gone + n;
  return gone;
end $$;

comment on function public.prune_history is
  'Чистка истории. Вешается на pg_cron: select cron.schedule(''prune'', ''0 4 * * *'', $$select public.prune_history(90)$$);';
