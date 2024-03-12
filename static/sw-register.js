// main thread
// Service Worker Registration

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/serviceworker.js');
}