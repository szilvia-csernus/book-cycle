// v3

const staticFilesUrls = [
  "https://fonts.googleapis.com/css2?family=KoHo:wght@300;500;600&family=Koulen&display=swap",
];

const imageFilesUrls = [];
const cachedUrls = new Set([...staticFilesUrls]);

// Service Worker Installation
self.addEventListener("install", (event) => {
  const fetchStaticFileURLs = async () => {
    try {
      const response = await fetch("/static-file-urls/", {
        mode: "cors",
        credentials: "omit",
      });
      const data = await response.json();
      staticFilesUrls.push(...data);
      cachedUrls.add(...data);
      return staticFilesUrls;
    } catch (error) {
      console.error("Error fetching static file URLs:", error);
      throw error;
    }
  };

  const fetchImageFileURLs = async () => {
    try {
      const response = await fetch("/inventory/book-image-urls/", {
        mode: "cors",
        credentials: "omit",
      });
      const data = await response.json();
      imageFilesUrls.push(...data);
      cachedUrls.add(...data);
      return imageFilesUrls;
    } catch (error) {
      console.error("Error fetching image file URLs:", error);
      throw error;
    }
  };

  event.waitUntil(
    caches.open("static_files").then(async (cache) => {
      try {
        const urls = await fetchStaticFileURLs();
        await Promise.all(
          urls.map(async (url) => {
            try {
              const response = await fetch(url, { mode: "no-cors" });
              if (response.ok) {
                await cache.put(url, response.clone());
              } else {
                console.error(`Failed to fetch ${url}: ${response.statusText}`);
              }
            } catch (error) {
              console.error(`Fetch error for ${url}:`, error);
            }
          })
        );
      } catch (error) {
        console.error("Error during static files caching:", error);
      }
    })
  );

  event.waitUntil(
    caches.open("image_files").then(async (cache) => {
      try {
        const urls = await fetchImageFileURLs();
        await Promise.all(
          urls.map(async (url) => {
            try {
              const response = await fetch(url, { mode: "no-cors" });
              if (response.ok) {
                await cache.put(url, response.clone());
              } else {
                console.error(`Failed to fetch ${url}: ${response.statusText}`);
              }
            } catch (error) {
              console.error(`Fetch error for ${url}:`, error);
            }
          })
        );
      } catch (error) {
        console.error("Error during image files caching:", error);
      }
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
        return (
          response ||
          fetch(event.request, { mode: "no-cors" })
            .then((networkResponse) => {
              return caches.open("dynamic").then((cache) => {
                cache.put(event.request, networkResponse.clone());
                return networkResponse;
              });
            })
            .catch((error) => {
              console.error(`Network error for ${event.request.url}:`, error);
              return new Response("Network error occurred", {
                status: 408,
                statusText: "Network error",
              });
            })
        );
      })
    );
  } else {
    // For other requests, fetch from the network
    event.respondWith(
      fetch(event.request, { mode: "no-cors" })
        .then((networkResponse) => {
          return caches.open("dynamic").then((cache) => {
            cache.put(event.request, networkResponse.clone());
            return networkResponse;
          });
        })
        .catch((error) => {
          console.error(`Network error for ${event.request.url}:`, error);
          return new Response("Network error occurred", {
            status: 408,
            statusText: "Network error",
          });
        })
    );
  }
});
