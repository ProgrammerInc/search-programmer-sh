/**
 * The cache name should change every time you want to "cache bust"
 * i.e. if you want to change these files
 * in a real-world app this would be handled by your build system
 * e.g. Vite or Next.js would hash the files so the name is unique based on content
 * (style-XYZ123.css etc)
 */
const CACHE_NAME = "programmer-cache-v0.0.7-alpha";
const urlsToCache = [
  "/",
  "/info/en/about",
  "/info/en/search-syntax",
  "/preferences",
  "/search",
  "/stats",
];

/**
 * Listen for the install event, which fires when the service worker is installing.
 * We use event.waitUntil() to ensure the install doesn't finished until our promise resolves
 * so we don't do anything else until the initial caching is done.
 */
self.addEventListener("install", async (event) => {
  self.skipWaiting();

  if (!this.unregistered) {
    event.waitUntil(cache_assets());
  }
});

async function cache_assets() {
  const cache = await self.caches.open(CACHE_NAME);
  return cache.addAll(urlsToCache);
}

/**
 * Listen for the activate event, which is fired after installation
 * Activate is when the service worker actually takes over from the previous
 * version, which is a good time to clean up old caches.
 * Again we use waitUntil() to ensure we don't move on until the old caches are deleted.
 */
self.addEventListener("activate", async (event) => {
  event.waitUntil(delete_old_caches());
});

async function delete_old_caches() {
  // Get the keys of all the old caches
  const keys = await caches.keys();
  const deletePromises = keys
    .filter((key) => key !== CACHE_NAME)
    .map((key) => self.caches.delete(key));
  return Promise.all(deletePromises);
}

/**
 * Listen for browser fetch events.
 * These fire any time the browser tries to load anything.
 * This isn't just fetch() calls; clicking a <a href> triggers it too.
 */
self.addEventListener("fetch", (event) => {
  if (!(event.request.url.indexOf("http") === 0) || this.unregistered) return;
  event.respondWith(get_response(event.request));
});

/**
 * Listen for browser message events.
 * Used to communicate with the background script from the browser.
 */
function messageHandler(event) {
  if (event.data === "purge_cache") {
    caches
      .delete(CACHE_NAME)
      .then((success) => {
        console.log("Cache removal status: " + success);
      })
      .catch((err) => {
        console.log("Cache removal error: ", err);
      });
  }

  if (event.data === "unregister") {
    caches
      .delete(CACHE_NAME)
      .then((success) => {
        this.unregistered = true;
        console.log("Cache removal status: " + success);
        self.registration.unregister().then((success) => {
          console.log("Service worker unregister status: " + success);
        });
      })
      .catch((err) => {
        console.log("Cache removal error: ", err);
      });
  }
}

self.addEventListener("message", (event) => {
  messageHandler(event);
});

/**
 * We follow the "stale-while-revalidate" pattern:
 * respond with the cached response immediately (if we have one)
 * even though this might be "stale" (not the most recent version).
 * In the background fetch the latest version and put that into cache
 * on next request the user will get the latest version
 */
async function get_response(request) {
  const cache = await self.caches.open(CACHE_NAME);
  const cached_response = await cache.match(request);
  // Important: we do not await here, since that would defeat the point of using the cache
  const pending_response = fetch(request).then((response) => {
    if (!this.unregistered) {
      cache.put(request, response.clone());
    }
    return response;
  });
  return cached_response || pending_response;
}
