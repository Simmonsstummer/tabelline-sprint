// Service Worker per Tabelline Sprint
// Strategia: cache-first per gli asset locali, network-first per il resto.
// Cambia CACHE_VERSION quando aggiorni l'app per forzare il refresh della cache.

const CACHE_VERSION = 'v2';
const CACHE_NAME = `tabelline-sprint-${CACHE_VERSION}`;

const CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './favicon.ico',
  './icon-180.png',
  './icon-192.png',
  './icon-512.png'
];

// INSTALL: pre-cache degli asset principali
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(CORE_ASSETS))
      .then(() => self.skipWaiting())
      .catch(err => console.log('SW install error:', err))
  );
});

// ACTIVATE: pulisce vecchie cache
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// FETCH: cache-first con fallback network, e caching opportunistico di Google Fonts
self.addEventListener('fetch', event => {
  const req = event.request;

  // Solo GET
  if (req.method !== 'GET') return;

  event.respondWith(
    caches.match(req).then(cached => {
      if (cached) return cached;

      return fetch(req).then(resp => {
        // Cache opportunistica per asset utili (fonts, immagini)
        const url = new URL(req.url);
        const shouldCache = (
          resp && resp.status === 200 &&
          (url.origin === location.origin ||
           url.hostname === 'fonts.googleapis.com' ||
           url.hostname === 'fonts.gstatic.com')
        );
        if (shouldCache) {
          const respClone = resp.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(req, respClone));
        }
        return resp;
      }).catch(() => {
        // Se offline e la richiesta era una navigazione, restituisci la home cached
        if (req.mode === 'navigate') {
          return caches.match('./index.html');
        }
        return new Response('', { status: 503 });
      });
    })
  );
});
