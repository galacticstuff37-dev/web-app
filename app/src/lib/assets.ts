// Фото лежат в /img у корня репозитория и НЕ дублируются в public: их 4.5 МБ.
// База сборки — /web-app/react/, значит корень ассетов на уровень выше.
// В dev-сервере base = '/', и фото берутся из ../img относительно app/.
const BASE = import.meta.env.BASE_URL // '/web-app/react/' в сборке, '/' в dev

export const ASSET_ROOT = BASE.endsWith('react/')
  ? BASE.slice(0, -'react/'.length)
  : BASE

/** Путь к фото вида или журнала: img('radish') -> '/web-app/img/radish.jpg' */
export const img = (name: string) => `${ASSET_ROOT}img/${name}.jpg`

/** CSS-значение для background-image. Пустое имя даёт 'none', а не битую ссылку. */
export const bg = (name: string | null | undefined) =>
  name ? `url(${img(name)})` : 'none'
