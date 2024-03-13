// v1

const static_files = [
    'https://fonts.googleapis.com/css2?family=KoHo:wght@300;500;600&family=Koulen&display=swap',
];

const image_files = [];

// Service Worker Installation
self.addEventListener('install', (event) => {
	const fetch_static_files = async () => {
		const response = await fetch('/static-file-urls/');
		const data = await response.json();
		static_files.push(...data);
		return static_files;
	};

	const fetch_image_files = async () => {
		const response = await fetch('/inventory/book-image-urls/');
		const data = await response.json();
		image_files.push(...data);
		return image_files;
	};

	event.waitUntil(
		caches.open('static_files').then(async (cache) => {
			const staticFiles = await fetch_static_files();
			return cache.addAll(staticFiles);
		})
	);

	event.waitUntil(
		caches.open('image_files').then(async (cache) => {
			const imageFiles = await fetch_image_files();
			return cache.addAll(imageFiles);
		})
	);
});

// Cache first strategy
self.addEventListener('fetch', (event) => {
	event.respondWith(
		caches.match(event.request).then((response) => {
			return response || fetch(event.request, { mode: 'cors' });
		})
	);
});
