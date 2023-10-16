// Display modal
const addModal = (modalElement, canceBtnId) => {
	modalElement.classList.add('modal-active');
	// Grab and add event listener to Cancel button to close modal
	const cancelBtn = document.getElementById(canceBtnId);
	cancelBtn.addEventListener('click', () => {
		removeModal(modalElement, () => {});
	});
};

// Remove modal
const removeModal = (modalElement) => {
	if (modalElement.classList.contains('modal-active')) {
		modalElement.classList.remove('modal-active');
	}
};

// Grab Signout links and modal element. There is one potential signout link in the
// header in desktop view and another in the Account page in mobile view. Only
// one of the two gets rendered.
const signoutLinks = document.querySelectorAll('.signout-link');
const signoutModal = document.getElementById('signout-modal');


// Add event listener to signout link to render modal
signoutLinks?.forEach( link => link.addEventListener('click', () => {
	addModal(signoutModal, 'signout-cancel');
}));


// Grab Delete User button and Modal elements
const deleteUserBtn = document.getElementById('delete-profile');
const deleteUserModal = document.getElementById('delete-user-modal');

deleteUserBtn?.addEventListener('click', () => {
	addModal(deleteUserModal, 'delete-user-cancel');
});

// Grab Delete Book and Modal elements
const deleteBookBtn = document.getElementById('delete-book');
const deleteBookModal = document.getElementById('delete-book-modal');

deleteBookBtn?.addEventListener('click', () => {
	addModal(deleteBookModal, 'delete-book-cancel');
});
