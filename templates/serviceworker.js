// v2

const staticFilesUrls = [
  "https://fonts.googleapis.com/css2?family=KoHo:wght@300;500;600&family=Koulen&display=swap",
];

const imageFilesUrls = [];
const cachedUrls = new Set([...staticFilesUrls]);

// Service Worker Installation
self.addEventListener("install", (event) => {
  const fetchStaticFileURLs = async () => {
    const response = await fetch("/static-file-urls/", {
      mode: "cors",
      credentials: "omit",
    });
    const data = await response.json();
    staticFilesUrls.push(...data);
    cachedUrls.add(...data);
    return staticFilesUrls;
  };

  const fetchImageFileURLs = async () => {
    const response = await fetch("/inventory/book-image-urls/", {
      mode: "cors",
      credentials: "omit",
    });
    const data = await response.json();
    imageFilesUrls.push(...data);
    cachedUrls.add(...data);
    return imageFilesUrls;
  };

  event.waitUntil(
    caches.open("static_files").then(async (cache) => {
      const urls = await fetchStaticFileURLs();
      return await Promise.all(
        urls.map((url) =>
          fetch(url, {mode: "cors"}).then((response) => cache.put(url, response))
        )
      );
    })
  );

  event.waitUntil(
    caches.open("image_files").then(async (cache) => {
      const urls = await fetchImageFileURLs();
      return Promise.all(
        urls.map((url) =>
          fetch(url, { mode: "cors" }).then((response) =>
            cache.put(url, response)
          )
        )
      );
    })
  );
});

// Cache first strategy for static and image files only
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // Check if the request URL is in the cached URLs set
  if (cachedUrls.has(url.href)) {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request, { mode: "cors" }).then((networkResponse) => {
          return caches.open("dynamic").then((cache) => {
            cache.put(event.request, networkResponse.clone());
            return networkResponse;
          });
        }).catch(() => {
          return new Response("Network error occurred", {
            status: 408,
            statusText: "Network error",
          });
        });
      })
    );
  } else {
    // For other requests, fetch from the network
    event.respondWith(
      fetch(event.request, { mode: "cors" }).then((networkResponse) => {
        return caches.open("dynamic").then((cache) => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
      }).catch(() => {
        return new Response("Network error occurred", {
          status: 408,
          statusText: "Network error",
        });
      })
    );
  }
});
