// Grab toast elements
const toastContainer = document.getElementById('toast-container');
const toastElement = document.getElementById('toast');
const toastCloseButton = document.getElementById('toast-close-button');

/** Apply styles to toast elements to make it appear */
const activateToast = () => {
    toastContainer.classList.add('toast-container-active');
    // setTimeout(closeToast, 5000);
}

/** Apply the disappear effect to toast and hide its container
 * after a delay. */
const closeToast = () => {
    hideToast()
    setTimeout(removeToastContainer, 500)
}

/** Apply the disappear effect to the toast */
const hideToast = () => {
    toastElement.classList.add("toast-disappear")
}

/** Hide the toast's container. */
const removeToastContainer = () => {
    if (toastContainer.classList.contains('toast-container-active')) {
        toastContainer.classList.remove('toast-container-active');
    }
}

// Add event listener to close the toast on clicking 'X'.
toastCloseButton.addEventListener('click', closeToast);


// Grab shopping bag icon element and apply an event listener
// that closes the toast this element gets clicked.
const bagIcon = document.getElementById('bag-link');
bagIcon.addEventListener('click', closeToast);


document.addEventListener('scroll', () => {
    setTimeout(closeToast, 1000)
});


activateToast();
