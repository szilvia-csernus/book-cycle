// If user changes the book's picture, update its name.
const image = document.getElementById('new-image');
const filename = document.getElementById('filename');
image?.addEventListener('change', () => {
    const file = image.files[0]?.name;
    filename.textContent = 'Image will be set to: ' + file;
})

// If user selects a new image, uncheck the "Remove" input field

const clearImageCkeckbox = document.getElementById('image-clear_id');
const fileName = document.getElementById('filename');
image?.addEventListener('change', () => {
	if (image.files.length > 0) {
        if (clearImageCkeckbox) {
        clearImageCkeckbox.checked = false;
        }
    }
});

clearImageCkeckbox?.addEventListener('change', () => {
    if (clearImageCkeckbox.checked === true) {
        console.log(image.files.length)
        image.value = '';
        console.log(image.files);
        filename.textContent = '';
    }
})