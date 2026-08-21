import fs from 'node:fs'
import path from 'node:path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Собираемся в /react у корня репозитория: GitHub Pages раздаёт корень, а живой
// прототип index.html остаётся на месте и не задет.
// Фото (4.5 МБ) не дублируем в public — они лежат в /img и берутся оттуда,
// см. src/lib/assets.ts. Шрифты (164 КБ) продублированы, потому что @font-face
// в собранном CSS не может ссылаться на путь за пределами базы.
// В dev корень репозитория лежит выше корня проекта, поэтому отдаём его сами:
// оттуда берутся фото (4.5 МБ, дублировать в public не станем) и сам прототип —
// он нужен в iframe на маршруте /review для сверки бок о бок.
// В сборке этого не требуется: на Pages и /web-app/img, и /web-app/index.html
// раздаются как есть.
const MIME: Record<string, string> = {
  '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml',
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript',
  '.json': 'application/json', '.woff2': 'font/woff2',
  '.webmanifest': 'application/manifest+json',
}
function serveRepoRoot() {
  return {
    name: 'serve-repo-root',
    configureServer(server: import('vite').ViteDevServer) {
      server.middlewares.use((req, res, next) => {
        const m = req.url?.match(/^\/web-app\/(?!react\/)(.+)$/)
        if (!m) return next()
        const rel = m[1].split('?')[0]
        const file = path.resolve(__dirname, '..', rel)
        // не выпускаем за пределы репозитория
        if (!file.startsWith(path.resolve(__dirname, '..'))) return next()
        if (!fs.existsSync(file) || !fs.statSync(file).isFile()) return next()
        res.setHeader('Content-Type', MIME[path.extname(file)] || 'application/octet-stream')
        fs.createReadStream(file).pipe(res)
      })
    },
  }
}

export default defineConfig({
  plugins: [react(), serveRepoRoot()],
  base: '/web-app/react/',
  build: {
    outDir: '../react',
    emptyOutDir: true,
  },
})
