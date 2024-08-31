// v1

const staticFilesUrls = [
    'https://fonts.googleapis.com/css2?family=KoHo:wght@300;500;600&family=Koulen&display=swap',
];

const imageFilesUrls = [];

// Service Worker Installation
self.addEventListener('install', (event) => {
	const fetchStaticFileURLs = async () => {
    const response = await fetch("/static-file-urls/", {
      mode: "cors",
      credentials: "omit",
    });
    const data = await response.json();
    staticFilesUrls.push(...data);
    return staticFilesUrls;
  };

  const fetchImageFileURLs = async () => {
    const response = await fetch("/inventory/book-image-urls/", {
      mode: "cors",
      credentials: "omit",
    });
    const data = await response.json();
    imageFilesUrls.push(...data);
    return imageFilesUrls;
  };

	event.waitUntil(
    caches.open("static_files").then(async (cache) => {
			const urls = await fetchStaticFileURLs();
			const corsRequests = urls.map(
        (url) => new Request(url, { mode: "cors", credentials: "omit" })
      );
			return await Promise.all(
				corsRequests.map((request) => fetch(request).then((response) => cache.put(request, response))
				)
			);
    })
  );

	event.waitUntil(
		caches.open('image_files').then(async (cache) => {
			const urls = await fetchImageFileURLs();
			const corsRequests = urls.map(
        (url) => new Request(url, { mode: "cors", credentials: "omit" })
      );
      return Promise.all(
        corsRequests.map((request) =>
          fetch(request).then((response) => cache.put(request, response))
        )
      );
		})
	);
});

// Cache first strategy
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Exclude all paths that start with /accounts/ from cache
  if (url.pathname.startsWith("/accounts/")) {
    event.respondWith(fetch(event.request));
    return;
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      return (
        response || fetch(event.request, { mode: "cors", credentials: "omit", redirect: "follow" })
      );
    })
  );
});
