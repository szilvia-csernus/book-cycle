// Toggle the visibility of the modal element
const toggleModal = (modalElement) => {
	if (modalElement.classList.contains('modal-active')) {
		modalElement.classList.remove('modal-active');
	} else {
		modalElement.classList.add('modal-active');
	}
};

// Grab Signout links and modal element. There is one potential signout link in the
// header in desktop view and another in the Account page in mobile view. Only
// one of the two gets rendered.
const signoutLinks = document.querySelectorAll('.signout-link');
const signoutModal = document.getElementById('signout-modal');

// Add event listener to signout link to render modal
signoutLinks.forEach( link => link.addEventListener('click', () => {
	toggleModal(signoutModal);
	// Grab and add event listener to Cancel button to close modal
	const cancelBtn = document.getElementById('signout-cancel');
	cancelBtn.addEventListener('click', () => {
		toggleModal(signoutModal)
	})
}))
