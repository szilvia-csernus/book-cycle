// Close toast message
const toastElement = document.getElementById('message-container');
const toastCloseButton = document.getElementById('toast-close-button');

toastElement.classList.add("message-active");

const inactivateToastElement = () => {
    if (toastElement.classList.contains('message-active')) {
        toastElement.classList.remove('message-active');
    }
}

// setTimeout(inactivateToastElement, 5000)

toastCloseButton.addEventListener('click', () => {
    inactivateToastElement()
});
