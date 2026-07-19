const CACHE_NAME = 'j-hub-cache-v6';
const urlsToCache = [
  './manifest.json'
];

self.addEventListener('install', event => {
  self.skipWaiting(); // 새로 업데이트된 SW가 대기하지 않고 즉시 활성화되도록 강제
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          // 이전 버전(v1)의 찌꺼기 캐시를 완벽히 삭제
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim()) // 열려있는 모든 클라이언트 페이지 제어권 즉시 확보
  );
});

// Network-First 전략 (FUNC-02 FIX: 서버 오류 시에도 캐시 Fallback)
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 네트워크 성공 + 정상 응답 시 캐시에 저장
        if(response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        // FUNC-02 FIX: 서버 오류(4xx/5xx) 시 캐시된 정상 버전 반환
        if (!response.ok) {
          return caches.match(event.request).then(cached => cached || response);
        }
        return response;
      })
      .catch(() => {
        // 오프라인 상태일 때만 캐시 사용
        return caches.match(event.request);
      })
  );
});
