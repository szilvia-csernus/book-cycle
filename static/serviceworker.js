// v1

const assets = [
	'/',
	'/static/css/account.css',
    '/static/css/base.css',
    '/static/css/checkout.css',
    '/static/css/home.css',
    '/static/css/inventory.css',
    '/static/css/loader.css',
    '/static/css/modal.css',
    '/static/css/orders.css',
    '/static/css/shopping_bag.css',
    '/static/js/bag.js',
    '/static/js/book_management.js',
    '/static/js/books.js',
    '/static/js/checkout.js',
    '/static/js/menu.js',
    '/static/js/modal.js',
    '/static/js/stripe_elements.js',
    '/static/js/toast.js',
	'sw-register.js',
	'https://fonts.googleapis.com/css2?family=KoHo:wght@300;500;600&family=Koulen&display=swap'
];

// Service Worker Installation
// 'self' used instead of 'this', it's safer to use
// self is the service worker itself, it's a different thread from the main thread.
self.addEventListener('install', (event) => {
	event.waitUntil(
		caches.open('assets').then((cache) => {
			// Fetch the list of static files from your API
			fetch('/inventory/book-image-urls/')
				.then((response) => {
					if (!response.ok) {
						throw new Error('Network response was not ok');
					}
					return response.json();
				})
				.then((imageUrls) => {
					// Add the image urls to the assets array
					assets.push(...imageUrls);
					// Cache all assets
					return cache.addAll(assets);
				})
				.catch((error) => {
					console.error(
						'There has been a problem with your fetch operation:',
						error
					);
				});
		})
	);
});


// Stale while revalidate strategy
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then( cachedResponse => {
                // Even if the response is in the cache, we fetch it
                // and update the cache for future usage
                const fetchPromise = fetch(event.request).then(
                     networkResponse => {
                        caches.open("assets").then( cache => {
                            cache.put(event.request, networkResponse.clone());
                        });
                    return networkResponse;
                    });
                // We use the currently cached version if it's there
                return cachedResponse || fetchPromise; // cached or a network fetch
            })
        );
    });