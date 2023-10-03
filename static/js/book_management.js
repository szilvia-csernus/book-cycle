// If user changes the book's picture, update its name.
const image = document.getElementById('new-image');
const filename = document.getElementById('filename');
image?.addEventListener('change', () => {
    const file = image.files[0]?.name;
    filename.textContent = 'Image will be set to: ' + file;
})