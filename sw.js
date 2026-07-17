const CACHE_NAME = 'j-hub-cache-v4';
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

// Network-First 전략: 무조건 서버에서 최신 데이터를 먼저 가져오고, 인터넷이 끊겼을 때만 캐시를 보여줌
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 네트워크 성공 시 새 데이터를 캐시에 덮어씌움
        if(response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // 오프라인 상태일 때만 캐시 사용
        return caches.match(event.request);
      })
  );
});
