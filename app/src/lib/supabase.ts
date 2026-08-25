// Клиент Supabase: база и вход.
//
// URL и publishable-ключ лежат прямо здесь и это нормально: ключ по замыслу
// публичный, он уходит в браузер к каждому человеку. Данные закрывает не
// секретность ключа, а RLS — политики привязаны к auth.uid(), и без входа
// анонимный запрос не отдаёт и не пишет ни строки (проверено: POST в plants
// возвращает 42501). Секретный service_role в клиент не попадает никогда.

import type { SupabaseClient } from '@supabase/supabase-js'

const SUPABASE_URL = 'https://bslttprzsbigcfplpxff.supabase.co'
const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_QpG40q5C2r7sUf5Lx2GwGA_PjLfeqVm'

// Библиотека грузится отдельным чанком и НЕ блокирует первый кадр: она весит
// больше, чем всё приложение (+59 КБ в гзипе), а экраны рисуются из
// localStorage мгновенно и без сети. Сессия подхватывается чуть позже — это
// незаметно, а задержка первого кадра была бы заметна.
let client: SupabaseClient | null = null
let loading: Promise<SupabaseClient> | null = null

export function supa(): Promise<SupabaseClient> {
  if (client) return Promise.resolve(client)
  if (!loading) {
    loading = import('@supabase/supabase-js').then(({ createClient }) => {
      client = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
        auth: {
          // PKCE задан явно: он возвращает код в query (?code=…), а implicit
          // кладёт токены в хеш — а на хеше у нас висит роутер экранов.
          flowType: 'pkce',
          detectSessionInUrl: true,
          persistSession: true,
          autoRefreshToken: true,
        },
      })
      return client
    })
  }
  return loading
}

// Хук для проверки, как __state()/__audit(): даёт стенду дотянуться до клиента
// и, например, получить ссылку входа без настоящего перехода на Google.
;(window as unknown as { __supa?: typeof supa }).__supa = supa

/** Куда Google возвращает человека. Работает и на Pages, и на localhost. */
export const authRedirect = () => location.origin + import.meta.env.BASE_URL

/**
 * Экран, на который надо попасть после возврата от провайдера. Страница при
 * этом перезагружается целиком, поэтому в состоянии его не сохранить — кладём
 * рядом с состоянием в localStorage.
 */
const NEXT_KEY = 'hg.authNext'
export const setAuthNext = (id: string) => {
  try { localStorage.setItem(NEXT_KEY, id) } catch { /* приватный режим */ }
}
export const takeAuthNext = (): string | null => {
  try {
    const v = localStorage.getItem(NEXT_KEY)
    if (v) localStorage.removeItem(NEXT_KEY)
    return v
  } catch { return null }
}
