// v1

const staticFilesUrls = [
    'https://fonts.googleapis.com/css2?family=KoHo:wght@300;500;600&family=Koulen&display=swap',
];

const imageFilesUrls = [];

// Service Worker Installation
self.addEventListener('install', (event) => {
	const fetch_static_files = async () => {
    const response = await fetch("/static-file-urls/", {
      mode: "cors",
      credentials: "omit",
    });
    const data = await response.json();
    staticFilesUrls.push(...data);
    return staticFilesUrls;
  };

  const fetch_image_files = async () => {
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
			const urls = await fetch_static_files();
			const corsRequests = urls.map((url) => new Request(url, { mode: "cors" }));
			return await Promise.all(
				corsRequests.map((request) => fetch(request).then((response) => cache.put(request, response))
				)
			);
    })
  );

	event.waitUntil(
		caches.open('image_files').then(async (cache) => {
			const urls = await fetch_image_files();
			const corsRequests = urls.map(
        (url) => new Request(url, { mode: "cors" })
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
	event.respondWith(
		caches.match(event.request).then((response) => {
			return (
				response || fetch(event.request, { mode: 'cors', redirect: 'follow' })
			);
		})
	);
});
