// Grab the DOM elements for the menu
const browseLink = document.querySelectorAll(".browse-link");
const closeMenuBtn = document.getElementById("close-menu")
const browse = document.getElementById("browse");

/** Opens the search browser menu */
export function openBrowse() {
    const overlayEl = document.createElement('div');
    document.body.appendChild(overlayEl);
    overlayEl.classList.add('overlay');
    browse.classList.add("browse-open");
	closeMenuBtn.addEventListener('click', () => {
		browse.classList.remove('browse-open');
		overlayEl.remove();
	})
    overlayEl.addEventListener('click', () => {
        browse.classList.remove("browse-open")
        overlayEl.remove();
    })
}

// There are two links (desktop, mobile) that should open the menu, so
// we have to apply the click event listener to both.
browseLink.forEach(link => link.addEventListener('click', openBrowse));


// Grab the DOM elements related to the textbook search.
const inputElement = document.getElementById('search-input');
const searchForm = document.getElementById('search-form');
const searchButton = document.getElementById('search-button');

/** Submit the search form only if there is a value in the field and the
 * Enter key / button icon was pressed, otherwise
 * disable the search icon button.
 */
inputElement.addEventListener('change', event => {
    if (event.target.value.length === 0) {
			searchButton.disabled = true;
		} else {
			searchButton.disabled = false;
		}
	if (event.key === 'Enter') {
		event.preventDefault();

		if (event.target.value.length === 0) {
			return;
		} else {
			searchForm.submit();
		}
	}
});

searchButton.addEventListener('click', () => {
	searchForm.submit();
});
