// Close toast message
const toastContainer = document.getElementById('toast-container');
const toastElement = document.getElementById('toast');
const toastCloseButton = document.getElementById('toast-close-button');

const activateToast = () => {
    toastContainer.classList.add('toast-container-active')
    // setTimeout(closeToast, 5000);
}

const closeToast = () => {
    hideToast()
    setTimeout(removeToastContainer, 500)
}

const hideToast = () => {
    toastElement.classList.add("toast-disappear")
}

const removeToastContainer = () => {
    if (toastContainer.classList.contains('toast-container-active')) {
        toastContainer.classList.remove('toast-container-active');
    }
}



toastCloseButton.addEventListener('click', () => {
    closeToast()
});

activateToast();
