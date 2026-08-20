const CACHE = 'homegrown-4b1bba15a0';
const ASSETS = [
  './', './index.html', './manifest.webmanifest', './scan-config.js',
  './img/hero.jpg', './img/garden.jpg', './img/radish.jpg', './img/basil.jpg',
  './img/flowers.jpg', './img/containers.jpg',
  './img/leaves1.jpg', './img/leaves2.jpg', './img/leaves3.jpg',
  './img/icon-192.png', './img/icon-512.png', './img/apple-touch-icon.png',
  './fonts/Caprasimo-400-latin.woff2', './fonts/Caprasimo-400-latin-ext.woff2',
  './fonts/InterTight-400-latin.woff2', './fonts/InterTight-400-latin-ext.woff2'
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const isDoc = req.mode === 'navigate' || req.destination === 'document';
  if (isDoc) {
    // HTML — только из сети, кэш лишь как офлайн-запасной. Иначе обновления
    // никогда не доходят до вернувшегося посетителя.
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put('./index.html', copy)).catch(() => {});
        return res;
      }).catch(() => caches.match('./index.html'))
    );
    return;
  }
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
      return res;
    }))
  );
});
